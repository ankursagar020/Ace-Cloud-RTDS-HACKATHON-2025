//#Note that requests are being sent by the model
import openstack
import sqlite3
import json
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Any, List, Optional

# --------------------------
# Configuration
# --------------------------
GEMINI_API_KEY = "AIzaSyDLMVJbi9AU6zFM_WeXjlKNYieqAbiEzlI"
genai.configure(api_key=GEMINI_API_KEY)

OPENSTACK_CLOUD_CONFIG = {
    "auth_url": "https://api-ap-south-mum-1.openstack.acecloudhosting.com:5000/v3/auth/tokens?nocatalog",
    "project_name": "Hackathon_AIML_1",
    "username": "Hackathon_AIML_1",
    "password": "Hackathon_AIML_1@567",
    "user_domain_name": "Default",
    "project_domain_name": "Default"
}
USER_ROLE = "user"

# Initialize clients
conn = openstack.connect(**OPENSTACK_CLOUD_CONFIG)

# Initialize database
db_conn = sqlite3.connect('requests.db')
db_cursor = db_conn.cursor()
db_cursor.execute('''CREATE TABLE IF NOT EXISTS requests
                     (id INTEGER PRIMARY KEY, user TEXT, command TEXT, 
                      intent TEXT, parameters TEXT, status TEXT, 
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

# --------------------------
# Core Functions
# --------------------------
class OperationManager:
    def __init__(self):
        self.current_intent: Optional[str] = None
        self.entities: Dict[str, Any] = {}
        self.required_params: Dict[str, List[str]] = {
            "create_vm": ["name", "flavor", "image", "network"],
            "resize_vm": ["name", "new_flavor"],
            "delete_vm": ["name"],
            "create_network": ["name", "cidr"],
            "delete_network": ["name"],
            "create_volume": ["name", "size"],
            "delete_volume": ["name"]
        }
        self.admin_actions = ["delete_vm", "delete_network", "delete_volume"]

    def parse_intent(self, user_input: str) -> Dict[str, Any]:
        """Parse user input using Gemini with parameter extraction"""
        prompt = f"""Analyze this cloud operation command: "{user_input}"
        Respond EXACTLY in this JSON format:
        {{
            "intent": "create_vm|resize_vm|delete_vm|create_network|delete_network|create_volume|delete_volume",
            "parameters": {{"param1": "value", ...}},
            "missing": ["param1", "param2"],
            "valid": true/false,
            "message": "clarification question if needed"
        }}
        If unsure, set "valid": false"""
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            response_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(response_text)
        except Exception as e:
            return {"valid": False, "message": str(e)}

    def check_permissions(self) -> bool:
        """Check if user has permission for the action"""
        if self.current_intent in self.admin_actions and USER_ROLE != "admin":
            return False
        return True

    def collect_parameters(self):
        """Collect missing parameters with user prompts"""
        for param in self.required_params.get(self.current_intent, []):
            if param not in self.entities or not self.entities[param]:
                prompt = self._get_param_prompt(param)
                value = input(f"Assistant: {prompt}\nYou: ").strip()
                self.entities[param] = value

    def _get_param_prompt(self, param: str) -> str:
        """Generate user-friendly parameter prompts"""
        prompts = {
            "name": lambda: f"What should we name the {self.current_intent.split('_')[1]}?",
            "flavor": lambda: "Which flavor? Available: " + ", ".join([f.name for f in conn.compute.flavors()]),
            "image": lambda: "Which image? Available: " + ", ".join([f.name for f in conn.image.images()]),
            "network": lambda: "Which network? Available: " + ", ".join([n.name for n in conn.network.networks()]),
            "cidr": lambda: "Enter CIDR block (e.g., 192.168.1.0/24):",
            "size": lambda: "Enter size in GB:",
            "new_flavor": lambda: "Enter new flavor for resize: Available: " + ", ".join([f.name for f in conn.compute.flavors()])
        }
        return prompts.get(param, lambda: f"Please enter {param.replace('_', ' ')}:")()

    def execute_action(self) -> str:
        """Execute OpenStack operation with full validation"""
        try:
            if not self.check_permissions():
                return "Permission denied: Admin privileges required for this action"

            if self.current_intent == "create_vm":
                return self._create_vm()
            elif self.current_intent == "resize_vm":
                return self._resize_vm()
            elif self.current_intent == "delete_vm":
                return self._delete_resource("compute", "server")
            elif self.current_intent == "create_network":
                return self._create_network()
            elif self.current_intent == "delete_network":
                return self._delete_resource("network", "network")
            elif self.current_intent == "create_volume":
                return self._create_volume()
            elif self.current_intent == "delete_volume":
                return self._delete_resource("block_storage", "volume")
            return "Unsupported action"
        except Exception as e:
            return f"Operation failed: {str(e)}"

    def _create_vm(self) -> str:
        """Create virtual machine using Nova API"""
        flavor = conn.compute.find_flavor(self.entities["flavor"])
        image = conn.image.find_image(self.entities["image"])
        network = conn.network.find_network(self.entities["network"])

        if not all([flavor, image, network]):
            return "Error: Invalid flavor, image, or network specified"

        server = conn.compute.create_server(
            name=self.entities["name"],
            flavor_id=flavor.id,
            image_id=image.id,
            networks=[{"uuid": network.id}]
        )
        server = conn.compute.wait_for_server(server)
        return f"VM '{self.entities['name']}' created! ID: {server.id}, IP: {self._get_server_ip(server)}"

    def _resize_vm(self) -> str:
        """Resize VM using Nova API"""
        server = conn.compute.find_server(self.entities["name"])
        new_flavor = conn.compute.find_flavor(self.entities["new_flavor"])

        if not server:
            return "Error: VM not found"
        if not new_flavor:
            return "Error: Invalid flavor specified"

        conn.compute.resize_server(server, new_flavor.id)
        conn.compute.wait_for_server_resize(server)
        return f"VM '{self.entities['name']}' resized to {new_flavor.name} successfully"

    def _create_network(self) -> str:
        """Create network using Neutron API"""
        network = conn.network.create_network(name=self.entities["name"])
        subnet = conn.network.create_subnet(
            name=f"{self.entities['name']}-subnet",
            network_id=network.id,
            ip_version=4,
            cidr=self.entities["cidr"]
        )
        return f"Network '{self.entities['name']}' created with CIDR {subnet.cidr}"

    def _create_volume(self) -> str:
        """Create volume using Cinder API"""
        volume = conn.block_storage.create_volume(
            name=self.entities["name"],
            size=int(self.entities["size"])
        )
        conn.block_storage.wait_for_status(volume, 'available')
        return f"Volume '{self.entities['name']}' ({self.entities['size']}GB) created"

    def _delete_resource(self, service: str, resource_type: str) -> str:
        """Generic delete function with confirmation"""
        confirm = input(f"Assistant: WARNING: This will PERMANENTLY delete {self.entities['name']}. Type 'y' to confirm: ")
        if confirm.lower() != 'y':
            return "Deletion cancelled"

        service_obj = getattr(conn, service)
        find_method = getattr(service_obj, f"find_{resource_type}")
        delete_method = getattr(service_obj, f"delete_{resource_type}")

        resource = find_method(self.entities["name"])
        if not resource:
            return f"Error: {resource_type.capitalize()} not found"

        delete_method(resource)
        return f"{resource_type.capitalize()} '{self.entities['name']}' deleted successfully"

    def _get_server_ip(self, server) -> str:
        """Get first available IP address"""
        for network in server.addresses.values():
            if network and len(network) > 0:
                return network[0]['addr']
        return "No IP assigned"

# --------------------------
# Main Workflow
# --------------------------
def main():
    manager = OperationManager()
    print("OpenStack Assistant: Hi! How can I help with your cloud operations?")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break

            # Parse user command
            result = manager.parse_intent(user_input)
            
            if not result.get("valid", False):
                print(f"Assistant: {result.get('message', 'Invalid command')}")
                continue

            manager.current_intent = result["intent"]
            manager.entities = result["parameters"]

            # Collect missing parameters
            if result["missing"]:
                print(f"Assistant: {result['message']}")
                manager.collect_parameters()

            # Check permissions
            if not manager.check_permissions():
                print("Assistant: Permission denied: Admin privileges required")
                continue

            # Execute action
            output = manager.execute_action()
            
            # Log result
            status = "success" if "Error" not in output else "failed"
            db_cursor.execute(
                """INSERT INTO requests 
                (user, command, intent, parameters, status) 
                VALUES (?, ?, ?, ?, ?)""",
                ("user", user_input, manager.current_intent, 
                 json.dumps(manager.entities), status)
            )
            db_conn.commit()

            print(f"Assistant: {output}")

        except KeyboardInterrupt:
            print("\nAssistant: Session ended.")
            break
        except Exception as e:
            print(f"Assistant: Critical error occurred: {str(e)}")

if __name__ == "__main__":
    main()
    db_conn.close()
    print("\nSession saved to database.")

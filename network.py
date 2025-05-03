import openstack

# Initialize connection
conn = openstack.connection.Connection(
    auth_url="https://api-ap-south-mum-1.openstack.acecloudhosting.com:5000/v3",
    project_name="",  # Replace with your actual project name
    username="Hackathon_AIML_1",
    password="Hackathon_AIML_1@567",
    user_domain_name="Default",
    project_domain_name="Default",
    region_name="ap-south-mum-1",
    verify=True
)

# Test token to confirm auth
try:
    token = conn.authorize()
    print("✅ Authenticated successfully!")

    print("\n🌐 Available Networks in OpenStack:")
    print("-" * 50)
    found = False
    for network in conn.network.networks():
        found = True
        print(f"{network.name} → {network.id} → Status: {network.status}")
    if not found:
        print("❌ No networks found in your project.")
except Exception as e:
    print(f"❌ Error: {e}")

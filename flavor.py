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

    print("\n📷 Available Flavors in OpenStack:")
    print("-" * 50)
    found = False
    for flavor in conn.compute.flavors():
        found = True
        print(f"{flavor.name} → {flavor.id} → RAM: {flavor.ram}MB, vCPUs: {flavor.vcpus}, Disk: {flavor.disk}GB")
    if not found:
        print("❌ No flavors found in your project.")
except Exception as e:
    print(f"❌ Error: {e}")

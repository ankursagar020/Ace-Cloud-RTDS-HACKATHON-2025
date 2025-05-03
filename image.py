import openstack
# def get_openstack_connection() -> connection.Connection:
#     try:
#         conn = connection.Connection(
#             auth_url = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:5000/v3",
#             project_name = "admin",
#             username = "Hackathon_AIML_1",
#             password = "Hackathon_AIML_1@567",
#             user_domain_name = "Default",
#             project_domain_name = "Default",
#             region_name = "ap-south-mum-1",
#             verify = True
#         )
#         print("✅ Auth succeeded")
#         return conn
#     except Exception as e:
#         print("❌ Auth failed:", e)
# Initialize connection
conn = openstack.connection.Connection(
    auth_url = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:5000/v3",
        project_name = "",
        username = "Hackathon_AIML_1",
        password = "Hackathon_AIML_1@567",
        user_domain_name = "Default",
        project_domain_name = "Default",
        region_name = "ap-south-mum-1",
        verify = True
)

# Test token to confirm auth
try:
    token = conn.authorize()
    print("✅ Authenticated successfully!")

    print("\n📷 Available Images in OpenStack:")
    print("-" * 50)
    found = False
    for image in conn.compute.images():
        found = True
        print(f"{image.name} → {image.id}")
    if not found:
        print("❌ No images found in your project.")
except Exception as e:
    print(f"❌ Error: {e}")

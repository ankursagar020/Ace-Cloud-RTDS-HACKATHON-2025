import sys
from openstack import connection
from openstack.compute.v2.server import Server
from openstack.block_storage.v3.volume import Volume
from typing import List, Optional


def get_openstack_connection() -> connection.Connection:
    try:
        conn = connection.Connection(
            auth_url="https://api-ap-south-mum-1.openstack.acecloudhosting.com:5000/v3",
            project_name="",
            username="Hackathon_AIML_1",
            password="Hackathon_AIML_1@567",
            user_domain_name="Default",
            project_domain_name="Default",
            region_name="ap-south-mum-1",
            verify=True
        )
        print("✅ Auth succeeded")
        return conn
    except Exception as e:
        print("❌ Auth failed:", e)


def create_server(
    conn: connection.Connection,
    name: str,
    image: str,
    flavor: str,
    network: str,
    key_name: Optional[str] = None,
    security_groups: Optional[List[str]] = None,
    wait: bool = True,
    timeout: int = 120
) -> Server:
    img = conn.compute.find_image(image, ignore_missing=False)
    flv = conn.compute.find_flavor(flavor, ignore_missing=False)
    net = conn.network.find_network(network, ignore_missing=False)

    server_kwargs = {
        "name": name,
        "image_id": img.id,
        "flavor_id": flv.id,
        "networks": [{"uuid": net.id}],
    }
    if key_name:
        server_kwargs["key_name"] = key_name
    if security_groups:
        server_kwargs["security_groups"] = [{"name": sg} for sg in security_groups]

    server = conn.compute.create_server(**server_kwargs)
    if wait:
        server = conn.compute.wait_for_server(server, wait=timeout)
    return server


def create_server_from_volume(
    conn: connection.Connection,
    name: str,
    image: str,
    flavor: str,
    network: str,
    key_name: Optional[str] = None,
    security_groups: Optional[List[str]] = None,
    wait: bool = True,
    timeout: int = 180
) -> Server:
    # Step 1: Find resources
    img = conn.compute.find_image(image, ignore_missing=False)
    flv = conn.compute.find_flavor(flavor, ignore_missing=False)
    net = conn.network.find_network(network, ignore_missing=False)

    print(f"🔄 Creating volume '{name}-volume' from image '{image}'...")
    volume = conn.block_storage.create_volume(
        size=40,
        name=f"{name}-volume",
        image_id=img.id
    )
    conn.block_storage.wait_for_status(volume, status='available')
    print(f"✅ Volume created: {volume.id}")

    print(f"🚀 Booting server '{name}' from volume...")
    server_kwargs = {
        "name": name,
        "flavor_id": flv.id,
        "networks": [{"uuid": net.id}],
        "block_device_mapping_v2": [{
            "boot_index": 0,
            "uuid": volume.id,
            "source_type": "volume",
            "destination_type": "volume",
            "delete_on_termination": True
        }]
    }

    if key_name:
        server_kwargs["key_name"] = key_name
    if security_groups:
        server_kwargs["security_groups"] = [{"name": sg} for sg in security_groups]

    server = conn.compute.create_server(**server_kwargs)
    if wait:
        server = conn.compute.wait_for_server(server, wait=timeout)
    return server



def interactive_create_server(conn: connection.Connection):
    print("\nVM Provisioning — please enter the following details:")
    name = input("1) VM name (e.g. dev-box): ").strip()
    image = input("2) Image name or ID (e.g. Almalinux9.5): ").strip()
    flavor = input("3) Flavor name or ID (e.g. S.64): ").strip()
    network = input("4) Network name or ID (e.g. External_Net_MUM): ").strip()
    key_name = input("5) SSH keypair name (press Enter to skip): ").strip() or None
    sg_input = input("6) Security groups (comma-separated, e.g. default,web; press Enter to skip): ").strip()
    security_groups = [s.strip() for s in sg_input.split(",")] if sg_input else None
    use_volume = input("7) Boot from volume instead of image? (y/n): ").strip().lower() == "y"

    try:
        if use_volume:
            server = create_server_from_volume(
                conn=conn,
                name=name,
                image=image,
                flavor=flavor,
                network=network,
                key_name=key_name,
                security_groups=security_groups,
            )
        else:
            server = create_server(
                conn=conn,
                name=name,
                image=image,
                flavor=flavor,
                network=network,
                key_name=key_name,
                security_groups=security_groups,
            )
    except Exception as e:
        print(f"❌ Failed to create VM: {e}")
        sys.exit(1)

    print(f"✅ Created VM '{server.name}' (ID={server.id}), Status={server.status}")


if __name__ == "__main__":
    conn = get_openstack_connection()
    conn.authorize()
    interactive_create_server(conn)

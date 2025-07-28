import docker
import os
import tarfile
import io
import time

WATCHED_CONTAINERS = os.getenv("WATCH_CONTAINERS", "").split(",")
CERT_DIR = "/certs"
TARGET_DIR = "/usr/local/share/ca-certificates/"

client = docker.from_env()

def make_tarball_of_certs(cert_dir):
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        for filename in os.listdir(cert_dir):
            if filename.endswith(".crt"):
                full_path = os.path.join(cert_dir, filename)
                tar.add(full_path, arcname=filename)
    tar_stream.seek(0)
    return tar_stream

def install_certs(container):
    try:
        print(f"Injecting CAs into container: {container.name}")

        tar_stream = make_tarball_of_certs(CERT_DIR)
        container.put_archive(TARGET_DIR, tar_stream)

        exec_log = container.exec_run("update-ca-certificates", stdout=True, stderr=True, user="root")
        print(exec_log.output.decode())

    except Exception as e:
        print(f"Error injecting certs into {container.name}: {e}")

def listen_to_events():
    print("Listening for container start events...")
    for event in client.events(decode=True):
        if event.get("Type") == "container" and event.get("Action") == "start":
            container_id = event["id"]
            try:
                container = client.containers.get(container_id)
                if container.name in WATCHED_CONTAINERS:
                    install_certs(container)
            except Exception as e:
                print(f"Failed to process container {container_id}: {e}")

def process_existing_containers():
    print("Checking existing containers...")
    for container in client.containers.list():
        if container.name in WATCHED_CONTAINERS:
            print(f"Container {container.name} already running — injecting certs")
            install_certs(container)

if __name__ == "__main__":
    process_existing_containers()
    while True:
        try:
            listen_to_events()
        except Exception as e:
            print(f"Listener crashed: {e}")
            time.sleep(5)

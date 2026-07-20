import subprocess
from pathlib import Path


class KubernetesSnapshotUploader:
    def __init__(self, namespace: str):
        self.namespace = namespace

    def log_info(self, message: str):
        print(f"[INFO] {message}")

    def log_success(self, message: str):
        print(f"[SUCCESS] {message}")

    def run_command(self, command: list[str], ignore_errors: bool = False):
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            if not ignore_errors:
                raise

    def upload_snapshot(
        self,
        local_file: str,
        pod_name: str,
        remote_path: str,
    ):
        self.log_info(
            f"Uploading snapshot: {local_file} -> {pod_name}:{remote_path}"
        )

        # Create remote directory
        remote_dir = str(Path(remote_path).parent)   # <<- from pathlib correct syntax 
        
        self.run_command(
            [
              "kubectl",
              "exec",
              "-n",
              self.namespace,
              pod_name,
              "--",
              "mkdir",
              "-p",
                remote_dir,
            ],
            ignore_errors=True,
        )

        # Copy file
        self.run_command(
            [
              "kubectl",
              "cp",
              local_file,
              f"{self.namespace}/{pod_name}:{remote_path}",
            ]
        )

        self.log_success("Snapshot uploaded")


if __name__ == "__main__":
    uploader = KubernetesSnapshotUploader(namespace="default")
    local_file = input("snapshot: ")
    pod_name = input("pod_name: ")
    remote_path = input("remote_path: ")

    uploader.upload_snapshot(
        local_file = local_file,
        pod_name = pod_name,
        remote_path = remote_path
    )


#wut?
import subprocess
from pathlib import Path

class SnapUploader:
    def __init__(self, namespace: str):
        self.namespace = namespace
    
    def log_info(self, message):
        print(f"[INFO] {message}")
    
    def log_success(self, message):
        print(f"[SUCCESS] {message}")
    
    def run_command(self, command: list[str], ignore_errors: bool = False):
        try:
          subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
          if not ignore_errors:
            raise

    def uploadsnap(
        self,
        pod: str,
        snap: str,
        dest: str
    ):
        self.log_info(
            f"Uploading {snap} to pod {pod} into {dest}"
        )

        #Create remote dir
        dest_path = str(Path(dest).parent)

        #Run upload command
        self.run_command(
            [
                "kubectl",
                "exec",
                "-n",
                self.namespace,
                pod,
                "--",
                "mkdir",
                "-p",
                dest_path,
            ],
            ignore_errors=True,
        )
        self.run_command(
            [
                "kubectl",
                "cp",
                snap,
                f"{self.namespace}/{pod}:{dest}"
            ]
            
            )
        self.log_success(
            f"The issue finished with success"
        )

if __name__ == "__main__":
    uploader = SnapUploader(namespace="default")
    snap = input("snapshot: ")
    pod = input("pod_name: ")
    dest = input("remote_path: ")

    uploader.uploadsnap(
        snap = snap,
        pod = pod,
        dest = dest
    )



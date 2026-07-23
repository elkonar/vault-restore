#SnapUploader
import subprocess
from pathlib import Path
import argparse

class SnapUploader:
    def __init__(self):
        pass
    
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
        namespace: str,
        pod: str,
        snap: str,
        dest: str
    ):
        self.log_info(
            f"Uploading {snap} to pod {pod} into {dest} in namespace {namespace}"
        )

        #Create remote dir
        dest_path = str(Path(dest).parent)

        #Run upload command
        self.run_command(
            [
                "kubectl",
                "exec",
                "-n",
                namespace,
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
                f"{namespace}/{pod}:{dest}"
            ],
            ignore_errors=True,
            
            )
        self.log_success(
            f"The issue finished with success"
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload snapshot")
    parser.add_argument("namespace", help="Namespace name")
    parser.add_argument("snap", help="Snapshot name")
    parser.add_argument("pod", help="Pod name")
    parser.add_argument("dest", help="Remote destination path")

    args = parser.parse_args()

    uploader = SnapUploader()

    uploader.uploadsnap(
        namespace=args.namespace,
        snap=args.snap,
        pod=args.pod,
        dest=args.dest
    )

# Usage example
# python3 SnapUploader.py fk-vault-raft-2026-04-29.snap fk-vault-0 /tmp/

#raft-restore.py

import subprocess
import argparse
from pathlib import Path
import logging

class raft_restore:
    def __init__(self):
        pass
    def log_info(self, message: str):
        print(f"[INFO] doing {message}")
    def log_success(self, message: str):
        print(f"[SUCCESS] { message}")
    def subpro_run(
        self,
        command: list[str],
        *,
        timeout: int | None = None,
        ignore_errors: bool = False,
    ) -> str:
    
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                timeout=timeout,
                text=True,
            )
        except subprocess.CalledProcessError as exec:
            if not ignore_errors:
                raise
            return "" 
    def raft_r(
        self,
        namespace: str,
        pod: str,
        dest: str,
    ):
        restore_path=str(Path(dest).parent)

        self.subpro_run(
            [ 
            "kubectl",
            "exec",
            "-n",
            namespace,
            pod,
            "--",
            "vault",
            "operator raft snapshot restore -force",
            restore_path,
            ],
            ignore_errors =True
        )
        self.log_success(
            f"Hurra!"
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("namespace", help="Namespace name")
    parser.add_argument("pod", help="Pod name")
    parser.add_argument("dest", help="Snap destination on remote pod")

    args = parser.parse_args()

    p = raft_restore()
    p.raft_r(
        namespace = args.namespace,
        pod = args.pod,
        dest = args.dest
    )
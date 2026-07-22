#vault-check.py

import subprocess
import argparse
import sys
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class raft_restore:
    def __init__(self):
        pass
    def log_info(self, message: str):
        print(f"[INFO] doing {message}")
    def log_success(self, message: str):
        print(f"[SUCCESS] because {message}")
    def subprocess_run(
        self,
        command: list[str],
        *,
        timeout: int | None = None,
        ignore_errors: bool = False,
    ): # -> str:

        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                timeout=timeout,
                text=True,
            )
            output = result.stdout
            return output
        except subprocess.CalledProcessError as exc:
            if exc.stdout:
                print(exc.stdout, end="")   # <<- end="" just removes last line
            if exc.stderr:
                print(exc.stderr, end="", file=sys.stderr)
                print("[WARNING] custom message")

            if ignore_errors:
                return    # <<- if variable ignore_errors is true return empty string
            print("[INFO] command failed for reasons")
            return None
    def raft_r(
        self,
        namespace: str,
        pod: str,
        dest: str,
    ):
        restore_path=str(Path(dest).parent)

        self.subprocess_run(
            [ 
            "kubectl",
            "exec",
            "-n",
            namespace,
            pod,
            "--",
            "vault",
            "status",   # "operator raft snapshot restore -force",
            #restore_path,
            #"/",
            ],
            ignore_errors = False
        )
        self.log_success("Hurra! everything went fine.")

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
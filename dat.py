# delete k resources
import subprocess
from pathlib import Path
import logging
import argparse

logger = logging.getLogger(__name__)    # <<- gdzie ten logger ma być?? tylko tu

class r_restore:
    def __init__(self):
        pass

    def log_info(self, message: str):
        print(f"[SUCCESS] {message}")

    def log_success(self, message: str):
        print(f"[SUCCESS] {message}")
    
    def run_command(
        self,
        flags: list[str],
        *,                  # <<- makes following parameters keyword-only, improves readability, not needed for this script
        timeout: int | None = None,   # <<- parameter can be an integer, default value none which equals 1, can be defined later ot left as is
        ignore_errors: bool = False,
    ) -> str:           # <<- return type annotation, this method should return a string   albo tylko ":"
        logger.info("Running: %s", " ".join(flags))

        try:
            result = subprocess.run(
                flags,
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            logger.error(
                "Command failed (%s): %s",
                exc.returncode,
                " ".join(flags),
            )
            if not ignore_errors:
                raise
            return ""
    
    def res_deleter(
        self,
        namespace: str,
        pod: str
    ):
        self.log_info(
            f"..deleting specified resource.."
        )
        self.run_command(
            [
                "kubectl",
                "delete",
                "pod",
                "-n",
                namespace,
                pod,
                "--ignore-not-found=true",
            ],
            ignore_errors=True,
        )
        self.run_command(
            [
                "kubectl",
                "get",
                "all"
            ],
            ignore_errors = True,
        )
        self.log_success(
            f"The issue finished with success"
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload snapshot")
    parser.add_argument("namespace", help="Namespace name")
    parser.add_argument("pod", help="Pod name")

    args = parser.parse_args()

    deleter = r_restore()

    deleter.res_deleter(
        namespace=args.namespace,
        pod=args.pod
    )



# delete k resources
import subprocess
from pathlib import Path

class r_restore:
    def __init__(self):
        pass

    def log_info(self, message: str):
        print(f"[SUCCESS] {message}")

    def log_success(self, message: str):
        print(f"[SUCCESS] {message}")
    
    def run_command(self, flags: list[str], ignore_errors: bool = False):
        try:
            subprocess.run(flags, check=True)
        except subprocess.CalledProcessError:
            if not ignore_errors:
                raise
    
    def res_deleter(
        self,
        namespace: str,
        pod: str,
        #job: str,
        #svc: str
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
                pod
            ]
        )
        self.run_command(
            [
                "kubectl",
                "get",
                "all"
            ]
        )
        self.log_info(
            f"all clear?"
        )

if __name__ == "__main__":
    remover = r_restore()
    namespace = input("namespace: ")
    pod = input("pod: ")
    
    remover.res_deleter(
        namespace = namespace,
        pod = pod
    )



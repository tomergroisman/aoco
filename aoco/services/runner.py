import subprocess


class RunnerService:
    @staticmethod
    def run(command: str):
        try:
            return subprocess.check_output(
                command,
                shell=True,
                executable="/bin/bash",
            ).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            print(e.output.decode('utf-8').strip())
            return None


    @staticmethod
    def run_python_script(filename: str, *args):
        script_args = " ".join(args)
        return RunnerService.run(f"python {filename} {script_args}")

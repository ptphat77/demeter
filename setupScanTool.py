import subprocess
import sys


def setupScanTool():
    subprocess.check_output(
        "docker rm --force oyentecon && docker run -d --name oyentecon -it luongnguyen/oyente sh",
        shell=True,
    )


sys.modules[__name__] = setupScanTool

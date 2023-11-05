import subprocess
import sys


def setupScanTool():
    # Setup oyente
    subprocess.check_output(
        """docker rm --force oyentecon && docker run -d --name oyentecon -it luongnguyen/oyente sh && docker cp ./oyenteDocker/oyente/symExec.py oyentecon:/oyente/oyente/symExec.py && docker cp ./oyenteDocker/oyente/oyente.py oyentecon:/oyente/oyente/oyente.py""",
        shell=True,
    )


sys.modules[__name__] = setupScanTool

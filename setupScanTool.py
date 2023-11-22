import subprocess
import sys


def setupScanTool(threadNo):
    # Setup oyente
    subprocess.check_output(
        f"docker rm --force oyenteContainer-{threadNo} && docker run -d --name oyenteContainer-{threadNo} -it luongnguyen/oyente sh && docker cp ./customCode/oyente/symExec.py oyenteContainer-{threadNo}:/oyente/oyente/symExec.py && docker cp ./customCode/oyente/oyente.py oyenteContainer-{threadNo}:/oyente/oyente/oyente.py",
        shell=True,
    )


sys.modules[__name__] = setupScanTool

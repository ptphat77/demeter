import subprocess
import sys


def setupScanTool():
    # Setup oyente
    subprocess.check_output(
        """docker rm --force oyentecon && docker run -d --name oyentecon -it luongnguyen/oyente sh && docker cp ./customCode/oyente/symExec.py oyentecon:/oyente/oyente/symExec.py && docker cp ./customCode/oyente/oyente.py oyentecon:/oyente/oyente/oyente.py""",
        shell=True,
    )

    # Setup maian
    # subprocess.check_output(
    #     """"""
    # )


sys.modules[__name__] = setupScanTool

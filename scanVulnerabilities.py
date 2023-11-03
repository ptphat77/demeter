import sys
import subprocess


def callOyente():
    label = False

    result = subprocess.check_output(
        "docker cp ./bytecode.txt oyentecon:/oyente/oyente/bytecode.txt && docker exec oyentecon python oyente/oyente.py -s /oyente/oyente/bytecode.txt -b -ce",
        shell=True,
    )

    result = result.decode("utf_8", "strict")

    label = "TRUE" in result

    return label


def scanVulnerabilities(originBytecode):
    with open("./bytecode.txt", "w") as file:
        file.write(originBytecode)

    oyenteLabel = callOyente()

    label = oyenteLabel

    return label


sys.modules[__name__] = scanVulnerabilities

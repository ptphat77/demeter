import sys
import subprocess


def callOyente():
    label = False

    result = subprocess.check_output(
        "docker cp ./bytecode.txt oyentecon:/oyente/oyente/bytecode.txt && docker exec oyentecon python oyente/oyente.py -s /oyente/oyente/bytecode.txt -b -ce",
        shell=True,
    )
    vulnerabilities = result.decode("utf_8", "strict")

    if vulnerabilities:
        label = True

    return {"vulnerabilities": vulnerabilities, "label": label}


def scanVulnerabilities(originBytecode):
    with open("./bytecode.txt", "w") as file:
        file.write(originBytecode)

    oyenteResult = callOyente()

    # Determine label
    label = oyenteResult["label"]

    # Merge all vulnerabilities
    vulnerabilities = oyenteResult["vulnerabilities"]

    if vulnerabilities == "":
        vulnerabilities = "None"
    else:
        # Remove ";" at the end of the string
        vulnerabilities = (
            vulnerabilities[:-1] if vulnerabilities[-1] == ";" else vulnerabilities
        )

    return {"vulnerabilities": vulnerabilities, "label": label}


sys.modules[__name__] = scanVulnerabilities

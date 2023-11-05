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


def callMythril():
    label = False

    vulnArr = [
        "Exception State",
        "Multiple Calls in a Single Transaction",
        "Unprotected Selfdestruct",
        "State access after external call",
        "Dependence on predictable environment variable",
        "External Call To User-Supplied Address",
        "Jump to an arbitrary instruction",
        "Unchecked return value from external call.",
        "Integer Arithmetic Bugs",
        "Write to an arbitrary storage location",
        "Delegatecall to user-supplied address",
        "Dependence on tx.origin",
        "Unprotected Ether Withdrawal",
    ]

    result = subprocess.check_output(
        "myth analyze -f bytecode.txt --execution-timeout 90",
        shell=True,
    )
    result = result.decode("utf_8", "strict")

    vulnerabilities = ""

    for vuln in vulnArr:
        if vuln in result:
            vulnerabilities += vuln + ";"

    if vulnerabilities:
        label = True

    return {"vulnerabilities": vulnerabilities, "label": label}


def scanVulnerabilities(originBytecode):
    with open("./bytecode.txt", "w") as file:
        file.write(originBytecode)

    # Scan vuln
    oyenteResult = callOyente()
    mythrilResult = callMythril()

    # Determine label
    label = oyenteResult["label"] or mythrilResult["label"]

    # Merge all vulnerabilities
    vulnerabilities = oyenteResult["vulnerabilities"] + mythrilResult["vulnerabilities"]

    if vulnerabilities == "":
        vulnerabilities = "None"
    else:
        # Remove ";" at the end of the string
        vulnerabilities = (
            vulnerabilities[:-1] if vulnerabilities[-1] == ";" else vulnerabilities
        )

    return {"vulnerabilities": vulnerabilities, "label": label}


sys.modules[__name__] = scanVulnerabilities

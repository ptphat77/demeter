import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor


# Run scan command && Extract vulnerbilities name
def scanAndExtractVuln(vulnArr, scanCommand, timeout, toolName):
    label = False
    vulnerabilities = ""
    result = ""

    try:
        result = subprocess.check_output(
            scanCommand,
            shell=True,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        result = result.decode("utf_8", "strict")

    except subprocess.CalledProcessError as grepexc:
        result = grepexc.output.decode("utf_8", "strict")
        print(
            ">>> {} error: ".format(toolName),
            grepexc.returncode,
            result,
        )

    for vuln in vulnArr:
        if vuln in result:
            vulnerabilities += vuln + ";"

    if vulnerabilities:
        label = True

    return {"vulnerabilities": vulnerabilities, "label": label}


def callOyente():
    vulnArr = [
        "Callstack Depth Attack Vulnerability",
        "Transaction-Ordering Dependence (TOD)",
        "Timestamp Dependency",
        "Re-Entrancy Vulnerability",
    ]

    subprocess.check_output(
        "docker cp ./bytecode.txt oyentecon:/oyente/oyente/bytecode.txt", shell=True
    )

    timeout = 90
    scanCommand = "docker exec oyentecon python oyente/oyente.py -s /oyente/oyente/bytecode.txt -b -ce --timeout {}".format(
        timeout
    )
    toolName = "Oyente"

    return scanAndExtractVuln(vulnArr, scanCommand, timeout * 2, toolName)


def callMythril():
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

    timeout = 900
    scanCommand = "myth analyze -f bytecode.txt --execution-timeout {}".format(timeout)
    Mythril = "Mythril"

    return scanAndExtractVuln(vulnArr, scanCommand, timeout * 2, Mythril)

def callMaian():
    vulnArr = [
        #file suicidal nó bị dính cái số 11111Suicidal
        "Suicidal",
        "Prodigal",
        "Greedy"
    ]

    timeout = 900
    scanCommand = "python3 mainan.py -b bytecode.txt -c 0 && python3 mainan.py -b bytecode.txt -c 1 && python3 mainan.py -b bytecode.txt -c 2  {}".format(timeout)
    Maian = "Maian"

    return scanAndExtractVuln(vulnArr, scanCommand, timeout * 2, Maian)

# Main function
def scanVulnerabilities(originBytecode):
    with open("./bytecode.txt", "w") as file:
        file.write(originBytecode)

    # Call scan function with multithreading
    threadNames = {"oyente": callMythril, "mythril": callOyente}

    with ThreadPoolExecutor() as executor:
        futures = {name: executor.submit(func) for name, func in threadNames.items()}

        threadResults = {name: future.result() for name, future in futures.items()}

    # Determine label
    labelSummary = threadResults["oyente"]["label"] or threadResults["mythril"]["label"]

    # Merge all vulnerabilities
    vulnerabilitiesSummary = (
        threadResults["oyente"]["vulnerabilities"]
        + threadResults["mythril"]["vulnerabilities"]
    )

    if vulnerabilitiesSummary == "":
        vulnerabilitiesSummary = "None"
    else:
        # Remove ";" at the end of the string
        vulnerabilitiesSummary = (
            vulnerabilitiesSummary[:-1]
            if vulnerabilitiesSummary[-1] == ";"
            else vulnerabilitiesSummary
        )

    return {
        "vulnerabilitiesSummary": vulnerabilitiesSummary,
        "labelSummary": labelSummary,
    }


sys.modules[__name__] = scanVulnerabilities

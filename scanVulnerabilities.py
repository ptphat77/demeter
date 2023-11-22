import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
from functools import partial


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
            f">>> {toolName} error: ",
            grepexc.returncode,
            result,
        )

    for vuln in vulnArr:
        if vuln in result:
            vulnerabilities += vuln + ";"

    if vulnerabilities:
        label = True

    return {"vulnerabilities": vulnerabilities, "label": label}


def callOyente(threadNo):
    vulnArr = [
        "Callstack Depth Attack Vulnerability",
        "Transaction-Ordering Dependence (TOD)",
        "Timestamp Dependency",
        "Re-Entrancy Vulnerability",
    ]

    subprocess.check_output(
        f"docker cp ./bytecode.txt oyenteContainer-{threadNo}:/oyente/oyente/bytecode.txt", shell=True
    )

    timeout = 90
    scanCommand = f"docker exec oyenteContainer-{threadNo} python oyente/oyente.py -s /oyente/oyente/bytecode.txt -b -ce --timeout {timeout}"
    toolName = "Oyente"

    return scanAndExtractVuln(vulnArr, scanCommand, timeout * 2, toolName)


def callMythril(threadNo):
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
    scanCommand = f"myth analyze -f bytecode.txt --execution-timeout {timeout}"
    Mythril = "Mythril"

    return scanAndExtractVuln(vulnArr, scanCommand, timeout * 2, Mythril)


# Main function
def scanVulnerabilities(originBytecode, threadNo):
    with open("./bytecode.txt", "w") as file:
        file.write(originBytecode)

    # Call scan function with multithreading
    threadNames = {"oyente": callMythril, "mythril": callOyente}

    with ThreadPoolExecutor() as executor:
        futures = {name: executor.submit(func, threadNo) for name, func in threadNames.items()}

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

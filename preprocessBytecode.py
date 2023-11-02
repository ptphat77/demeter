# All operations here: https://gavwood.com/paper.pdf
import sys


def preprocessBytecode(originBytecode):
    # PUSH2, PUSH32 => PUSH1
    preprocessedBytecode = originBytecode.replace("61", "60")
    preprocessedBytecode = preprocessedBytecode.replace("7f", "60")

    # DUP2, DUP16 => DUP1
    preprocessedBytecode = preprocessedBytecode.replace("81", "80")
    preprocessedBytecode = preprocessedBytecode.replace("8f", "80")

    # SWAP2, SWAP16 => SWAP1
    preprocessedBytecode = preprocessedBytecode.replace("91", "90")
    preprocessedBytecode = preprocessedBytecode.replace("9f", "90")

    # LOG1, LOG4 => LOG1
    preprocessedBytecode = preprocessedBytecode.replace("a1", "a0")
    preprocessedBytecode = preprocessedBytecode.replace("a4", "a0")

    return preprocessedBytecode


sys.modules[__name__] = preprocessBytecode

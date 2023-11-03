# All operations here: https://gavwood.com/paper.pdf
import sys

def replaceCommonOpcode(arr, opcode, desiredOpcode):
    for i, n in enumerate(arr): 
        if n == opcode:
            arr[i] = desiredOpcode
    return arr

def replaceInvalidOpcode(arr):
    InvalidBytecodeArr = [ "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0a", "0b", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1a", "1b", "1c", "1d", "20", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "3a", "3b", "3c", "3d", "3e", "3f", "40", "41", "42", "43", "44", "45", "46", "47", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "5a", "5b", "60", "80", "90", "a0", "f0", "f1", "f2", "f3", "f4", "f5", "fa", "fd", "fe", "ff"]
    for i, n in enumerate(arr): 
        if n not in InvalidBytecodeArr:
            arr[i] = "xx"
    return arr

def preprocessBytecode(originBytecode):
    preprocessedBytecode = originBytecode

    # Split bytecode
    preprBytecodeLen = len(preprocessedBytecode)
    lenSplit = 2
    preprBytecodeArray = [
        preprocessedBytecode[i : i + lenSplit]
        for i in range(0, preprBytecodeLen, lenSplit)
    ]

    # All PUSH => PUSH0
    PUSHArray = ["61", "62", "63", "64", "65", "66", "67", "68", "69", "6a", "6b", "6c", "6d", "6e", "6f", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "7a", "7b", "7c", "7d", "7e", "7f"] 
    for opcode in PUSHArray:
        preprBytecodeArray = replaceCommonOpcode(preprBytecodeArray, opcode, "60")

    # All DUP => DUP1
    DUPArray = ["81", "82", "83", "84", "85", "86", "87", "88", "89", "8a", "8b", "8c", "8d", "8e", "8f"]
    for opcode in DUPArray:
        preprBytecodeArray = replaceCommonOpcode(preprBytecodeArray, opcode, "80")

    # All SWAP => SWAP1
    SWAPArray = ["91", "92", "93", "94", "95", "96", "97", "98", "99", "9a", "9b", "9c", "9d", "9e", "9f"]
    for opcode in SWAPArray:
        preprBytecodeArray = replaceCommonOpcode(preprBytecodeArray, opcode, "90")

    # All LOG => LOG0
    LOGArray =  ["a1", "a2", "a3", "a4"]
    for opcode in LOGArray:
        preprBytecodeArray = replaceCommonOpcode(preprBytecodeArray, opcode, "a0")
    
    # Replace invalid bytecode with xx
    preprBytecodeArray = replaceInvalidOpcode(preprBytecodeArray)

    # Convert bytecodeArray to bytecodeString
    preprocessedBytecode = ''.join(str(e) for e in preprBytecodeArray)

    return preprocessedBytecode

sys.modules[__name__] = preprocessBytecode

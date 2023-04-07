#!/usr/bin/python3
import argparse
from lxml import etree
import xml.etree.ElementTree as ET
import sys


def log(s):
    if DEBUG:
        print("LOG: ", s)


DEBUG = False

parser = argparse.ArgumentParser(description='interpret')

parser.add_argument('--source', dest='source', type=str, help='source XML file')

parser.add_argument('--input', dest='input', type=str, help='file with inputs')

args = parser.parse_args()

sourceFile = str(args.source)
inputFile = str(args.input)
inputLines = []

if (sourceFile == "None" and inputFile == "None"):
    log("ERROR: --source or --input must be defined")
    exit(10)

try:
    if (sourceFile == "None"):
        log("reading source from stdin")
        tree = ET.parse(sys.stdin)
    else:
        log("source: " + sourceFile)
        tree = ET.parse(args.source)

except:
    log("Wrong XML format of source")
    exit(31)
if (inputFile == "None"):
    log("reading input from stdin")
    for line in sys.stdin:
        inputLines.append(line)
else:
    log("input: " + inputFile)
    file = open(inputFile, 'r')
    Lines = file.readlines()
    for line in Lines:
        inputLines.append(line)

root = tree.getroot()
orderNumbers = []

stack = []
varStorage = {}
output=""
outputErr=""

try:
    for element in root.findall("./instruction"):
        if (int(element.attrib["order"]) not in orderNumbers and int(element.attrib["order"]) >= 0):
            orderNumbers.append(int(element.attrib["order"]))
        else:
            raise
except:
    exit(32)
orderNumbers.sort()

for n in orderNumbers:
    try:
        # iterate throught XML based on order number
        element = root.find('.//instruction[@order="' + str(n) + '"]')
        opcode = element.attrib["opcode"].upper()

        # FRAMES
        if (opcode == "MOVE"):
            var = element.find('./arg1')
            symb = element.find('./arg2')

            if (symb.attrib["type"] == "var"):
                varStorage[var.text] = varStorage[symb.text]
            else:
                varStorage[var.text] = symb.text
            log("moving " + symb.text + " to " + var.text)
        elif (opcode == "CREATEFRAME"):
            log("CREATEFRAME not implemented", file=sys.stderr)
        elif (opcode == "PUSHFRAME"):
            log("PUSHFRAME not implemented", file=sys.stderr)
        elif (opcode == "POPFRAME"):
            log("POPFRAME not implemented", file=sys.stderr)
        elif (opcode == "DEFVAR"):
            variable = element.find('./arg1').text

            if (variable not in varStorage):
                varStorage[variable] = None
            else:
                exit(52)
            log("created variable: " + variable)

        elif (opcode == "CALL"):
            log("work in progres")
        elif (opcode == "RETURN"):
            log("work in progres")
            # STACK
        elif (opcode == "PUSHS"):
            toPush = element.find('./arg1')
            if (toPush.attrib["type"] == "string"):
                stack.append(toPush.text)
            elif (toPush.attrib["type"] == "int"):
                stack.append(int(toPush.text))
            else:
                log("PUSHS: wrong type")
                exit(53)
            log("pushing to stak: " + toPush.text)

        elif (opcode == "POPS"):
            variableName = element.find('./arg1').text
            if (len(stack) > 0):
                varStorage[variableName] = stack.pop()
            else:
                exit(56)

        # MATH Functions
        elif (opcode == "ADD"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')

            result = 0
            try:
                if (symb1.attrib["type"] == "var"):
                    result += int(varStorage[symb1.text])
                elif (symb1.attrib["type"] == "int"):
                    result += int(symb1.text)
                else:
                    raise Exception('wrong type')

                if (symb2.attrib["type"] == "var"):
                    result += int(varStorage[symb2.text])
                elif (symb2.attrib["type"] == "int"):
                    result += int(symb2.text)
                else:
                    raise Exception('wrong type')
            except:
                exit(53)
            varStorage[var.text] = result
            log(symb1.text + " + " + symb2.text + " = " + str(result))
        elif (opcode == "SUB"):
            log("sub")
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')

            result = 0
            try:
                if (symb1.attrib["type"] == "var"):
                    result += int(varStorage[symb1.text])
                elif (symb1.attrib["type"] == "int"):
                    result += int(symb1.text)
                else:
                    raise Exception('wrong type')

                if (symb2.attrib["type"] == "var"):
                    result -= int(varStorage[symb2.text])
                elif (symb2.attrib["type"] == "int"):
                    result -= int(symb2.text)
                else:
                    raise Exception('wrong type')
            except:
                exit(53)
            varStorage[var.text] = result
            log(symb1.text + " - " + symb2.text + " = " + str(result))
        elif (opcode == "MUL"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')

            result = 0
            try:
                if (symb1.attrib["type"] == "var"):
                    result += int(varStorage[symb1.text])
                elif (symb1.attrib["type"] == "int"):
                    result += int(symb1.text)
                else:
                    raise Exception('wrong type')

                if (symb2.attrib["type"] == "var"):
                    result *= int(varStorage[symb2.text])
                elif (symb2.attrib["type"] == "int"):
                    result *= int(symb2.text)
                else:
                    raise Exception('wrong type')
            except:
                exit(53)
            result = int(result)
            varStorage[var.text] = result
            log(symb1.text + " * " + symb2.text + " = " + str(result))
        elif (opcode == "IDIV"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')

            result = 0
            try:
                if (symb1.attrib["type"] == "var"):
                    result += int(varStorage[symb1.text])
                elif (symb1.attrib["type"] == "int"):
                    result += int(symb1.text)
                else:
                    raise Exception('wrong type')

                if (symb2.text == "0"):
                    exit(57)
                elif (symb2.attrib["type"] == "var"):
                    result /= int(varStorage[symb2.text])
                elif (symb2.attrib["type"] == "int"):
                    result /= int(symb2.text)
                else:
                    raise Exception('wrong type')
            except:
                exit(53)
            result = int(result)
            varStorage[var.text] = result
            log(symb1.text + " / " + symb2.text + " = " + str(result))
        elif (opcode == "LT"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')
            try:
                if (symb1.attrib["type"] == symb2.attrib["type"]):
                    if (symb1.attrib["type"] == "int"):
                        varStorage[var.text] = int(
                            symb1.text) < int(symb2.text)
                    elif (symb1.attrib["type"] == "var"):
                        varStorage[var.text] = varStorage[symb1.text] < varStorage[symb2.text]
                    elif (symb1.attrib["type"] == "string"):
                        varStorage[var.text] = symb1.text < symb2.text
                    elif (symb1.attrib["type"] == "bool"):
                        varStorage[var.text] = bool(
                            symb1.text) < bool(symb2.text)
                else:
                    raise Exception('wrong type')
            except:
                exit(53)
            log(symb1.text + " < " + symb2.text +
                " => " + str(varStorage[var.text]))
        elif (opcode == "GT"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')
            try:
                if (symb1.attrib["type"] == symb2.attrib["type"]):
                    if (symb1.attrib["type"] == "int"):
                        varStorage[var.text] = int(
                            symb1.text) > int(symb2.text)
                    elif (symb1.attrib["type"] == "var"):
                        varStorage[var.text] = varStorage[symb1.text] > varStorage[symb2.text]
                    elif (symb1.attrib["type"] == "string"):
                        varStorage[var.text] = symb1.text > symb2.text
                    elif (symb1.attrib["type"] == "bool"):
                        varStorage[var.text] = bool(
                            symb1.text) > bool(symb2.text)
                else:
                    raise Exception('wrong type')
            except:
                exit(53)
            log(symb1.text + " > " + symb2.text +
                " => " + str(varStorage[var.text]))
        elif (opcode == "EQ"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')
            try:
                if (symb1.attrib["type"] == symb2.attrib["type"]):
                    if (symb1.attrib["type"] == "int"):
                        varStorage[var.text] = int(
                            symb1.text) == int(symb2.text)
                    elif (symb1.attrib["type"] == "var"):
                        varStorage[var.text] = varStorage[symb1.text] == varStorage[symb2.text]
                    elif (symb1.attrib["type"] == "string"):
                        varStorage[var.text] = symb1.text == symb2.text
                    elif (symb1.attrib["type"] == "bool"):
                        varStorage[var.text] = bool(
                            symb1.text) == bool(symb2.text)
                else:
                    raise Exception('wrong type')
            except:
                exit(53)
            log(symb1.text + " == " + symb2.text +
                " => " + str(varStorage[var.text]))
        elif (opcode == "AND"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')
            try:
                if (symb1.attrib["type"] == "var"):
                    symb1 = bool(varStorage[symb1.text])
                elif (symb1.attrib["type"] == "bool"):
                    symb1 = bool(symb1.text)
                else:
                    raise Exception('wrong type')

                if (symb2.attrib["type"] == "var"):
                    symb2 = bool(varStorage[symb2.text])
                elif (symb1.attrib["type"] == "bool"):
                    symb2 = bool(symb2.text)
                else:
                    raise Exception('wrong type')

                varStorage[var.text] = symb1 and symb2
            except:
                exit(53)
            log(symb1 + " and " + symb2 +
                " => " + str(varStorage[var.text]))
        elif (opcode == "OR"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')
            try:
                if (symb1.attrib["type"] == "var"):
                    symb1 = bool(varStorage[symb1.text])
                elif (symb1.attrib["type"] == "bool"):
                    symb1 = bool(symb1.text)
                else:
                    raise Exception('wrong type')

                if (symb2.attrib["type"] == "var"):
                    symb2 = bool(varStorage[symb2.text])
                elif (symb1.attrib["type"] == "bool"):
                    symb2 = bool(symb2.text)
                else:
                    raise Exception('wrong type')

                varStorage[var.text] = symb1 or symb2
            except:
                exit(53)
            log(symb1 + " or " + symb2 + " => " +
                str(varStorage[var.text]))
        elif (opcode == "NOT"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            try:
                if (symb1.attrib["type"] == "var"):
                    symb1 = bool(varStorage[symb1.text])
                elif (symb1.attrib["type"] == "bool"):
                    symb1 = bool(symb1.text)
                else:
                    raise Exception('wrong type')

                varStorage[var.text] = not symb1
            except:
                exit(53)
            log(" not " + symb1 + " => " + varStorage[var.text])
        elif (opcode == "INT2CHAR"):
            var = element.find('./arg1')
            symb = element.find('./arg2')
            try:
                if (symb.attrib["type"] == "var"):
                    varStorage[var.text] = chr(int(varStorage[symb.text]))
                else:
                    varStorage[var.text] = chr(int(symb.text))
            except:
                exit(58)
            log("converting " + str(varStorage[symb.text]) +
                " to " + str(varStorage[var.text]))

        elif (opcode == "STRI2INT"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')

            try:
                result = list(varStorage[var.text])
                index = int(symb2.text)

                if (symb1.attrib["type"] == "var"):
                    result[index] = ord(varStorage[symb1.text])
                else:
                    result[index] = ord(symb.text)

                varStorage[var.text] = ''.join(result)

            except:
                exit(58)
            log("converting " + str(varStorage[symb.text]) +
                " to " + str(varStorage[var.text]))
            # INPUT / OUTPUT
        elif (opcode == "READ"):
            var = element.find('./arg1').text
            typ = element.find('./arg2').text

            readedValue = inputLines.pop(0)

            if (typ == "int"):
                varStorage[var] = int(readedValue)
            elif (typ == "bool"):
                if(upper(readedValue) == "TRUE"):
                    varStorage[var] = True
                else:
                    varStorage[var] = False
            elif (typ == "string"):
                varStorage[var] = readedValue
            else:
                exit(53)

            log("Reading value: " +
                str(varStorage[var]) + " to variable: " + var)

        elif (opcode == "WRITE"):
            symb = element.find('./arg1')

            if (symb.text == "nil@nil"):
                symb.text = ""
            elif (symb.attrib["type"] == "var"):
                output+=str(varStorage[symb.text])
            else:
                output+=symb.text
            # RETAZCE
        elif (opcode == "CONCAT"):
            var = element.find('./arg1')
            symb1 = element.find('./arg2')
            symb2 = element.find('./arg3')

            result = ""
            try:
                if (symb1.attrib["type"] == "var"):
                    result += str(varStorage[symb1.text])
                else:
                    result += symb1.text

                if (symb2.attrib["type"] == "var"):
                    result += str(varStorage[symb2.text])
                else:
                    result += symb2.text
            except:
                exit(53)
            varStorage[var.text] = result
            log(symb1.text + " concatenate " + symb2.text + " = " + result)
        elif (opcode == "STRLEN"):
            var = element.find('./arg1').text
            symb = element.find('./arg2').text

            varStorage[var] = len(str(symb))

            log("length of " + symb + " is " + varStorage[var])

        elif (opcode == "GETCHAR"):
            var = element.find('./arg1').text
            symb1 = element.find('./arg2').text
            symb2 = element.find('./arg3').text

            try:
                strToList = list(symb1)
                oneChar = strToList[int(symb2)]
                varStorage[var] = ''.join(oneChar)
            except:
                exit(58)
            log("getchar " + str(oneChar) + " from " + symb1)

        elif (opcode == "SETCHAR"):
            var = element.find('./arg1').text
            symb1 = element.find('./arg2').text
            symb2 = element.find('./arg3').text

            try:
                strToList = list(varStorage[var])
                strToList[int(symb1)] = symb2[0]
                varStorage[var] = ''.join(strToList)
            except:
                exit(58)
            log("setchar " + symb2[0] + " to " + str(varStorage[var]))
            # TYPES
        elif (opcode == "TYPE"):
            var = element.find('./arg1').text
            symb = element.find('./arg2')

            if (symb.attrib["type"] == "var"):
                varStorage[var] = "var"
            elif (symb.attrib["type"] == "int"):
                varStorage[var] = "int"
            if (symb.attrib["type"] == "bool"):
                varStorage[var] = "bool"
            elif (symb.attrib["type"] == "string"):
                varStorage[var] = "string"
            else:
                varStorage[var] = ""
            log("type of " + symb.text + " is " + str(varStorage[var]))
            # FLOW CONTROL
        elif (opcode == "LABEL"):
            log("LABEL not implemented", file=sys.stderr)
        elif (opcode == "JUMP"):
            log("JUMP not implemented", file=sys.stderr)
        elif (opcode == "JUMPIFEQ"):
            log("JUMPIFEQ not implemented", file=sys.stderr)
        elif (opcode == "JUMPIFNEQ"):
            log("JUMPIFNEQ not implemented", file=sys.stderr)
        elif (opcode == "EXIT"):
            symb = element.find('./arg1').text
            try:
                returnCode = int(symb)
                if (returnCode <= 49 and returnCode >= 0):
                    exit(returnCode)
                else:
                    raise Exception('wrong number')
            except:
                exit(57)

            # DEBUG
        elif (opcode == "DPRINT"):
            symb = element.find('./arg1').text
            if (symb in varStorage):
                outputErr+=str(varStorage[symb])
            else:
                outputErr+=symb
        elif (opcode == "BREAK"):
            output+="stored variables: \n", varStorage, "\nstack: \n", stack
        else:
            log("\nunknown opcode: " + opcode)
            exit(32)
    except Exception as e:
        log(e)
        exit(32)

if len(output) > 0:
    print(output)
if len(outputErr) > 0:
    print(outputErr, file=sys.stderr)

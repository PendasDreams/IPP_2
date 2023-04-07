#!/usr/bin/env python3
# author: Denis Novosád
# login : xnovos14

import re
import argparse
import os
import sys
import xml.etree.ElementTree as ET
from enum import IntEnum, Enum



# dictionary with specific types of arguments for each instruction 
# this part is also implemented in parser / syntactic check
instruction_arguments_types = {
    'CREATEFRAME' :  [None, None, None],'PUSHFRAME':[None, None, None],'POPFRAME':[None, None, None],'RETURN':[None, None, None],'BREAK':[None, None, None],
    'DEFVAR': ['VAR', None, None],'POPS': ['VAR', None, None],'CALL': ['LABEL', None, None],
    'LABEL': ['LABEL', None, None],'JUMP': ['LABEL', None, None],'PUSHS': ['SYMB', None, None],
    'WRITE': ['SYMB', None, None],'EXIT': ['SYMB', None, None],'DPRINT': ['SYMB', None, None],
    'MOVE': ['VAR', 'SYMB', None],'INT2CHAR': ['VAR', 'SYMB', None],'STRLEN': ['VAR', 'SYMB', None],
    'TYPE': ['VAR', 'SYMB', None],'READ': ['VAR', 'TYPE', None],'NOT': ['VAR', 'SYMB', None],
    'ADD': ['VAR', 'SYMB', 'SYMB'],'SUB': ['VAR', 'SYMB', 'SYMB'],
    'MUL': ['VAR', 'SYMB', 'SYMB'],'IDIV': ['VAR', 'SYMB', 'SYMB'],
    'LT': ['VAR', 'SYMB', 'SYMB'],'GT': ['VAR', 'SYMB', 'SYMB'],
    'EQ': ['VAR', 'SYMB', 'SYMB'],'JUMPIFEQ': ['VAR', 'SYMB', 'SYMB'],
    'JUMPIFNEQ': ['VAR', 'SYMB', 'SYMB'],'OR': ['VAR', 'SYMB', 'SYMB'],
    'AND': ['VAR', 'SYMB', 'SYMB'],'STRI2INT': ['VAR', 'SYMB', 'SYMB'],
    'CONCAT': ['VAR', 'SYMB', 'SYMB'],'GETCHAR': ['VAR', 'SYMB', 'SYMB'],
    'SETCHAR': ['VAR', 'SYMB', 'SYMB'],
}


# dictionary with keys which represents number of arguments for each instruction which are displayed in the dictonary as values 
# this part is also implemented in parser / syntactic check
instructionNumOfArguments = {
    0 : ('PUSHFRAME','POPFRAME', 'RETURN','CREATEFRAME', 'BREAK'),
    1 : ('DEFVAR', 'POPS', 'CALL', 'LABEL', 'JUMP', 'PUSHS', 'WRITE', 'EXIT', 'DPRINT'),
    2 : ('MOVE', 'INT2CHAR', 'STRLEN', 'TYPE', 'READ',  'NOT'),
    3 : ('ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'JUMPIFEQ', 'JUMPIFNEQ', 'OR', 'AND', 'STRI2INT', 'CONCAT', 'GETCHAR', 'SETCHAR')
}   


class Val(Enum):
    NIL = 'nil'

class Var(IntEnum):
    VALUE = 0   
    TYPE = 1

# Data structures and important variables
instruction_counter = 0  # loop counter
number_of_local_frames = 0  # number of Local Frames
is_temp_frame_created = False
exists_temp_frame = False
is_eof = False
temp_dict = {}  # dictionary used for swapping variables between var_list and var_stack
var_list = {}  # dictionary for all available variables
label_list = {}
data_stack = []  # stack used by instructions PUSHS and POPS
call_stack = []  # stack used by instructions CALL and RETURN
var_stack = []  # stack for LF variables which are currently not available
sorted_ins = []


class ProgramArgs:
    # this class takes care of program arguments, their parsing and checks correctness

    def __init__(self):
        self.inputToBeExecuted = None
        self._parser = None
        self._arguments = None
        self.inputToBeRead = None
        self.sourceBool = False
        self.inputBool = False
    
    def executeProgramParams(self):
        self.parseProgramsArgumets()
        self.checkProgramArguments()
        self.checkProgramsArgumentsPath()
    
    def parseProgramsArgumets(self):
    # parses arguments with argParse
        if '--help' in sys.argv and len(sys.argv) > 2: exit(10)
        if '-h' in sys.argv and len(sys.argv) > 2: exit(10)
        self._parser = argparse.ArgumentParser(description="IPP/2023 Interpret")
        self._parser.add_argument("--source",  action="store", dest="source")
        self._parser.add_argument("--input", action="store", dest="input")
        self._arguments = self._parser.parse_args()

    
    def checkProgramsArgumentsPath(self):
    # this method is checking the existence of file(s)

        isExists = None
        if self.sourceBool:
            isExists = os.path.exists(self._arguments.source)
            if not isExists:
                exit(11)
        if self.inputBool:
            isExists = os.path.exists(self._arguments.input)
            if not isExists:
                exit(11)

        
    def checkProgramArguments(self):
    # checks if user entered correct arguments

        if self._arguments.source == None and self._arguments.input == None:
           pass #exit(10)
        elif self._arguments.source != None and self._arguments.input == None:
            self.inputToBeExecuted = self._arguments.source
            self.inputToBeRead = sys.stdin
            self.sourceBool = True
        elif self._arguments.source == None and self._arguments.input != None:
            self.inputToBeExecuted = sys.stdin
            self.inputToBeRead = open(self._arguments.input, "r")
            self.inputBool = True
        elif self._arguments.source != None and self._arguments.input != None:
            self.inputToBeExecuted = self._arguments.source
            self.inputToBeRead = open(self._arguments.input, "r")
            self.sourceBool, self.inputBool = True, True

class Instruction:
    def __init__(self, opcode, num, args):
        self._opcode = opcode
        self._num = num
        self._type = str
        self.arg1, self.arg2, self.arg3 = None, None, None

        self.check_opcode()

        if len(args) >= 1:
            self.arg1 = Argument(1, args[0].get('type').upper(), args[0].text)
        if len(args) >= 2:
            self.arg2 = Argument(2, args[1].get('type').upper(), args[1].text)
        if len(args) == 3:
            self.arg3 = Argument(3, args[2].get('type').upper(), args[2].text)

        if self.arg1:
            self.arg1.check()
        if self.arg2:
            self.arg2.check()
        if self.arg3:
            self.arg3.check()

    def get_opcode(self):
        return self._opcode

    def check_opcode(self):
        if self._opcode not in instructionNumOfArguments[self._num]:
            exit(32)

class Argument:
    def __init__(self, num, typ: str, value):
        self._num = num
        self._typ = typ
        self._value = value

    def getValue(self):
        return self._value
    
    def getType(self):
        return self._typ

    def checkArgumentsType(self,typ):
        if typ == self._typ or typ == 'VAR':
            pass
        elif typ == "SYMB" and self._typ in ('VAR', 'INT', 'STRING', 'BOOL', 'NIL'):
            pass
        elif typ == "TYPE" and self._typ in ("int", "string", "bool"):
            pass
        elif typ == 'LABEL' and self._typ == 'LABEL':
            pass
        else:
            exit(53)
           
    def check(self):
        """ Checks arguments - if variable is defined properly (in existing frame), undefined
        variables, in case we are going read from variables so they are not uninitializated. 
        Escape sequentions, type conversions. 
        """

        self.checkArgumentsType(instruction_arguments_types[insOpCode][self._num-1])
        if self._typ == 'VAR' and not insOpCode == 'DEFVAR':
            if     self._value.startswith('TF') and not exists_temp_frame  : exit(55)
            if     self._value.startswith('LF') and     number_of_local_frames == 0 : exit(55)
            if not self._value in var_list: exit(54)
            self._varName = self._value
            if not self._num == 1:
                self._typ   = var_list[self._value][Var.TYPE]
                self._value = var_list[self._value][Var.VALUE]
        self.checkTypeConversion()
        self.replaceEscapeSequences()
        if self._value  == None and insOpCode != 'TYPE': exit(56)

    def replaceEscapeSequences(self):
        """ This method looks for escape sequences by regex. It saves them into an array 'x'.
        Then it converts them to integers and by chr() function replaces these escape sequences
        by their queal representation in ASCII. If the string is empty this method is not performed.
        """

        if self._typ == 'STRING' and self._value != None:
            x = re.findall(r"\\[0-9]{3}", self._value)
            x = [string[1:] for string in x]
            x = list(map(int, x))
            for escSeq in x:
                toReplace = '\\0' + str(escSeq)
                self._value = self._value.replace(toReplace, chr(escSeq))
        elif self._typ == 'STRING' and self._value == None:
            self._value = ''
    
    def checkTypeConversion(self):
        """ Converts string represented values into their real types """

        if self._typ == 'INT':
            try: 
                self._value = int(self._value)
            except: 
                exit(32)
        elif self._typ == 'BOOL':
            if self._value == True or self._value== 'true':
                self._value = True
            else:
                self._value =   False
        elif self._typ == 'NIL':
            self._value = Val.NIL
        else :
            return

class Program:
    
    sorted_ins = []
    def __init__(self, treeToBeParsed):
        if os.stat(treeToBeParsed).st_size == 0:
            exit(0)
        try:
            self._tree = ET.parse(treeToBeParsed)
        except ET.ParseError:
            exit(31)
        self._root = self._tree.getroot()
    
    def executeProgram(self):
        self.checkStructionOfXMLTree()
        self.orderInstructions()
        self.findLabels()

    def checkStructionOfXMLTree(self):
        """ Checks the representation of XML tree. It goes intruction by instruction and
        their arguments and checks their tags and atributtes. If anything fails, the exit
        is called. """

        try:
            for ins in self._root:
                assert ins.tag == 'instruction'
                assert ins.attrib['opcode']  
                assert ins.attrib['order'] 
                numOfArgs = 0 
                for arg in ins:
                    assert re.match(r"^arg[1-3]$", arg.tag)
                    assert arg.attrib['type']
                    numOfArgs = numOfArgs + 1
            assert self._root.tag == 'program'
            assert self._root.attrib['language']        
            assert self._root.get('language') == 'IPPcode23'
        except:
            exit(32)

    def orderInstructions(self):
        """ Sorts instructions with lambda function by their order. It looks for duplicated orders 
        and non-positive values. """

        try:
            sorted_ins[:] = sorted(self._root, key=lambda child: (child.tag,int(child.get('order'))))
            duplicatedOrderds = []
            for ins in sorted_ins:
                num = int(ins.get('order'))
                duplicatedOrderds.append(num)
                if num < 1: exit(32) # detects non-positive order numbers
            if not len(duplicatedOrderds) == len(set(duplicatedOrderds)): exit(32) # detects duplication of order numbers
        except:
            exit(32)

    def findLabels(self):
        """ Looks for labels and checks their uniqueness. """

        cycle = 0
        for ins in self._root:
            if ins.get('opcode') == 'LABEL':
                if ins[0].text in label_list:
                    exit(52)
                label_list[ins[0].text] = cycle
            cycle = cycle + 1

#### PROGRAM STARTS EXECUTING HERE ####
if __name__ == "__main__":
    argParse = ProgramArgs()
    argParse.executeProgramParams()
    program = Program(argParse.inputToBeExecuted)
    program.executeProgram()

    # main loop executing instructions
    while True:
        # tries to load new instruction and execute it, otherwise throws exit(0)
        try:    
            r = sorted_ins[instruction_counter]
        except: 
            exit(0)

        temp_dict = {} # used for swapping variables between var_stack and var_list
        insOpCode  = r.get('opcode').upper() # obtains current instruction's operation code
        rootLength = len(sorted_ins[instruction_counter]) # num of arguents
        arg = []
        arg[:] = sorted(r,key=lambda x: x.tag) # sorts arguments by their tags
        ins = Instruction(insOpCode, rootLength, arg)

        if ins.arg1:
            valueArg1 = ins.arg1.getValue()
            typeArg1  = ins.arg1.getType()
        if ins.arg2:
            valueArg2 = ins.arg2.getValue()
            typeArg2  = ins.arg2.getType()
        if ins.arg3:
            valueArg3 = ins.arg3.getValue()
            typeArg3  = ins.arg3.getType()
        
        # **** (INSTRUCTIONS EXECUTION) ****
        # **** Working with Frames, Functions Calls ****
        # MOVE
        if insOpCode == 'MOVE':
            var_list[valueArg1][Var.VALUE] = valueArg2
            var_list[valueArg1][Var.TYPE]  = typeArg2
        
        # CREATEFRAME
        elif insOpCode == 'CREATEFRAME':
            if exists_temp_frame: # deletes variables in current TF if it already exists
                [var_list.pop(var) for var in list(var_list.keys()) if var.startswith('TF')]
            is_temp_frame_created = True 
            exists_temp_frame = True

        # PUSHFRAME
        elif insOpCode == "PUSHFRAME":
            if not is_temp_frame_created: exit(55) # Undefined frame
            number_of_local_frames += 1

            # if any LF now exists push its values to the stack and make them not available for usage
            for var in list(var_list.keys()):
                if var.startswith('LF'):
                    temp_dict[var] = var_list.pop(var)
            var_stack.append(temp_dict)

            # change every current TF to LF
            for var in list(var_list.keys()):
                newKey = var.replace('TF', 'LF')
                var_list[newKey] =  var_list.pop(var)
        
            IsTempFrameCreated = False
            exists_temp_frame = False 
            
        # POPFRAME
        elif insOpCode == "POPFRAME":
            if number_of_local_frames == 0: exit(55)
            if exists_temp_frame == True: # deletes variables in current TF if it already exists
                [var_list.pop(var) for var in list(var_list.keys()) if var.startswith('TF')]

            # moves current LF values to TF 
            for var in list(var_list.keys()):
                newKey = var.replace('LF', 'TF')
                var_list[newKey] = var_list.pop(var)

            # moves variables from stack to current LF, if any exists
            var_list.update(var_stack.pop())
            
            number_of_local_frames -= 1
            IsTempFrameCreated = True
            exists_temp_frame = True
    
        # DEFVAR 
        elif insOpCode == 'DEFVAR':
            if  valueArg1 in var_list: exit(52) 
            if  valueArg1.startswith('TF') and exists_temp_frame:
                var_list[valueArg1] = [None, None]
            elif valueArg1.startswith('LF') and not number_of_local_frames == 0:
                var_list[valueArg1] = [None, None]
            elif valueArg1.startswith('GF'):
                var_list[valueArg1] = [None , None]
            else: 
                exit(55)           

        # CALL
        elif insOpCode == 'CALL':
            if not valueArg1 in label_list: exit(52)
            call_stack.append(instruction_counter)
            instruction_counter = label_list[valueArg1] 

        # RETURN
        elif insOpCode == 'RETURN':
            if not call_stack: exit(56) 
            instruction_counter = call_stack.pop()

        # **** Working with the data stack ****
        # PUSHS
        elif insOpCode == 'PUSHS':
            if typeArg1 == 'VAR':
                valueVar = var_list[valueArg1][Var.VALUE]
                if valueVar == None: exit(56)
                data_stack.append([valueArg1, typeArg1])
            else:
                data_stack.append([valueArg1, typeArg1])

        # POPS 
        elif insOpCode == 'POPS':           
            if not data_stack: exit(56) 
            poppedData = data_stack.pop()
            var_list[valueArg1][Var.VALUE] = poppedData[Var.VALUE]
            var_list[valueArg1][Var.TYPE]  = poppedData[Var.TYPE]

        # **** Arithmetic, relational, Boolean and conversion instructions ****
        # ADD, SUB, MUL, IDIV
        elif insOpCode in ('ADD', 'SUB', 'MUL', 'IDIV'):  
            if typeArg2 != 'INT' or typeArg3 != 'INT': exit(53)
            if   insOpCode == 'ADD':
                var_list[valueArg1][Var.VALUE] = valueArg2 + valueArg3
            elif insOpCode == 'SUB':
                var_list[valueArg1][Var.VALUE] = valueArg2 - valueArg3
            elif insOpCode == 'MUL':
                var_list[valueArg1][Var.VALUE] = valueArg2 * valueArg3
            elif insOpCode == 'IDIV':
                if valueArg3 == 0: exit(57)
                var_list[valueArg1][Var.VALUE] = int(valueArg2 / valueArg3)
            var_list[valueArg1][Var.TYPE] = 'INT'

        # LT, GT, EQ
        elif insOpCode in ('LT', 'GT', 'EQ'):
            if insOpCode == 'LT':
                if typeArg2 == 'NIL' or typeArg3 == 'NIL': exit(53)
                if typeArg2 != typeArg3: exit(53)
                if valueArg2 < valueArg3:
                    var_list[valueArg1][Var.VALUE] = True
                else:
                    var_list[valueArg1][Var.VALUE] = False
            
            elif insOpCode == 'GT':
                if typeArg2 == 'NIL' or typeArg3 == 'NIL': exit(53)
                if typeArg2 != typeArg3: exit(53)
                if valueArg2 > valueArg3:
                    var_list[valueArg1][Var.VALUE] = True
                else:
                    var_list[valueArg1][Var.VALUE] = False
            
            elif insOpCode == 'EQ':
                if typeArg2 != typeArg3:
                    if typeArg2 == 'NIL' or typeArg3 == 'NIL':
                        pass
                    else:
                        exit(53)     
                if valueArg2 == valueArg3:
                    var_list[valueArg1][Var.VALUE] = True
                else:
                    var_list[valueArg1][Var.VALUE] = False
            var_list[valueArg1][Var.TYPE] = 'BOOL'

        # AND, OR, NOT
        elif insOpCode in ('AND', 'OR', 'NOT'):
            if typeArg2 != 'BOOL': exit(53)
            if insOpCode == 'NOT':
                if   valueArg2 == False:
                    var_list[valueArg1][Var.VALUE] = True
                elif valueArg2 == True:
                    var_list[valueArg1][Var.VALUE] = False
            else:
                if typeArg3 != 'BOOL': exit(53)
                if insOpCode == 'AND':
                    if   valueArg2 == False and valueArg3 == False:
                        var_list[valueArg1][Var.VALUE] = False
                    elif valueArg2 == False and valueArg3 == True:
                        var_list[valueArg1][Var.VALUE] = False
                    elif valueArg2 == True  and valueArg3 == False:
                        var_list[valueArg1][Var.VALUE] = False
                    elif valueArg2 == True  and valueArg3 == True:
                        var_list[valueArg1][Var.VALUE] = True
                if insOpCode == 'OR':
                    if   valueArg2 == False and valueArg3 == False:
                        var_list[valueArg1][Var.VALUE] = False
                    elif valueArg2 == False and valueArg3 == True:
                        var_list[valueArg1][Var.VALUE] = True
                    elif valueArg2 == True  and valueArg3 == False:
                        var_list[valueArg1][Var.VALUE] = True
                    elif valueArg2 == True  and valueArg3 == True:
                        var_list[valueArg1][Var.VALUE] = True       
            var_list[valueArg1][Var.TYPE] = 'BOOL'    

        # INT2CHAR
        elif insOpCode == 'INT2CHAR': 
            if typeArg2 != 'INT': exit(53)
            if not 0 < valueArg2 < 256: exit(58)
            var_list[valueArg1][Var.VALUE] = chr(valueArg2)
            var_list[valueArg1][Var.TYPE]  = 'STRING'
        
        # STRI2INT
        elif insOpCode == 'STRI2INT':
            if typeArg2 != 'STRING' or typeArg3 != 'INT': exit(53)
            if not 0 < valueArg3 < len(valueArg2): exit(58)
            var_list[valueArg1][Var.VALUE] = ord(valueArg2[valueArg3])
            var_list[valueArg1][Var.TYPE]  = 'INT'
        
        # **** I/O Instructions ****
        # READ
        elif insOpCode == 'READ':
            typeArg2 = (arg[1].text).upper()
            inputValue = argParse.inputToBeRead.readline() 
            if not inputValue: is_eof = True
            if is_eof == False and inputValue[-1] == '\n':
                inputValue = inputValue[:-1] # cuts the newline  
            if typeArg2 == 'BOOL':
                if inputValue.lower() == 'true':
                    var_list[valueArg1][Var.VALUE] = True
                    var_list[valueArg1][Var.TYPE] = 'BOOL'
                else:
                    var_list[valueArg1][Var.VALUE] = False
                    var_list[valueArg1][Var.TYPE] = 'BOOL'
            elif typeArg2 == 'INT':
                try:    
                    var_list[valueArg1][Var.VALUE] = int(inputValue)
                    var_list[valueArg1][Var.TYPE] = 'INT'
                except: 
                    var_list[valueArg1][Var.VALUE] = Val.NIL
                    var_list[valueArg1][Var.TYPE] = 'NIL'      
            elif typeArg2 == 'STRING' and not is_eof:
                var_list[valueArg1][Var.VALUE] = inputValue
                var_list[valueArg1][Var.TYPE] = 'STRING'
            else:
                var_list[valueArg1][Var.VALUE] = Val.NIL
                var_list[valueArg1][Var.TYPE] = 'NIL'

        # WRITE
        elif insOpCode == 'WRITE':
            if typeArg1 == 'VAR':
                if var_list[valueArg1][Var.VALUE] == None: exit(56)
                valueArg1 = var_list[valueArg1][Var.VALUE]
            valueArg1 = str(valueArg1)
            if valueArg1 == 'True': valueArg1 = 'true'
            elif valueArg1 == 'False': valueArg1 = 'false'
            elif valueArg1 == 'Val.NIL': valueArg1 = ''
            print(valueArg1, end="")

        # **** Working with strings ****
        # CONCAT 
        elif insOpCode == 'CONCAT': 
            if typeArg2 != 'STRING' or typeArg3 != 'STRING': exit(53)
            var_list[valueArg1][Var.VALUE] = valueArg2 + valueArg3
            var_list[valueArg1][Var.TYPE]  = 'STRING'

        # STRLEN
        elif insOpCode == 'STRLEN':  
            if typeArg2 != 'STRING': exit(53)
            var_list[valueArg1][Var.VALUE] = len(valueArg2)
            var_list[valueArg1][Var.TYPE]  = 'INT'

        # GETCHAR
        elif insOpCode == 'GETCHAR':  
            if typeArg2 != 'STRING' or typeArg3 != 'INT': exit(53) 
            lenArg2 = len(valueArg2)-1
            if valueArg3 > lenArg2 or valueArg3 < 0: exit(58)
            var_list[valueArg1][Var.VALUE] = valueArg2[valueArg3]
            var_list[valueArg1][Var.TYPE]  = 'STRING'

        # SETCHAR
        elif insOpCode == 'SETCHAR':
            if var_list[valueArg1][Var.VALUE]  == None: exit(56)
            if var_list[valueArg1][Var.TYPE] != 'STRING': exit(53)
            if typeArg2 != 'INT' or typeArg3 != 'STRING': exit(53) 
            string = var_list[valueArg1][Var.VALUE]
            index = valueArg3
            if len(valueArg3) == 0: exit(58)
            lenArg1 = len(var_list[valueArg1][Var.VALUE]) - 1
            if valueArg2 < 0 or valueArg2 > lenArg1: exit(58) #  Bad work with the string 
            var_list[valueArg1][Var.VALUE] = string[:valueArg2] + valueArg3[0] + string[valueArg2+1:]

    # **** Working with types ****
    # TYPE - dynamically detects the type of the symbol and writes a string indiciating this type to a variable
        elif insOpCode == 'TYPE':
            if typeArg2 in ('INT', 'STRING', 'BOOL', 'NIL'):
                var_list[valueArg1][Var.VALUE] = typeArg2.lower()
                var_list[valueArg1][Var.TYPE]  = 'STRING'
            else:
                var_list[valueArg1][Var.VALUE] = ''
                var_list[valueArg1][Var.TYPE]  = 'STRING'

        # **** Program flow control instructions ****
        # JUMP - unconditional jump
        elif insOpCode == 'JUMP':
            if not valueArg1 in label_list: exit(52) 
            instruction_counter = label_list[valueArg1]

        # JUMPIFEQ, JUMPIFNEQ - conditional jump
        elif insOpCode in ('JUMPIFEQ', 'JUMPIFNEQ'):
            if not valueArg1 in label_list: exit(52)
            if not typeArg2 == typeArg3:
                    if typeArg2 == 'NIL' or typeArg3 == 'NIL':
                        pass
                    else:
                        exit(53) # Bad operand types     
            if insOpCode == 'JUMPIFEQ'  and valueArg2 == valueArg3:  
                instruction_counter = label_list[valueArg1]
            if insOpCode == 'JUMPIFNEQ' and valueArg2 != valueArg3:
                instruction_counter = label_list[valueArg1]
        
        # EXIT - terminates program execution
        elif insOpCode == 'EXIT':
            if typeArg1 == 'VAR':
                typeArg1  = var_list[valueArg1][Var.TYPE]
                valueArg1 = var_list[valueArg1][Var.VALUE]
            if valueArg1 == None : exit(56)
            if typeArg1 != 'INT' : exit(53)
            if valueArg1 < 0 or valueArg1 > 49: exit(57)
            exit(valueArg1)
        
        # **** Debugging instructions ****
        # DPRINT - prints the specified value to standard error output
        elif insOpCode == 'DPRINT':
            if typeArg1 == 'VAR':
                typeArg1  = var_list[valueArg1][Var.TYPE]
                valueArg1 = var_list[valueArg1][Var.VALUE]
            if valueArg1 == None : exit(56)
            print(valueArg1, file = sys.stderr)
        
        # BREAK
        elif insOpCode == 'BREAK':
            print("Předpokládá se, že na standardní chybový výstup vypíše stav interpretu." , file = sys.stderr)

        instruction_counter = instruction_counter + 1;

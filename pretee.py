"""
CSCI-603 PreTee Lab
Author: Sean Strout @ RIT CS
Author: Vidhathri Kota
Author: Mary Shilpa Thumma

The main program and class for a prefix expression interpreter of the
PreTee language.  See prog1.pre for a full example.

Usage: python3 pretee.py source-file.pre
"""

import sys              # argv
import literal_node     # literal_node.LiteralNode
import variable_node    # variable_node.VariableNode
import assignment_node  # assignment_node.AssignmentNode
import print_node       # print_node.PrintNode
import math_node        # math_node.MathNode
import syntax_error     # syntax_error.SyntaxError
import runtime_error    # runtime_error.RuntimeError

class PreTee:
    """
    The PreTee class consists of:
    :slot srcFile: the name of the source file (string)
    :slot symTbl: the symbol table (dictionary: key=string, value=int)
    :slot parseTrees: a list of the root nodes for valid, non-commented
        line of code
    :slot lineNum:  when parsing, the current line number in the source
        file (int)
    :slot syntaxError: indicates whether a syntax error occurred during
        parsing (bool).  If there is a syntax error, the parse trees will
        not be evaluated
    """
    __slots__ = 'srcFile', 'symTbl', 'parseTrees', 'lineNum', 'syntaxError'

    # the tokens in the language
    COMMENT_TOKEN = '#'
    ASSIGNMENT_TOKEN = '='
    PRINT_TOKEN = '@'
    ADD_TOKEN = '+'
    SUBTRACT_TOKEN = '-'
    MULTIPLY_TOKEN = '*'
    DIVIDE_TOKEN = '//'
    MATH_TOKENS = ADD_TOKEN, SUBTRACT_TOKEN, MULTIPLY_TOKEN, DIVIDE_TOKEN

    def __init__(self, srcFile, symTbl=dict(), parseTrees=[], lineNum=0):
        """
        Initialize the parser.
        :param srcFile: the source file (string)
        """
        self.srcFile = srcFile
        self.symTbl = dict()
        self.parseTrees = parseTrees
        self.lineNum = lineNum
        self.syntaxError = False

    def __parse(self, tokens):
        """
        The recursive parser that builds the parse tree from one line of
        source code.
        :param tokens: The tokens from the source line separated by whitespace
            in a list of strings.
        :exception: raises a syntax_error.SyntaxError with the message
            'Incomplete statement' if the statement is incomplete (e.g.
            there are no tokens left and this method was called).
        :exception: raises a syntax_error.SyntaxError with the message
            'Invalid token {token}' if an unrecognized token is
            encountered (e.g. not one of the tokens listed above).
        :return:
        """
        
        if len(tokens) ==  0:
            return
        elif tokens[0].isidentifier():
            node = variable_node.VariableNode(tokens[0], self.symTbl)
            self.parseTrees.append(node)
        elif tokens[0].isdigit():
            node = literal_node.LiteralNode(int(tokens[0]))
            self.parseTrees.append(node)
        elif tokens[0] == '=': 
            node = assignment_node.AssignmentNode(self.parseTrees.pop(),self.parseTrees.pop(), self.symTbl, tokens[0])
            self.parseTrees.append(node)
        elif tokens[0] == '@':
            node = print_node.PrintNode(self.parseTrees.pop())
            self.parseTrees.append(node)
        elif tokens[0] in self.MATH_TOKENS:
            x = self.parseTrees.pop()
            y = self.parseTrees.pop()
            if not isinstance(x, (variable_node.VariableNode, literal_node.LiteralNode, math_node.MathNode)):
                raise syntax_error.SyntaxError('Incomplete Statement')
            if not isinstance(y, (variable_node.VariableNode, literal_node.LiteralNode, math_node.MathNode)):
                raise syntax_error.SyntaxError('Incomplete Statement')
            node = math_node.MathNode(x,y, tokens[0])
            self.parseTrees.append(node)
        else:
            raise syntax_error.SyntaxError("Invalid token")
        self.__parse(tokens[1:])

        """
        elif tokens[0] == '=':
            try:
                x = self.parseTrees.pop()
                y = self.parseTrees.pop()
                node = assignment_node.AssignmentNode(x,y, self.symTbl, tokens[0])
                self.parseTrees.append(node)
            except syntax_error.SyntaxError as syn:
                self.parseTrees.append(y)
                self.parseTrees.append(x)
                raise syn
        
        """

    def parse(self):
        """
        The public parse is responsible for looping over the lines of
        source code and constructing the parseTree, as a series of
        calls to the helper function that are appended to this list.
        It needs to handle and display any syntax_error.SyntaxError
        exceptions that get raised.
        : return None
        """
        
        count = 1
        fh = open(self.srcFile)
        for i in fh:
            try:
                self.lineNum = count
                tokens = i.split() 
                if i[0] == '#' or tokens == []:
                    count+=1
                    continue
                elif any(self.MATH_TOKENS) in tokens:
                    if len(tokens) < 3:
                        raise syntax_error.SyntaxError("Incomplete Statement")
                if '=' in tokens[1:]:
                    count+=1
                    raise syntax_error.SyntaxError("Invalid Token")

                if i[0] == '=' or i[0] == '@':
                    count+=1   
                    if len(tokens) == 1:
                        if tokens[0] == '@':
                            node = print_node.PrintNode(literal_node.LiteralNode(' '))
                            self.parseTrees.append(node)
                        else:
                            if '@' in tokens[1:]:
                                raise syntax_error.SyntaxError("Bad assignment expression")
                            raise syntax_error.SyntaxError("Incomplete Statement")
                    self.__parse(tokens[::-1])
                else:
                    count += 1
                    if not (i[0] in self.MATH_TOKENS):
                        raise syntax_error.SyntaxError("Invalid Token")
            except syntax_error.SyntaxError as syn:
                self.syntaxError = True
                print("Line ",self.lineNum," ",syn)

    def emit(self):
        """
        Prints an infix string representation of the source code that
        is contained as root nodes in parseTree.
        :return None
        """
        for i in self.parseTrees:
            print(i.emit())

    def evaluate(self):
        """
        Prints the results of evaluating the root notes in parseTree.
        This can be viewed as executing the compiled code.  If a
        runtime error happens, execution halts.
        :exception: runtime_error.RunTimeError may be raised if a
            parse tree encounters a runtime error
        :return None
        """
        for i in self.parseTrees:
            if i.evaluate() != None:
                print(i.evaluate())

def main():
    """
        The main function prompts for the source file, and then does:
            1. Compiles the prefix source code into parse trees
            2. Prints the source code as infix
            3. Executes the compiled code
        :return: None
    """
    if len(sys.argv) != 2:
        print('Usage: python3 pretee.py source-file.pre')
        return

    pretee = PreTee(sys.argv[1])
    print('PRETEE: Compiling', sys.argv[1] + '...')
    pretee.parse()
    print('\nPRETEE: Infix source...')
    pretee.emit()
    #print(pretee.lineNum)
    print('\nPRETEE: Executing...')
    try:
        if pretee.syntaxError is False:
            pretee.evaluate()
    except runtime_error.RuntimeError as e:
        # on first runtime error, the supplied program will halt execution
        print('*** Runtime error:', e)

if __name__ == '__main__':
    main()
"""
CSCI-603 Parser Lab
Author: Sean Strout @ RIT CS

An assignment statement is of the prefix form:

    '= {variable} {expression}'

For example:

    '= x 10'
    '= y 20'
    '= z + x y'
    '= x 40'

When emitted, the variable is emitted, followed by the equals sign, followed
by the emission of the expression that followed.

    'x = 10'
    'y = 20'
    'z = (x + y)'
    'x = 40'

When evaluated, the expression is evaluated and its result is
stored in the symbol table for the variable.

    # symbol table: {..., 'x': 10, ...}
    # symbol table: {..., 'y': 20, ...}
    # symbol table: {..., 'z': 30, ...}
    # symbol table: {..., 'x': 40, ...}

A syntax_error.SyntaxError will be raised for the following:

    1. Assignment to a non-variable node, e.g.:

        = 10 10     # error message: Bad assignment to non-variable

    2. Bad expression for assignment, e.g.:

        = x @       # error message: Bad assignment expression
"""

import literal_node     # literal_node.LiteralNode
import math_node        # math_node.MathNode
import variable_node    # variable_node.VariableNode
import syntax_error     # syntax_error.SyntaxError

class AssignmentNode:
    """
    The AssignmentNode class consists of:
    :slot variable: The variable node (VariableNode)
    :slot expression: The expression that represents the value
        the variable will be associated with (LiteralNode,
        MathNode or VariableNode)
    :slot symTbl: The symbol table which associates variable
        names (key=str) with values (value=int)
    :slot token:  The character associated with assignment
        when emitting (str)
    """
    __slots__ = 'variable', 'expression', 'symTbl', 'token'

    def __init__(self, variable, expression, symTbl, token):
        """
        Initialize an AssignmentNode.

        :param variable: The variable node (VariableNode)
        :param expression: The expression that represents the value
            the variable will be associated with (LiteralNode,
            MathNode or VariableNode)
        :param symTbl: The symbol table which associates variable
            names (key=str) with values (value=int)
        :param token: The character associated with assignment
            when emitting (str)
        :exception: raises syntax_error.SyntaxError if there is an assignment
            to a non-variable, with the message, 'Bad assignment to non-variable'
        :exception: raises syntax_error.SyntaxError if the expression is bad,
            with the message, 'Bad assignment expression'.
        :return: None
        """
        # first check for syntax errors and raise an appropriate exception
        if not isinstance(variable, variable_node.VariableNode):
            raise syntax_error.SyntaxError('Bad assignment to non-variable')

        if not isinstance(expression,
            (literal_node.LiteralNode, math_node.MathNode, variable_node.VariableNode)):
            raise syntax_error.SyntaxError('Bad assignment expression')

        self.variable = variable
        self.expression = expression
        self.symTbl = symTbl
        self.token = token

    def emit(self):
        """
        Returns a string in infix form:
            '{variable-emit} {token} {expression-token}'
        :return: The infix string (str)
        """
        return self.variable.emit() + ' ' + self.token + ' ' + self.expression.emit()

    def evaluate(self):
        """
        Evaluates the expression and stores the result in the symbol table
        for the variable name.
        :exception: runtime_error.RunTimeError may be raised if an assignment
            to an invalid expression is made (e.g. unknown variable name or
            bad expression).
        :return: None
        """
        self.symTbl[self.variable.id] = self.expression.evaluate()

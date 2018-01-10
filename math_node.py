"""
CSCI-603 Parser Lab
Author: Sean Strout @ RIT CS
Author: Vidhathri Kota
Author: Mary Shilpa Thumma

A math expression is of the prefix form:

    '{operator} {left-expression} {right-expression}'

For example:

    '+ 10 20'
    '* 3 5'
    '- 2 4'
    '// 13 2'
    '+ 2 * 8 7'

When emitted, the statement is converted into an infix string:

    '(10 + 20)'
    '(3 * 5)'
    '(2 - 4)'
    '(13 //2 )'
    '(2 + (8 * 7))'

When evaluated, integer result is returned:

    30
    15
    -2
    6
    58

A runtime exception is raised division by 0 is attempted:

    '// 4 0'            # error message: Division by zero error
"""

import runtime_error        # runtime_error.RuntimeError
import pretee               # pretee.PreTee.ADD_TOKEN, ...

class MathNode:
    """
    A MathNode consists of:
    :slot left: the left expression (LiteralNode, MathNode, VariableNode)
    :slot right: the right expression (LiteralNode, MathNode, VariableNode)
    :token: the character for the math operation (str)
    """
    __slots__ = 'left', 'right', 'token'

    def __init__(self, left, right, token):
        """
        Initialize a MathNode.
        :param left: the left expression (LiteralNode, MathNode, VariableNode)
        :param right: the right expression (LiteralNode, MathNode, VariableNode)
        :param token: the character for the math operation (str)
        :return: None
        """
        """
        if not isinstance(left, (variable_node.VariableNode, literal_node.LiteralNode, MathNode)):
            raise syntax_error.SyntaxError('Incomplete Statement')
        if not isinstance(right, (variable_node.VariableNode, literal_node.LiteralNode, MathNode)):
            raise syntax_error.SyntaxError('Incomplete Statement')
        """

        self.left = left
        self.right = right
        self.token = token

    def emit(self):
        """
        Returns a parenthesized string with the emits of the left and
        right expressions, e.g.:
            '({left-emit} {token} {right-emit})'
        :return:
        """
        return "( "+ self.left.emit() + self.token + self.right.emit() + " )"

    def evaluate(self):
        """
        Evaluates the math expression and returns the result.
        :exception: raises a runtime_error.RuntimeError if division by zero
            is attempted, with the message, 'Division by zero error'
        :return: The result of performing the math operation (int)
        """
        if self.token == '+':
            return self.left.evaluate() + self.right.evaluate()
        elif self.token == '-':
            return self.left.evaluate() - self.right.evaluate()
        elif self.token == '*':
            return self.left.evaluate() * self.right.evaluate()
        else:
            try:
                return self.left.evaluate() // self.right.evaluate()
            except:
                raise runtime_error.RuntimeError("Division by 0 error")

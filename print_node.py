"""
CSCI-603 Parser Lab
Author: Sean Strout @ RIT CS
Author: Vidhathri Kota
Author: Mary Shilpa Thumma

A print statement is of the prefix form, where {expression} is optional:

    '@ {expression}'

For example:

    '@'
    '@ 10'
    '@ + 10 20'
    '@ x'            # assuming x = 10

When emitted, the string {\tt ``print''} is emitted, followed by a
space, and the emission of the expression that follows.

    'print'
    'print 10'
    'print (10 + 20)'
    'print x'

When evaluated, the expression is evaluated and its result,
if present, is displayed:

                    # just a newline is printed
    10
    30
    10              # the value of x is printed
"""

class PrintNode:
    """
    A PrintNode consists of:
    :slot expression: A valid expression node (LiteralNode, VariableNode,
        MathNode)
    """
    __slots__ = 'expression'

    def __init__(self, expression=None):
        """
        Initialize a PrintNode
        :param expression: A valid expression node (LiteralNode, VariableNode,
            MathNode)
        :return: None
        """
        self.expression =  expression

    def emit(self):
        """
        Returns a string in infix form, where {expression} is optional:
            print {expression-emit}
        :return: The infix string (str)
        """
        if self.expression.emit().startswith("print"):
            return self.expression.emit()
        return "print ( "+ self.expression.emit() + " )"

    def evaluate(self):
        """
        If the expression is not present, just prints a newline, otherwise
        it prints the evaluation of the expression in string form.
        :return: None
        """
        if self.expression.emit().startswith("print"):
            pass
        else:
            print(self.expression.evaluate())

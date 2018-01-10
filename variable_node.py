"""
CSCI-603 Parser Lab
Author: Sean Strout @ RIT CS
Author: Vidhathri Kota
Author: Mary Shilpa Thumma 

A variable expression is a legal identifier in Python:

    '{id}'

For example:

    'x'
    'y'
    'variable'

When emitted, the variable name is returned as a string, e.g.:

    'x'
    'y'
    'variable'

When evaluated, the value associated with the variable name in the symbol
table is returned.  For example if the symbol table contains 
{..., 'x': 10, 'y' : 20, 'z' : 30, ...}, the evaluations
would be:

	 10             
	 20              
	 30

A runtime exception is raised if the variable is not in the symbol table, e.g.:

    'a'             # error message: Unrecognized variable a
"""

import runtime_error        # runtime_error.RuntimeError

class VariableNode:
    """
    A VariableNode consists of:
    :slot id: The name of the variable (str)
    :slot symTbl: The symbol table which associates variable
        names (key=str) with values (value=int)
    """
    __slots__ = 'id', 'symTbl'

    def __init__(self, id, symTbl):
        """
        Initialize a VariableNode.
        :param id: The name of the variable (str)
        :param symTbl: The symbol table which associates variable
        names (key=str) with values (value=int)
        :return: None
        """
        self.id = id
        self.symTbl = symTbl

    def emit(self):
        """
        Return the name of the variable.
        :return: The variable name (str)
        """
        return str(self.id)

    def evaluate(self):
        """
        Evaluates the variable to retrieve its stored value.
        :exception: raises a runtime_error.RuntimeError if the variable name
            is not in the symbol table, with the message,
            'Unrecognized variable {variable}'
        :return: The value associated with the variable (int)
        """
        try:
            return self.symTbl[self.id]
        except:
            raise runtime_error.RuntimeError("Unrecognized variable",self.id)

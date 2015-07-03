#!/usr/bin/0python3

"""
Code which saves mathematical expressions as an expression tree, this is done by implementing 
the Shunting-Yard algorithm to convert the Reverse Polish Notation into an expression tree.
This representation can be used to perform several calculations and symbolic manipulation.

B.J.M. van Dijk & M.O. El-Haloush @ Utrecht, 2015
"""

import math

# split a string into mathematical tokens
# returns a list of numbers, operators, parantheses and commas
# output will not contain spaces
def tokenize(string):
    splitchars = list("+-*/(),%")
    # surround any splitchar by spaces
    tokenstring = []
    for c in string:
        if c in splitchars:
            tokenstring.append(' %s ' % c)
        else:
            tokenstring.append(c)
    tokenstring = ''.join(tokenstring)
    # split on spaces: this gives us our tokens
    tokens = tokenstring.split()
    # special casing for ** and //
    ans = []
    for t in tokens:
        if len(ans) > 0 and t == ans[-1] == '*':
            ans[-1] = '**'
        elif len(ans) > 0 and t == ans[-1] == '/':
            ans[-1] = '//'
        #elif len(ans) > 0 and t == ans[-1] == '=':
        #    ans[-1] = '=='
        else:
            ans.append(t)
    return ans


# check if a string represents a numeric value
def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# check if a string represents an integer value        
def isint(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


# check if a string represents a variable
def isvar(string):
    try:
        str(string)
        return True
    except ValueError:
        return False


# check precedence
def prec(token):
    if token == '**':
        return(1)
    elif token == '*' or token == '/' or token == '%' or token == '//':
        return(2)
    elif token == '+' or token == '-':
        return(3)


# check associativity
def assoc(token):
    l_oplist = ['+', '-', '*', '/', '%', '//']
    r_oplist = ['**']   
    if token in l_oplist:
        return(0)
    if token in r_oplist:
        return(1)


class Expression():
    """A mathematical expression, represented as an expression tree"""
    """
    Any concrete subclass of Expression should have these methods:
     - __str__(): return a string representation of the Expression.
     - __eq__(other): tree-equality, check if other represents the same expression tree.
    """
    # operator overloading:
    # this allows us to perform 'arithmetic' with expressions, and obtain another expression
    def __add__(self, other):
        return AddNode(self, other)

    def __sub__(self, other):
        return SubNode(self, other)

    def __mul__(self, other):
        return MulNode(self, other)

    def __truediv__(self, other):
        return TrueDivNode(self, other)
        
    def __pow__(self, other):
        return PowNode(self, other)

    def __mod__(self, other):
        return ModNode(self, other)

    def __floordiv__(self, other):
        return FloorDivNode(self, other)

    def __eq__(self, other):
        #return EqNode(self, other)
        if type(self) != type(other):
            return False

    # basic Shunting-yard algorithm
    def fromString(string):
        # split into tokens
        tokens = tokenize(string)
        # stack used by the Shunting-Yard algorithm
        stack = []
        # output of the algorithm: a list representing the formula in RPN
        # this will contain Constant's and '+'s
        output = []
        # list of operators
        oplist = ['+', '-', '*', '/', '**', '%', '//']
        for token in tokens:
            if isnumber(token):
                # numbers go directly to the output
                if isint(token):
                    output.append(Constant(int(token)))
                else:
                    output.append(Constant(float(token)))
            elif isvar(token) and token not in oplist:
                output.append(Variable(str(token)))
            elif token in oplist:
                # pop operators from the stack to the output until the top is no longer an operator
                while True:
                    if len(stack) == 0 or stack[-1] not in oplist \
                    or int(assoc(stack[-1])) == 0 and int(prec(stack[-1])) <= int(prec(token)) \
                    or int(assoc(stack[-1])) == 1 and int(prec(stack[-1])) <  int(prec(token)):
                        break
                    output.append(stack.pop())
                # push the new operator onto the stack
                stack.append(token)
            elif token == '(':
                # left parantheses go to the stack
                stack.append(token)
            elif token == ')':
                # right paranthesis: pop everything upto the last left paranthesis to the output
                while not stack[-1] == '(':
                    output.append(stack.pop())
                # pop the left paranthesis from the stack (but not to the output)
                stack.pop()
            else:
                # unknown token
                raise ValueError('Unknown token: %s' % token)
        # pop any tokens still on the stack to the output
        while len(stack) > 0:
            output.append(stack.pop())
        # convert RPN to an actual expression tree
        for t in output:
            if t in oplist:
                # let eval and operator overloading take care of figuring out what to do
                y = stack.pop()
                x = stack.pop()
                stack.append(eval('x %s y' % t))
            else:
                # a constant, push it to the stack
                stack.append(t)
        # the resulting expression tree is what's left on the stack
        return stack[0]


class Constant(Expression):
    """Represents a constant value"""
    def __init__(self, value):
        self.value = value
        
    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.value == other.value
        else:
            return False
        
    def __str__(self):
        return str(self.value)
        
    # allow conversion to numerical values
    def __int__(self):
        return int(self.value)
        
    def __float__(self):
        return float(self.value)

    def evaluate(self, dic=None):
        return float(self)


class Variable(Expression):
    """Represents a variable"""
    def __init__(self, variable):
        self.variable = variable

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.variable == other.variable
        else:
            return False
        
    def __str__(self):
        return str(self.variable)
        
    def evaluate(self, dic=None):
        return dic[self.variable]          

        
class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""    
    def __init__(self, lhs, rhs, op_symbol):
        self.lhs = lhs
        self.rhs = rhs
        self.op_symbol = op_symbol
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif self.op_symbol != other.op_symbol:
            return False
        else:
            return self.lhs == other.lhs and self.rhs == other.rhs
            
    def expteq(self,other,dic1=None, dic2=None):
        "A function to compare the similarity of operants/constants/variables in self and other expression"
        oplist = ['+', '-', '*', '/', '**', '%', '//']
        charlist = ['(',')',' ','.']
        #Creating a string from self, without changing self
        strself = str(self) 
        #Creating a string from other, wothout changing other
        strother = str(other)
        #Initiating an operant string from self
        selfop = str()
        #Initiating an operant string from other
        otherop = str()
        #Initiating a Constant string from self
        selfc = str()
        #Initiating a Constant string from other
        otherc = str()
        #Initiating a Variable string from self
        selfv = str()
        #Intiating a Variable string from other
        otherv = str()

        #Creating a string from self, without changing self
        for i in str(self):
            if i in oplist:
                # Initiating an operant string from self
                selfop += str(i)
            else:
                if isint(i) == False or isnumber(i) == False:
                    if i not in charlist:
                        # Initiating a Variable string from self
                        selfv += str(i)
                else:
                    # Initiating a Constant string from self
                    selfc += str(i)
        # Creating a string from other, without changing other
        for i in str(other):
            # Adding of the strings from other
            if i in oplist:
                # Initiating an operant string from other
                otherop += str(i)
            else:
                if isint(i) == False or isnumber(i) == False:
                    if i not in charlist:
                        # Initiating a Variable string from self
                        otherv += str(i)
                else:
                    # Initiating a Constant string from other
                    otherc += str(i)
        if (selfop == otherop) == True:
            print(' Operations are equal and in the same order')
        else:
            print(' Operations are not equal')
        if (selfc == otherc) == True:
            print(' Constants are equal and in the same order')
        else:
            print(' Constants are not equal')
        print(selfc,selfop)    
        return        
            
    def __str__(self):
        lstring = str(self.lhs)
        rstring = str(self.rhs)
        oplist = ['+', '-', '*', '/', '**', '%', '//']
        for token in lstring:
            if token in oplist:
                if  (int(assoc(token)) == 0 and int(prec(token) <= int(prec(self.op_symbol)))):
                    return "%s %s %s" % (lstring, self.op_symbol, rstring)
                elif ((int(assoc(token)) == 1 and int(prec(token))) <  int(prec(self.op_symbol))):
                    return "(%s) %s %s" % (lstring, self.op_symbol, rstring)
        return "%s %s %s" % (lstring, self.op_symbol, rstring)
        
    def evaluate(self, dic=None):
        lhsEval = self.lhs.evaluate(dic)
        rhsEval = self.rhs.evaluate(dic)
        return eval("(%s %s %s)" % (lhsEval, self.op_symbol, rhsEval)) 

    def findRoot(self , x, a = -1000, b = 1000, epsilon = 0.01):
        "Represents a function to find zero points of an expression with 1 Variable()"
        m = ( a + b ) / 2
        while (b - a) > epsilon:
            if eval(str(self), {x: m}) == 0:
                return m
            elif (eval(str(self), {x: a}) * eval(str(self), {x:m})) < abs(epsilon):
                b = m
            elif (eval(str(self), {x: b}) * eval(str(self), {x:m})) < abs(epsilon):
                a = m
            else:
                b = m
            m = ( a + b ) / 2
        return ("{:.3f}".format(m))
    
    def findAllRoots(self, x, a = -1000, b = 1000, epsilon = 0.01):
        zero = []
        #self=str(self)
        while abs(b - a) > epsilon:
            if (eval(str(self), {x:a}) * eval(str(self), {x: a + epsilon})) > 0:
                a += epsilon
            else:
                zero.append(self.findRoot(x, a, (a+epsilon), epsilon))
                a += epsilon
        return zero   

        
class AddNode(BinaryNode):
    """Represents the addition operator"""
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs, '+')


class SubNode(BinaryNode):
    """Represents the substraction operator"""
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs, '-')


class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs, '*')

        
class TrueDivNode(BinaryNode):
    """Represents the division operator"""
    def __init__(self, lhs, rhs):
        super(TrueDivNode, self).__init__(lhs, rhs, '/')


class PowNode(BinaryNode):
    """Represents the power operator"""
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs, '**')


class ModNode(BinaryNode):
    """Represents the modulus operator"""
    def __init__(self, lhs, rhs):
        super(ModNode, self).__init__(lhs, rhs, '%')


class FloorDivNode(BinaryNode):
    """Represents the floor division operator"""
    def __init__(self, lhs, rhs):
        super(FloorDivNode, self).__init__(lhs, rhs, '//')


class EqNode(BinaryNode):
    """Represents the equality operator"""
    def __init__(self, lhs, rhs):
        super(EqNode, self).__init__(lhs, rhs, '==')
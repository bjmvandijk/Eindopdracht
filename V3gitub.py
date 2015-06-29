#!/usr/bin/python3

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
    #split on spaces - this gives us our tokens
    tokens = tokenstring.split()
    
    #special casing for ** and //
    ans = []
    for t in tokens:
        if len(ans) > 0 and t == ans[-1] == '*':
            ans[-1] = '**'
        elif len(ans) > 0 and t == ans[-1] == '/':
            ans[-1] = '//'
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

#check if a string represents an Variable
def isvar(string):
    try:
        str(string)
        return True
    except ValueError:
        return False

class Expression():
    """A mathematical expression, represented as an expression tree"""
    
    """
    Any concrete subclass of Expression should have these methods:
     - __str__(): return a string representation of the Expression.
     - __eq__(other): tree-equality, check if other represents the same expression tree.
    """
    # TODO: when adding new methods that should be supported by all subclasses, add them to this list
    
    # operator overloading:
    # this allows us to perform 'arithmetic' with expressions, and obtain another expression
    def __add__(self, other):
        return AddNode(self, other)

    def __sub__(self, other):
        return SubNode(self, other)

    def __mul__(self, other):
        return MulNode(self, other)

    def __truediv__(self, other):
        return DivNode(self, other)
        
    def __pow__(self, other):
        return PowNode(self, other)

    def __mod__(self, other):
        return ModNode(self, other)

    def __floordiv__(self, other):
        return FloorDivNode(self, other)

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
                    # TODO: when there are more operators, the rules are more complicated
                    # look up the shunting yard-algorithm
                    if len(stack) == 0 or stack[-1] not in oplist:
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
            # TODO: do we need more kinds of tokens?
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
        
    def evaluate(self,dic):
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
        
    def evaluate(self,dic):
        return dic[self.variable]
    

class Function(Expression):
    """Represents a function"""
    def __init__(self, function):
        self.function = function

    def __eq__(self, other):
        if isinstance(other, Function):
            return self.function == other.function
        else:
            return False

    def __str__(self):
        return str(self.function)

class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""
    
    def __init__(self, lhs, rhs, op_symbol):
        self.lhs = lhs
        self.rhs = rhs
        self.op_symbol = op_symbol
    # TODO: what other properties could you need? Precedence, associativity, identity, etc.

    def __eq__(self, other):
        if type(self) == type(other):
            if self.lhs == other.lhs and self.rhs == other.rhs:
                return True
        else:
            return False
    def opeq(self,other,dic1=None, dic2=None):
        "An function to compare the similarity of operants in self and other expression"
        print('Equalty check started:')
        oplist = ['+', '-', '*', '/', '**', '%', '//']
        charlist = ['(',')',' ','.']
        strself=str(self) #Creating a string from self, without changing self
        strother=str(other) #Creating a string from other, wothout changing other
        selfop=str() #Initiating an operant string from self
        otherop=str() #Initiating an operant string from other
        selfc=str() #Initiating a Constant string from self
        otherc=str() #Initiating a Constant string from other
        selfv=str() #Initiating a Variable string from self
        otherv=str() #Intiating a Variable string from other
        for i in strself:
            "Adding of the strings from self"
            if i in oplist:
                selfop+=i
            else:
                if isint(i)==False or isnumber(i)==False:
                    if i not in charlist:
                        selfv+=i
                else:
                    selfc+=i
        for i in strother:
            "Adding of the strings from other"
            if i in oplist:
                otherop+=i
            else:
                if isint(i)==False or isnumber(i)==False:
                    if i not in charlist:
                        otherv+=i
                else:
                    otherc+=i
        if (len(selfv) or len(otherv))>0:
            "Checking if there is an Variable() in self or other and if a dictionary is given"
            if (isvar(self)==True and dic1==None) or (isvar(other)==True and dic2==None):
                print(' Found Type Variable() but missing dictionary')
                print(' For comparing evaluate, please provide a dictionary for Expression in the following order:\n        self, other, dictonary self, dictionary other')
                return
            else:
                "Evaluation of self and other and comparing the result (with or without dictionaries"
                evaluated=(BinaryNode.evaluate(self,dic1)==BinaryNode.evaluate(other,dic2))
                if evaluated==True:
                    print(' Evaluated Expressions are equal:',BinaryNode.evaluate(self,dic1))
                else:
                    print(' Evaluated Expressions are not equal:', BinaryNode.evaluate(self,dic1),'and', BinaryNode.evaluate(other,dic2))
        if (selfop==otherop)==True:
            print(' Operations are equal and in the same order')
        else:
            print(' Operations are not equal')
        if (selfc==otherc)==True:
            print(' Constants are equal and in the same order')
        else:
            print(' Constants are not equal')
        return         
 
    def __str__(self):
        def stringinstr(self):
            lstring = str(self.lhs)
            rstring = str(self.rhs)
            # TODO: do we always need parantheses?
            oplist = ['+', '-', '*', '/', '**', '%', '//']
            oplist2 = ['+','-']
            oplist3 = ['*','/']
            oplist4 = ['**']
            oplist5 = ['%', '//']
            if self.op_symbol in oplist4:
                    stringself= "%s %s %s %s" % (lstring[:len(lstring)-2],lstring[len(lstring)-1], self.op_symbol, rstring)
                    return stringself
            for i in lstring:
                if i in oplist2:
                    if self.op_symbol not in oplist2:
                        stringself= "(%s) %s %s" % (lstring, self.op_symbol, rstring)
                        return stringself
                if i in oplist3:
                    if self.op_symbol not in (oplist3 and oplist2):
                        stringself= "(%s) %s %s" % (lstring, self.op_symbol, rstring)
                        return stringself
                if i in oplist5:
                    if self.op_symbol not in (oplist5 and oplist3 and oplist2):
                        stringself= "(%s) %s %s" % (lstring, self.op_symbol, rstring)
                        return stringself
                if i in oplist4:
                    if self.op_symbol not in oplist4:
                        stringself= "(%s) %s %s" % (lstring, self.op_symbol, rstring)
                        return stringself        
            stringself= "%s %s %s" % (lstring, self.op_symbol, rstring)
            return stringself
        new=stringinstr(self)
        return new     
        
    def evaluate(self, dic=None):
        lhsEval = self.lhs.evaluate(dic)
        rhsEval = self.rhs.evaluate(dic)
        return eval("%s %s %s" % (lhsEval, self.op_symbol, rhsEval))
        
    def findRoot(self,x,epsilon,n1=None,n2=None):
        "Represents a function to find zero points of an expression with 1 Variable()"
        if (n1 or n2)==None:
            print('To find Root, please provide an interval as a two dictionaries:\n  interval1: {Dictionary} , interval2 {Dictionary}')
            return
        m={x:float((n1[x]+n2[x])/2)}
        b=float(n2[x])
        a=float(n1[x])
        epsilon=float(epsilon)
        if abs(b-a)<=epsilon:
            print("{:.2f}".format(m[x]))
            return m
        elif self.evaluate(n1)<0.0 and self.evaluate(m)>0.0:
            return self.findRoot(x,epsilon,n1,m)
        elif self.evaluate(n2)<0.0 and self.evaluate(m)>0.0: 
            return self.findRoot(x,epsilon,m,n2)
        elif self.evaluate(n1)>0.0 and self.evaluate(m)<0.0:
            return self.findRoot(x,epsilon,n1,m)
        elif self.evaluate(n2)>0.0 and self.evaluate(m)<0.0: 
            return self.findRoot(x,epsilon,m,n2)    
        else:
            n1[x]+=epsilon
            n2[x]-=epsilon
            return self.findRoot(x,epsilon,n1,n2)    

class AddNode(BinaryNode):
    """Represents the addition operator"""
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs, '+')

    def minimum(self):
        ans = minimum(self)
        return ans

class SubNode(BinaryNode):
    """Represents the substraction operator"""
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs, '-')

class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs, '*')
 
class DivNode(BinaryNode):
    """Represents the division operator"""
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs, '/')

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

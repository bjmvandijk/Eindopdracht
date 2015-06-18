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

class Expression():
    """A mathematical expression, represented as an expression tree"""
    
    """
    Any concrete subclass of Expression should have these methods:
     - __str__(): return a string representation of the Expression.
     - __eq__(other): tree-equality, check if other represents the same expression tree.
    """
##### TODO: when adding new methods that should be supported by all subclasses, add them to this list
    
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
            elif token in oplist:
                # pop operators from the stack to the output until the top is no longer an operator
                while True:
##################### TODO: when there are more operators, the rules are more complicated
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
############# TODO: do we need more kinds of tokens?
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

def evaluate(self):
        
    new = str(self)
    
    
    
    charlist = ['+', '-', '*', '/', '**', '%', '//', '(', ')']
    #oplist2 = ['(','+','-','*','/','**',')']
    count = 0
    
    #for i in new:
    count += new.count("(")    
    i = 0
    j = 0
    
    while i < len(new):
        if new[i] == '(':
            if count == 1:
                i = j
                while j < len(new):
                    if new[j] == ')':
                        print(new[i+1:j+1])
                        new2 = new[i+1:j+1]
                        new3 = str()
                        for i in new2:
                            charlist3=[' ', '(', ')']
                            if i not in charlist3:
                                new3 += i
                        print(new3)        
                        if '+' in new3:
                            new4 = float(new3[0]) + float(new3[2])
                        elif '-' in new3:
                            new4 = float(new3[0]) - float(new3[2])   
                        elif '/' in new3:
                            new4 = float(new3[0]) / float(new3[2])    
                        elif '*' in new3:
                            new4 = float(new3[0]) * float(new3[2])
                        elif '**' in new3:
                            new4 = float(new3[0]) ** float(new3[2])  
                        elif '%' in new3:
                            new4 = float(new3[0]) % float(new3[2])
                        elif '//' in new3:
                            new4 = float(new3[0]) // float(new3[2])    
                        print(new4)    
                        j = (len(new)-1)
                        i = (len(new)-1)
                    j += 1
                i += 1
            count -= 1
            i += 1
            
            #else:
             #   continue
        else:
            i += 1
    new = new.split()
            
    print(new, type(new))
        
    
    
    return new

    
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
        
class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""
    
    def __init__(self, lhs, rhs, op_symbol):
        self.lhs = lhs
        self.rhs = rhs
        self.op_symbol = op_symbol
    
##### TODO: what other properties could you need? Precedence, associativity, identity, etc.
            
    def __eq__(self, other):
        if type(self) == type(other):
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return False
            
    def __str__(self):
        lstring = str(self.lhs)
        rstring = str(self.rhs)
        
######### TODO: do we always need parantheses?
        return "(%s %s %s)" % (lstring, self.op_symbol, rstring)
        
class AddNode(BinaryNode):
    """Represents the addition operator"""
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs, '+')

    def evaluate(self):
    	ans = evaluate(self)
    	return ans

class SubNode(BinaryNode):
    """Represents the substraction operator"""
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs, '-')

    def evaluate(self):
    	ans = evaluate(self)
    	return ans

class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs, '*')

    def evaluate(self):
    	ans = evaluate(self)
    	return ans
        
class DivNode(BinaryNode):
    """Represents the division operator"""
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs, '/')

    def evaluate(self):
    	ans = evaluate(self)
    	return ans

class PowNode(BinaryNode):
    """Represents the power operator"""
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs, '**')

    def evaluate(self):
    	ans = evaluate(self)
    	return ans

class ModNode(BinaryNode):
    """Represents the modulus operator"""
    def __init__(self, lhs, rhs):
        super(ModNode, self).__init__(lhs, rhs, '%')

    def evaluate(self):
    	ans = evaluate(self)
    	return ans

class FloorDivNode(BinaryNode):
    """Represents the floor division operator"""
    def __init__(self, lhs, rhs):
        super(FloorDivNode, self).__init__(lhs, rhs, '//')

    def evaluate(self):
    	ans = evaluate(self)
    	return ans

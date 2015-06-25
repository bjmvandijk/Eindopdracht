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

    #def __str__(self,var=None):
    #    def evaluate(self, var=None):
    #        ans = evaluate(self,var)
    #        return ans
    #    ans=replace(self,var)
    #    return ans 

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
        #stack[0]=stack[0].minimum()
        #ans=Expression.__str__(stack[0])
        ans=0
        '''for i in stack[0]:
            print(i)
            oplist = ['+', '-', '*', '/', '**', '%', '//', '(', ')']
            if i in oplist:
                ans+=i
            else:    
                try: 
                    ans+=Constant(i)
                except:
                    ans+=Variable(i)
            
        print(ans, type(ans))'''
        return stack[0]

def replace(self, var=None):
        self = str(self)
        if var == None:
            return self
        else:
            ans = str()
            for i in self:
                if i in var:
                    j = var.get(i)
                    ans += str(j)
                else:
                    ans += str(i)    
            self = ans
            return self
        
'''def evaluate(self, var=None):
    new = replace(self,var) 
    charlist = ['+', '-', '*', '/', '**', '%', '//', '(', ')']
    oplist = ['+', '-', '*', '/', '**', '%', '//']
    i = 0
    
    def calc(string):
        calc = str(string)
        i = 0
        j = 0
        k = 0
        newcalc = 0
        while i < len(calc):
            if calc[i] in oplist:
                if calc[i] == '+':
                    j = i - 1
                    while j >= 0:
                        if calc[j] in charlist:
                            k = i + 1
                            while k <= len(calc):
                                if calc[k] in charlist:
                                    newcalc += float(calc[j+1:i]) + float(calc[i+1:k])
                                    calc = calc[:j] + str(newcalc) + calc[k:]
                                    k = (len(calc) + 1)
                                else:
                                    k += 1
                            j -= 1
                            i = 0
                        else:
                            j -= 1
                if calc[i] == '-':
                    j = i - 1
                    while j >= 0:
                        if calc[j] in charlist:
                            k = i + 1
                            while k <= len(calc):
                                if calc[k] in charlist:
                                    newcalc += float(calc[j+1:i]) - float(calc[i+1:k])
                                    calc = calc[:j] + str(newcalc) + calc[k:]
                                    k = (len(calc) + 1)
                                else:
                                    k += 1
                            j -= 1
                            i = 0
                        else:
                            j -= 1
                if calc[i] == '*' and calc[i+1] == '*':
                    j = i - 1
                    while j >= 0:
                        if calc[j] in charlist:
                            k = i + 2
                            while k <= len(calc):
                                if calc[k] in charlist:
                                    newcalc += float(calc[j+1:i]) ** float(calc[i+2:k])
                                    calc = calc[:j] + str(newcalc) + calc[k:]
                                    k = (len(calc) + 1)
                                else:
                                    k += 1
                            j -= 1
                            i = 0
                        else:
                            j -= 1
                if calc[i] == '/' and calc[i+1] == '/':
                    j = i - 1
                    while j >= 0:
                        if calc[j] in charlist:
                            k = i + 2
                            while k <= len(calc):
                                if calc[k] in charlist:
                                    newcalc += float(calc[j+1:i]) // float(calc[i+2:k])
                                    
                                    calc = calc[:j] + str(newcalc) + calc[k:]
                                    k = (len(calc) + 1)
                                else:
                                    k += 1
                            j -= 1
                            i = 0
                        else:
                            j -= 1
                if calc[i] == '*':
                    j = i - 1
                    while j >= 0:
                        if calc[j] in charlist:
                            k = i + 1
                            while k <= len(calc):
                                if calc[k] in charlist:
                                    newcalc += float(calc[j+1:i]) * float(calc[i+1:k])
                                    
                                    calc = calc[:j] + str(newcalc) + calc[k:]
                                    k = (len(calc) + 1)
                                else:
                                    k += 1
                            j -= 1
                            i = 0
                        else:
                            j -= 1            
                if calc[i]== '/':
                    j = i - 1
                    while j >= 0:
                        if calc[j] in charlist:
                            k = i + 1
                            while k <= len(calc):
                                if calc[k] in charlist:
                                    newcalc += float(calc[j+1:i]) / float(calc[i+1:k])
                                    calc = calc[:j] + str(newcalc) + calc[k:]
                                    k = (len(calc) + 1)
                                else:
                                    k += 1
                            j -= 1
                            i = 0
                        else:
                            j -= 1
                if calc[i] == '%':
                    j = i - 1
                    while j >= 0:
                        if calc[j] in charlist:
                            k = i + 1
                            while k <= len(calc):
                                if calc[k] in charlist:
                                    newcalc += float(calc[j+1:i]) % float(calc[i+1:k])
                                    calc = calc[:j] + str(newcalc) + calc[k:]
                                    k = (len(calc) + 1)
                                else:
                                    k += 1
                            j -= 1
                            i = 0
                        else:
                            j -= 1            
                else:
                    i += 1
            else:
                i += 1
        newcalc = str()
        remove = str()
        for i in calc:
            if i== '(' or i == ')':
                remove += i
            else:
                newcalc += i
        calc = newcalc        
        return calc
    count = new.count("(") 
    while i < len(new):
        if new[i] == '(':
            if count == 1:    
                j = i + 1
                while j < len(new):
                    if new[j] == ')':
                        ans = (calc(new[i:j + 1]))
                        new = new[:i] + str(ans) + new[j+1:]
                        j = len(new)
                        i = 0
                        count = new.count("(")
                    else:
                        j += 1
            else:
                count -= 1
                i += 1
        else:
            i += 1
    return new
'''
def minimum(self):
    oplist = ['+', '-', '*', '/', '**', '%', '//']
    oplist2 = ['+','-']
    oplist3 = ['*','/']
    oplist4 = ['**']
    oplist5 = ['%', '//']
    #oplist6 = ['//']
    new = (str(self))
    i = 0
    j = 0
    while i < len(new):
        if new[i] in oplist:
            # define the importance of + and -
            if new[i] in oplist2:
                j = i + 1
                while j < len(new):
                    if new[j] in oplist:
                        if new[j] in oplist2:
                            new1 = new[i:j]
                            new2 = str()
                            for k in new1:
                                if k is not ')':
                                    new2 += k
                            new3 = str()
                            new3 = new[0:i] + new2 + new[j:len(new)]
                            l = i
                            while l >= 0:
                                if new3[l] == '(':
                                    new4 = str()
                                    new4 = new3[:l] + new3[l+1:]
                                    new = new4
                                    i = 0
                                    j = 0
                                    l =- 1
                                else:
                                    l -= 1
                            j = len(new)    
                        else:
                            j = len(new)
                    else:
                        j += 1
            # define the importance of * and /
            elif new[i] in oplist3:
                j = i + 1
                while j < len(new):
                    if new[j] in oplist:
                        if new[j] in oplist3 or new[j] in oplist2:  #????????????????
                            new1 = new[i:j]
                            new2 = str()
                            for k in new1:
                                if k is not ')':
                                    new2 += k
                            new3 = str()
                            new3 = new[0:i] + new2 + new[j:len(new)]
                            l = i
                            while l >= 0:
                                if new3[l] == '(':
                                    new4 = str()
                                    new4 = new3[:l] + new3[l+1:]
                                    new = new4
                                    i = 0
                                    j = 0
                                    l =- 1
                                else:
                                    l -= 1
                            j = len(new)    
                        else:
                            j = len(new)
                    else:
                        j += 1
            # define the importance of ** 
            elif new[i] in oplist4:
                j = i + 1
                while j < len(new):
                    if new[j] in oplist:
                        if new[j] in oplist4:
                            new1 = new[i:j]
                            new2 = str()
                            for k in new1:
                                if k is not ')':
                                    new2 += k
                            new3 = str()
                            new3 = new[0:i] + new2 + new[j:len(new)]
                            l = i
                            while l >= 0:
                                if new3[l] == '(':
                                    new4 = str()
                                    new4 = new3[:l] + new3[l+1:]
                                    new = new4
                                    i = 0
                                    j = 0
                                    l =- 1
                                else:
                                    l -= 1
                            j = len(new)    
                        else:
                            j = len(new)
                    else:
                        j += 1   
            # define the importance of % and //
            elif new[i] in oplist5:
                j = i + 1
                while j < len(new):
                    if new[j] in oplist:
                        if new[j] in oplist5:
                            new1 = new[i:j]
                            new2 = str()
                            for k in new1:
                                if k is not ')':
                                    new2 += k
                            new3 = str()
                            new3 = new[0:i] + new2 + new3[l+1:]
                            l = i
                            while l >= 0:
                                if new3[l] == '(':
                                    new4 = str()
                                    new4 = new3[:l] + new3[l+1:]
                                    new = new4
                                    i = 0
                                    j = 0
                                    l += 1
                                else:
                                    l -= 1
                            j = len(new)    
                        else:
                            j = len(new)
                    else:
                        j += 1  
            i = len(new)
        else:
           i += 1
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
        
        
    # allow conversion to numerical values (if possible)
    def __int__(self):
        return int(self.variable)
        
    def __float__(self):
        return float(self.variable)    

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
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return False
            
    def __str__(self):
        lstring = str(self.lhs)
        rstring = str(self.rhs)
        
        # TODO: do we always need parantheses?
        return "(%s %s %s)" % (lstring, self.op_symbol, rstring)
        
    def evaluate(self, dic=None):
        lhsEval = self.lhs.evaluate(dic)
        rhsEval = self.rhs.evaluate(dic)
        return eval("%s %s %s" % (lhsEval, self.op_symbol, rhsEval))    
        
class AddNode(BinaryNode):
    """Represents the addition operator"""
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs, '+')

    """ def evaluate(self, var=None):
        ans = BinaryNode(Expression).evaluate(self)
        return ans"""
        
    def minimum(self):
        ans = minimum(self)
        return ans

class SubNode(BinaryNode):
    """Represents the substraction operator"""
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs, '-')

        
    def minimum(self):
        ans = minimum(self)
        return ans  

class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs, '*')

    def minimum(self):
        ans = minimum(self)
        return ans  
        
class DivNode(BinaryNode):
    """Represents the division operator"""
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs, '/')


    def minimum(self):
        ans = minimum(self)
        return ans  

class PowNode(BinaryNode):
    """Represents the power operator"""
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs, '**')


        
    def minimum(self):
        ans = minimum(self)
        return ans  

class ModNode(BinaryNode):
    """Represents the modulus operator"""
    def __init__(self, lhs, rhs):
        super(ModNode, self).__init__(lhs, rhs, '%')


    def minimum(self):
        ans = minimum(self)
        return ans  

class FloorDivNode(BinaryNode):
    """Represents the floor division operator"""
    def __init__(self, lhs, rhs):
        super(FloorDivNode, self).__init__(lhs, rhs, '//')

    def minimum(self):
        ans = minimum(self)
        return ans  
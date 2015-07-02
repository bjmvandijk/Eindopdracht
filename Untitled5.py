def __str__(self):
        lstring = str(self.lhs)
        rstring = str(self.rhs)
        
######### TODO: do we always need parantheses?
        oplist = ['+', '-', '*', '/', '**', '%', '//']
        print(lstring)
        for token in lstring:
            if token in oplist:
                print(int(prec(self.op_symbol)), int(prec(token)))
                if  int(prec(token)) >=int(prec(self.op_symbol)) and int(prec(token))<=2:
                    stringself= "(%s) %s %s" % (lstring, self.op_symbol, rstring)
                    print(stringself, type(stringself), 'prec')
                    return stringself
                else:
                    stringself= "%s %s %s" % (lstring, self.op_symbol, rstring)
                    print(stringself, type(stringself))
                    return stringself
                    
        stringself= "%s %s %s" % (lstring, self.op_symbol, rstring)
        print(stringself, type(stringself))
        return stringself
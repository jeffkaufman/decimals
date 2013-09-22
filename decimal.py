# See http://mathwithbaddrawings.com/2013/08/13/the-kaufman-decimals

import copy

def deg(kd):
    # degree of the list    
    # deg(number) = 0, deg(line) = 1, deg(plane) = 2 ...    
    if isinstance(kd , int): return(0)
    if isinstance(kd , list): return(max([deg(k) for k in kd])+1)

class Decimal(object):
    def __init__(self, s):
  
        def process_subsequence(ss):
            output = list()
            i = 0
            
            while i < len(ss):
                if ss[i].isdigit(): # if digit then append
                    output.append(int(ss[i]))
                elif ss[i] == "(":
                    start = i
                    level = 1
                    while (level > 0) and (i < len(ss)):
                        i += 1
                        if ss[i] == "(": level += 1
                        elif ss[i] == ")": level -= 1
                    if level > 0 and i == len(ss):
                        raise ValueError("Unmatched '('")
                    if i == start + 1:
                        raise ValueError("Parens must not be empty '()'")
                    output.append(process_subsequence(ss[(start+1):i]))
                elif ss[i] == ")":
                    raise ValueError("Unmatched ')'")
                else: 
                    raise ValueError("Invalid character '%s'" % ss[i])
                i += 1
                
            return output
        
        def check_numeric_list(ss):
            if isinstance(ss , list):
                return all([check_numeric_list(i) for i in ss])
            elif isinstance(ss , int) and ss>=0 and ss<=9:
                return True
            else: 
                raise ValueError("Invalid element '%s'" % ss)
                
        
        if isinstance(s, basestring):
            self.sequence = process_subsequence(s)
        elif isinstance(s, list):
            assert check_numeric_list(s)
            self.sequence = s
        else: 
            raise ValueError("Neither string, nor list of digits: %s" % s)

    def fedeg(self): 
    # degree of the first element
        return deg(self.sequence[0])
        
    def split(self, order, repetition = False):
    # returns the first omega^order degits
        def cut_first(ss, repetition=False):
            first_element = ss.pop(0)
            if repetition: ss.append(first_element)
            pass    

        end = copy.deepcopy(self)
        begin = Decimal([])
        
        if deg(self.sequence) <= order:
            raise ValueError("Not long enough.")
        
        while end.fedeg() < order: 
            begin.sequence.append(end.sequence[0])
            cut_first(end.sequence, repetition)
            
        if end.fedeg() == order:
            begin.sequence.append(end.sequence[0])
            cut_first(end.sequence, repetition)
        else: # end.fedeg() > order
            tmp, tmp2 = Decimal(end.sequence[0]).split(order, True)
            begin.sequence += tmp.sequence
            end.sequence[0] = tmp2.sequence
            
        return begin, end

    def __repr__(self):
        tmp = str(self.sequence) # convert list to string
        tmp = tmp.replace('[','(').replace(']',')') # brackets
        tmp = tmp.replace(' ','').replace(',','') # spaces
        return tmp[1:-1] 

    def is_zero(self):
        # test if all digits are zeros    
        def anynonzero(x):
            if isinstance(x, int) and x==0: return(False)
            if isinstance(x, int) and x!=0: return(True)
            if isinstance(x, list): return any([anynonzero(k) for k in x])
        return not anynonzero(self.sequence)

    def __compare__(self, other):
        # compares self to other, returns 1 if greater, 0 if equal, -1 if less        

        def stringerize(x, y):
            return str(x.sequence) + '+' + str(y.sequence)

        def dcompare(x, y, order=0, repetition=False):
        # comparison of two pieces of the length omega^order
            if repetition:
                tried_combinations = set()
                while not(stringerize(x,y) in tried_combinations):
                    tried_combinations.add(stringerize(x,y))
                    d = min(x.fedeg(), y.fedeg())
                    dx, x = x.split(d, True)
                    dy, y = y.split(d, True)
                    compdxy = dcompare(dx, dy, d, False)
                    if compdxy != 0: return compdxy
                return 0
                
            else:
                
                if order==0 and x.sequence[0] > y.sequence[0]: return 1
                if order==0 and x.sequence[0]== y.sequence[0]: return 0
                if order==0 and x.sequence[0] < y.sequence[0]: return -1
        
                while len(x.sequence)>1 or len(y.sequence)>1:
                    d = min(x.fedeg(), y.fedeg())
                    dx, x = x.split(d, False)
                    dy, y = y.split(d, False)
                    compdxy = dcompare(dx, dy, d)
                    if compdxy!=0: return compdxy
        
                if x.fedeg() != y.fedeg():
                    d = min(x.fedeg(), y.fedeg())
                    dx, x = x.split(d, False)
                    dy, y = y.split(d, False)
                    compdxy = dcompare(dx, dy, d)
                    if compdxy!=0: 
                        return compdxy
                    elif len(x.sequence)>0 and not x.is_zero():
                        return 1
                    elif len(y.sequence)>0 and not y.is_zero(): 
                        return -1
                    else: 
                        return 0
                else:
                    d = x.fedeg()
                    x = Decimal(x.sequence[0])
                    y = Decimal(y.sequence[0])
                    return dcompare(x, y, d, True)

        if not isinstance(other, Decimal):
            raise ValueError("Not implemented")
        output = 0
        a = copy.deepcopy(self)
        b = copy.deepcopy(other)
    
        while output == 0 and len(a.sequence)>0 and len(b.sequence)>0:
            d = min(a.fedeg(), b.fedeg())
            da, a = a.split(d, False)
            db, b = b.split(d, False)
            output = dcompare(da, db, d, False)
        
        if output == 0 and len(a.sequence)>0 and not a.is_zero(): output = 1
        if output == 0 and len(b.sequence)>0 and not b.is_zero(): output = -1
        return(output)
        
    def __ne__(self, other):
        return not self == other
        
    def __eq__(self, other):
        return self.__compare__(other) == 0
        
    def __lt__(self, other):
        return self.__compare__(other) == -1

ordered_examples = [
  "(0)1",
  "1",
  "(1)(2)(3)(4)",
  "(1)(3)(3)(4)",
  "2",
  "2(0)(0)1",
  "2(0)1",
  "(2)(2)(3)(4)",
  "(2)3",
  "((2)3)",
  "(2)(3)",
  "54",
  "55",
  "((551)57)4",
  "552",
  "5589",
  "56",
  "8",
  "(81)", 
  "89",
  "9",
  "(9)",
  "((9)1)2",
  "(((9)1)((27)))8",
  "(((9)1)2)7",
  "(((9)1)2)73(((8(46)))5)",
  "(9)3",
  "(9)4",
  "(9)4(8)1",
  "(9)5",
  "(9)(9)",
  "((9))1"
]
   
for i, bigger in enumerate(ordered_examples):
  for j, smaller in enumerate(ordered_examples):
    assert repr(Decimal(smaller)) == smaller
    assert Decimal(smaller) == Decimal(smaller)

    if i > j:
      assert Decimal(smaller) < Decimal(bigger)
      assert not Decimal(smaller) == Decimal(bigger)
      assert not Decimal(bigger) < Decimal(smaller)

print "all tests pass"
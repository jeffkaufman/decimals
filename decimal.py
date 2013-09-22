import copy

def readit(s):
    kd = list()
    i = 0
    while i<len(s):
        if s[i]!="(":
            kd.append(int(s[i]))
        else:
            start = i
            level = 1
            while level>0:
                i+=1
                if s[i]=="(": level+=1
                elif s[i]==")": level-=1
            repetition = readit(s[(start+1):i])
            kd.append(repetition)
        i+=1
    return(kd)

def degree(kd):
    if isinstance(kd , int): return(0)
    if isinstance(kd , list): return(max([degree(k) for k in kd])+1)

def cutFromBeginning(kd,output,order,rep):
    while degree(kd[0]) < order: 
        output.append(kd[0])
	if rep:
	    kd = kd[1:] + [kd[0]]
	else:
	    kd = kd[1:]
	if len(kd) == 0: return None # empty 
    if degree(kd[0]) > order:
        kd[0] = cutFromBeginning(kd[0],output,order,1)
    else: # imply degree(kd[0]) == order
        output.append(kd[0])
        if rep:
	    kd = kd[1:] + [kd[0]]
	else:
	    kd = kd[1:]
    return kd	


def rcompare(u,v):
    def stringerize(a,b): return str(a) + '+' + str(b)
	
    tried = set()	
    if log: print 'Recursive Comparing', u, 'and', v, 'degree', "\n"
    while not(stringerize(u,v) in tried):
        tried.add(stringerize(u,v))    
        d = min(degree(u[0]), degree(v[0]))
	cu = list()
	cv = list()
        u = cutFromBeginning(u, cu, d, 1)
        v = cutFromBeginning(v, cv, d, 1)
        res = dcompare(cu,cv,d)
        if res!=0: return(res)
    return 0

def dcompare(x,y,d):
    if log: print 'Comparing', x, 'and', y, 'degree', d, "\n" 
    if d==0 and x[0]>y[0]: return 1
    if d==0 and x[0]==y[0]: return 0
    if d==0 and x[0]<y[0]: return -1
    while len(x)>1 or len(y)>1:
	   d2 = min(degree(x[0]), degree(y[0]))
           cx = list()
	   cy = list()
           x = cutFromBeginning(x, cx, d2, 0)
	   y = cutFromBeginning(y, cy, d2, 0)
           cxy = dcompare(cx,cy,d2)
	   if cxy!=0: return cxy
    if degree(x[0]) != degree(y[0]):
           d2 = min(degree(x[0]), degree(y[0]))
           cx = list()
	   cy = list()
           x = cutFromBeginning(x, cx, d2, 0)
	   y = cutFromBeginning(y, cy, d2, 0)
           cxy = dcompare(cx,cy,d2)
	   if cxy!=0: return cxy
           if len(x)>0 and anynonzero(x): return 1
	   if len(y)>0 and anynonzero(y): return -1
	   return(0)
    return rcompare(x[0],y[0])

def anynonzero(x):
  if isinstance(x, int) and x==0: return(False)
  if isinstance(x, int) and x!=0: return(True)
  if isinstance(x, list): return any([anynonzero(k) for k in x])

def compare(x,y):
    res = 0
    a = copy.deepcopy(x)
    b = copy.deepcopy(y)
    while res == 0 and len(a)>0 and len(b)>0:
        d = min(degree(a[0]), degree(b[0]))
	ca = list()
	cb = list()
        a = cutFromBeginning(a, ca, d, 0)
	b = cutFromBeginning(b, cb, d, 0)
        res = dcompare(ca,cb,d)
    if res == 0 and len(a)>0 and anynonzero(a): res = 1
    if res == 0 and len(b)>0 and anynonzero(b): res = -1
    return(res)
   
compare(readit('1(36(6))'),readit('13(6)'))

s = "1((0)1((8)6))4(0)1"
ss = readit(s)
rr = list()

ss = cutFromBeginning(ss, rr, 4, 0)
print ss,"\n",rr

ordered_examples = [
  "(0)1",
  "1",
  "(1)(2)(3)(4)",
  "(1)(3)(3)(4)",
  "2",
  "2(0)",
  "2(0)0",
  "2(0)(0)1",
  "2(0)1",
  "(2)(2)(3)(4)",
  "(2)3",
  "(2)(3)",
  "((2)3)",
  "54",
  "55",
  "552",
  "5589",
  "56",
  "((551)57)4", # this isn't where I'd expect this to go
  "8",
  "89",
  "(81)", # this isn't where I'd expect this to go either
  "9",
  "(9)",
  "(9)3",
  "(9)4",
  "(9)4(8)1",
  "(9)5",
  "(9)(9)",
  "((9))1",
  "((9)1)2",
  "(((9)1)2)7",
  "(((9)1)2)73(((8(46)))5)",
  "(((9)1)((27)))8",
]

ke = [readit(s) for s in ordered_examples]

for i in range(len(ke)-1):
    if compare(ke[i], ke[i+1]) == 1:
        print  str2(ke[i]) + ' and ' + str2(ke[i+1]) + "\n"	


swapped = True
j = 0
while swapped:
  j+=1
  print j, "\n"
  swapped = False
  for i in range(len(ke)-1):
	  if compare(ke[i], ke[i+1]) == 1:
		  print 'Swapping', ke[i], 'and', ke[i+1], "\n"
		  ke[i], ke[i+1] = ke[i+1], ke[i]
                  ordered_examples[i], ordered_examples[i+1] = ordered_examples[i+1], ordered_examples[i]
		  swapped = True

log = True


def str2(x):
  return str(x).replace('[','(').replace(']',')').replace(' ','')

for k in ke:
	print(str2(k))

# See http://mathwithbaddrawings.com/2013/08/13/the-kaufman-decimals

class Decimal(object):
  def __init__(self, s, repeated=False, pos=0):
    def eat_subsequence():
      paren_count = 1
      endpos = pos
      while True:
        endpos += 1
        if endpos >= len(s):
          raise ValueError("Reached end of input without matching all parens.")
        if s[endpos] == '(':
          paren_count += 1
        elif s[endpos] == ')':
          paren_count -= 1
          if paren_count == 0:
            self.sequence.append(Decimal(s[:endpos], repeated=True, pos=pos+1))
            return endpos

    self.sequence = []
    self.repeated = repeated
    while True:
      if pos >= len(s):
        break
      c = s[pos]
      if c == '(':
        pos = eat_subsequence()
      elif c == ')':
        raise ValueError("Unmatched ')' at %s" % pos)      
      elif c.isdigit():
        self.sequence.append(int(c))
      else:
        raise ValueError("Invalid character '%s' at position %s" % (c, pos))
      pos += 1

  def __repr__(self):
    r = "".join(repr(x) for x in self.sequence)
    return r if not self.repeated else "(" + r + ")"

  def __ne__(self, other):
    return not self == other

  def __eq__(self, other):
    if type(self) != type(other):
      return False
    if len(self.sequence) != len(other.sequence):
      return False
    if self.repeated != other.repeated:
      return False
    for s, o in zip(self.sequence, other.sequence):
      if s != o:
        return False
    return True

  def __lt__(self, other):
    print "comparing '%s' with '%s'" % (self, other)
    if type(self) != type(other):
      return self.sequence[0] < other
    for s, o in zip(self.sequence, other.sequence):
      if s != o:
        if type(s) == type(0):
          return not o < s
        return s < o
    # they're equal as long as they go, but the shorter one is smaller
    return len(self.sequence) < len(other.sequence)

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
   
for i, bigger in enumerate(ordered_examples):
  for j, smaller in enumerate(ordered_examples):
    assert repr(Decimal(smaller)) == smaller
    assert Decimal(smaller) == Decimal(smaller)

    if i > j:
      assert Decimal(smaller) < Decimal(bigger)
      assert not Decimal(smaller) == Decimal(bigger)
      assert not Decimal(bigger) < Decimal(smaller)

print "all tests pass"

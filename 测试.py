from parseDxf import *

p=Point(1,1)
l=Line((0,0),(2,2))
print(p.isInSegment(l))
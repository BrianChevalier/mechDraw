from Shapes import Node, Element
from math import sqrt
from py.test import raises, main

def test_Node():
	n1 = Node(0.0, 0.0)
	assert isinstance(n1.x, float)
	assert isinstance(n1.y, float)
	
def test_Element():
	x1, x2 = 0, 1
	y1, y2 = 0, 0
	n1 = Node(x1, y1)
	n2 = Node(x2, y2)
	e1 = Element(n1, n2)
	assert e1.length == sqrt((x2-x1)**2+(y2-y1)**2)
	
if __name__ == '__main__':
	main([__file__])

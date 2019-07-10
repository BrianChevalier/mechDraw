from Shapes import *


n = [Node(0, 0, fixity='pin'),
		 Node(1, 0, fixity='pin'),
		 Node(2, 0, fixity='pin')
		]
elems = [Element(n[0], n[1]), Element(n[1], n[2])]

fig, ax = plt.subplots()

for node in n:
	node.plot(scale=0.2)

for elem in elems:
	elem.plot()

plt.grid(True)
plt.axis('equal')
plt.show()

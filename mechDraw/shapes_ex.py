import matplotlib.pyplot as plt
import numpy as np
from Shapes import Point, Arc, Circle, Grid, Line, RotationMatrix


plt.figure()
plt.clf()			

pt0 = Point(0, 0)
pt1 = Point(1, 1)
pt2 = Point(2, 0)
pt0.plot()
pt1.plot()
pt2.plot()

arc = Arc(pt0, 1, 0, 2*np.pi)
arc.plot(arrow='->')

Line(pt0, pt1).plot(arrow='<->')
Line(pt0, pt2).plot(arrow='->')

circle = Circle(pt0, 2)
circle.plot()
plt.axis('equal')


grid = Grid(pt0, pt1, 5)
#grid.plot(color='k', lw=1)

plt.show()

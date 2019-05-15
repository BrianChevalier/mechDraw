import matplotlib.pyplot as plt
import numpy as np

def Canvas():
	"""
	Make a clean preconfigured canvas to draw on
	"""
	fig, ax = plt.subplots()
	
	plt.axis('off')
	plt.axis('equal')
	
	return (fig, ax)

def RotationMatrix(theta):
	"""
	Generates a Rotation Matrix given some theta as input
	
	Args:
		theta (float): angle to rotate by (relative to horizontal)
	
	Returns:
		np.ndarray: The rotation matrix (2x2)
	"""
	cos = np.cos(theta)
	sin = np.sin(theta)
	return np.array([[cos, -sin], 
				     [sin, cos]])

class Point(object):
	"""
	A Point object used to describe points of interest in drawings.
	
	Args:
		x (float): the x position of the Point
		y (float): the y position of the Point
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def asArray(self):
		return np.array([[self.x, self.y]])
		
	def deform(self, F):
		"""
		Deforms the Point using a *Deformation Map*, F.
		
		Args:
			F (np.ndarray): A 2-d numpy array (2x2 matrix)
		
		Returns:
			Point: A *new* Point object
		"""
		pass
		
	def rotate(self, theta, about=None):
		"""
		Rotates the Point about some Point by some amount theta with respect to the horizontal
		
		Args:
			theta (float): Amount to rotate the Point by
		
		Kwargs:
			about (Point): The Point to rotate the point about
		
		Returns:
			Point: A *new* Point object
		"""
		R = RotationMatrix(theta)
		# 2x2 @ (1x2).T
		x0 = self.asArray()
		new = R.dot(x0.T).T
		return Point(new[0, 0], new[0, 1])
	
	def plot(self, color='k', style=None, **kwargs):
		if style is None:
			plt.scatter(self.x, self.y, color=color, **kwargs)
		else:
			plt.scatter(self.x, self.y, **style, **kwargs)
		
	def __repr__(self):
		return f'Point({self.x}, {self.y})'
		
		
class Line(object):
	"""
	A Line is a connection between two points.
	
	Args:
		pt0 (Point): The starting Point
		pt1 (Point): The ending Point
	"""
	def __init__(self, pt0, pt1):
		self.pt0 = pt0
		self.pt1 = pt1
		
	def rotate(self, theta, about=None):
		
		newpt0 = self.pt0.rotate(theta)
		newpt1 = self.pt1.rotate(theta)
		return Line(newpt0, newpt1)
	
	@property
	def length(self):
		x = self.pt1.asArray() - self.pt0.asArray()
		return np.linalg.norm(x)
	
	@property
	def vec(self):
		pt0 = self.pt0
		pt1 = self.pt1
		return pt1.asArray() - pt0.asArray()
		
	@property
	def unVec(self):
		return self.vec/self.length
		
	def plot(self, style=None, arrow=None, lw=1, color='k', **kwargs):
		
		pt0 = self.pt0
		pt1 = self.pt1
		x = [pt0.x, pt1.x]
		y = [pt0.y, pt1.y]
		
		if style is not None:
			plt.plot(x, y, **style)
		else:
			plt.plot(x, y, lw, color, **kwargs)
		
		if arrow is not None:
			scale = 0.1*self.length
			dx = scale*self.unVec[0,0]
			dy = scale*self.unVec[0,1]
		
		# Plot arrow heads
		if arrow == '<->' or arrow == '->':
			start = Point(pt1.x - dx, pt1.y - dy)
			
			if style is None:
				plt.arrow(start.x,
					  start.y,
					  dx,
					  dy,
					  head_width=0.1,
					  head_length=0.1,
					  lw=lw,
					  color=color,
					  length_includes_head=True)
			else:
				plt.arrow(start.x,
					  start.y,
					  dx,
					  dy,
					  head_width=0.1,
					  head_length=0.1,
					  length_includes_head=True)
		
		if arrow == '<->' or arrow == '<-':
			start = Point(pt0.x + dx, pt0.y + dy)
			
			if style is None:
				plt.arrow(start.x,
					  start.y,
					  -dx,
					  -dy,
					  #scale,
					  head_width=0.1,
					  head_length=0.1,
					  lw=lw,
					  color=color,
					  length_includes_head=True)
			else:
				plt.arrow(start.x,
					  start.y,
					  -dx,
					  -dy,
					  head_width=0.1,
					  head_length=0.1,
					  length_includes_head=True)
			
	def __repr__(self):
		return f'Line({self.pt0}, {self.pt1})'

class Arc(object):
	"""
	An circular Arc
	
	Args:
		center (Point): center point of the circle
		radius (float): The radius of the circle
		th0 (float): The initial angle relative to the horizontal
		thf (float): The final angle relative to the horizontal
	
	Kwargs:
		dtheta (float): The incremental theta value to use to connect the arc. Default is pi/100
	"""
	def __init__(self, center, radius, th0, thf, dtheta=np.pi/100):
		self.center = center
		self.th0 = th0
		self.thf = thf
		self.dtheta = dtheta
		self.radius = radius
		
		# calculate start and end point
		x0 = center.x + radius*np.cos(th0)
		y0 = center.y + radius*np.sin(th0)
		self.pt0 = Point(x0, y0)
		xf = center.x + radius*np.cos(thf)
		yf = center.y + radius*np.sin(thf)
		self.pt1 = Point(xf, yf)
	
	def asArray(self):
		
		center = self.center
		th0 = self.th0
		thf = self.thf
		dtheta = self.dtheta
		radius = self.radius
		
		thetas = np.arange(th0, thf+dtheta, dtheta)
		x = center.x + radius*np.cos(thetas)
		y = center.y + radius*np.sin(thetas)
		return np.array([x, y]).T
	
	def plot(self, label=None, lw=1, color='k', arrow=None, fill=False, bbox=None, **kwargs):
		"""
		Kwargs:
			label (string): Text label
			arrow (string): ->, <-, or <->, draws an arrow at start or end of arc
			bbox (dict): dictionary with properties for [FancyBboxPatch](https://matplotlib.org/api/_as_gen/matplotlib.patches.FancyBboxPatch.html#matplotlib.patches.FancyBboxPatch)
		"""
		x, y = self.asArray()[:,0], self.asArray()[:,1]
		plt.plot(x, y, lw=lw, color=color,**kwargs)
		
		if fill == True:
			x = [self.center.x] + list(x) + [self.center.x]
			y = [self.center.y] + list(y) + [self.center.y]
			plt.fill(x, y, '#D3D3D3', zorder=-100)
        
		if arrow is not None:
			dtheta = np.pi/100
			radius = self.radius
			center = self.center
			th0 = self.th0
			thf = self.thf
		
		if arrow == '<->' or arrow == '->':
			x0 = center.x + radius*np.cos(thf-dtheta)
			y0 = center.y + radius*np.sin(thf-dtheta)
			start = Point(x0, y0)
			dx = self.pt1.x - x0
			dy = self.pt1.y - y0
			plt.arrow(start.x,
					  start.y,
					  dx,
					  dy,
					  head_width=0.1,
					  head_length=0.1,
					  lw=lw,
					  color=color,
					  length_includes_head=True)
		
		if arrow == '<->' or arrow == '<-':
			x0 = center.x + radius*np.cos(th0+dtheta)
			y0 = center.y + radius*np.sin(th0+dtheta)
			start = Point(x0, y0)
			dx = self.pt0.x - x0
			dy = self.pt0.y - y0
			plt.arrow(start.x,
					  start.y,
					  dx,
					  dy,
					  head_width=0.1,
					  head_length=0.1,
					  lw=lw,
					  color=color,
					  length_includes_head=True)
		
		if label is not None:
			if bbox is None:
				bbox=dict(alpha=1, color='#FFFFFF')
			thmid = (thf+th0)/2
			x = center.x + radius*np.cos(thmid)
			y = center.y + radius*np.sin(thmid)
			plt.text(x,
							 y,
							 label,
							 fontsize=12,
							 rotation=np.rad2deg(thmid),
							 horizontalalignment='center',
							 bbox=bbox
							 )
		
	def __repr__(self):
		return f'Arc({self.center}, {self.radius}, {self.th0}, {self.thf})'

class Circle(Arc):
	"""
	A Circle object, Inherits from the Arc class.
	
	Args:
		center (Point): Center of the circle
		radius (float): Radius of the circle
	"""
	def __init__(self, center, radius):
		Arc.__init__(self, center, radius, 0, 2*np.pi)
	
	def __repr__(self):
		return f'Circle({self.center}, {self.radius})'


class Rectangle(object):
	"""
	Creates a Rectangle object
	
	Args:
		pt0 (Point): lower left corner of rectangle
		pt2 (Point): upper right corner of rectangle
	"""
	def __init__(self, pt0, pt2, pt1=None, pt3 = None):
		self.pt0 = pt0
		self.pt2 = pt2
		
		if pt1 is not None and pt3 is not None:
			self.pt1 = pt1
			self.pt3 = pt3
		else:
			self.pt1 = Point(pt2.x, pt0.y)
			self.pt3 = Point(pt0.x, pt2.y)
			
	@classmethod
	def from_center(cls, center, b, h):
		"""
		Args:
			center (Point): Center of the shape
			b (float): base/width of rectangle
			h (float): height of rectangle
		"""
		pt0 = Point(center.x-b/2, center.y-h/2)
		pt1 = Point(center.x+b/2, center.y+h/2)
		
		return cls(pt0, pt1)
	
	@classmethod
	def from_array(cls, array):
		"""
		Alternative constructor
		
		"""
		if array.shape[1] != 2:
			raise ValueError('Input must be two column 2darray.')
		x = array[:, 0]
		y = array[:, 1]
		
		pt0 = Point(x[0], y[0])
		pt1 = Point(x[1], y[1])
		pt2 = Point(x[2], y[2])
		pt3 = Point(x[3], y[3])
		return cls(pt0, pt2, pt1=pt1, pt3=pt3)
	
	@property	
	def asArray(self):
		pt0 = self.pt0
		pt1 = self.pt1
		pt2 = self.pt2
		pt3 = self.pt3
		
		pts = [
			[pt0.x, pt0.y],
			[pt1.x, pt1.y],
			[pt2.x, pt2.y],
			[pt3.x, pt3.y],
			[pt0.x, pt0.y]
			]
		return np.array(pts)
	
	def rotate(self, theta):
		
		R = RotationMatrix(theta)
		new = (R @ self.asArray.T).T
		newRect = Rectangle.from_array(new)
		return newRect
		
	def plot(self, lw=1, color='k', **kwargs):
		
		plt.plot(self.asArray[:,0], self.asArray[:,1], lw=lw, color='k')
		
		return self
		
class Square(Rectangle):
	"""
	Creates a Square object
	
	Args:
		pt0 (Point): lower left corner of rectangle
		s (float): side length of the square
	"""
	def __init__(self, pt0, s):
		pt1 = Point(pt0.x+s, pt0.y+s)
		Rectangle.__init__(self, pt0, pt1)
	
	
class Grid(object):
	"""
	A Grid of lines
	
	Args:
		pt0 (Point): lower left corner of grid
		pt1 (Point): upper right corner of the grid
		nLines (int): The number lines internal to the rectangle to draw
	"""
	def __init__(self, pt0, ptN, nLines):
		
		self.pt0 = pt0
		self.ptN = ptN
		self.nLines = nLines
		
		self.dx = (ptN.x - pt0.x)/(nLines + 1)
		self.dy = (ptN.y - pt0.y)/(nLines + 1)
		
		self.N = nLines + 1
		
	def plot(self, color='k', **kwargs):
		
		N = self.N
		pt0 = self.pt0
		ptN = self.ptN
		x0 = pt0.x
		xN = ptN.x
		y0 = pt0.y
		yN = ptN.y
		dx = self.dx
		dy = self.dy
		
		for i in range(N+1):
			plt.plot([x0+i*dx, x0+i*dx], [y0, yN], color=color, **kwargs)
			plt.plot([x0, xN],           [y0+i*dy, y0+i*dy], color=color, **kwargs)


class Bezier(object):
	"""
	
	"""
	def __init__(self, pt0, pt1, pt2, pt3):
		self.pt0 = pt0
		self.pt1 = pt1
		self.pt2 = pt2
		self.pt3 = pt3
		
class IBeam(object):
	"""
	
	Args:
		b
		h
		tf
		tw
		
	Kwargs:
		center (Point): Center of IBeam location
	"""
	def __init__(self, b, d, tf, tw, center=Point(0,0)):
		self.b = b
		self.d = d
		self.tf = tf
		self.tw = tw
		
		self.center = center
		c = center
		
		self.list = [
			[c.x - b/2,  c.y - d/2-tf],
			[c.x + b/2,  c.y - d/2-tf],
			[c.x + b/2,  c.y - d/2   ],
			[c.x + tw/2, c.y - d/2   ],
			[c.x + tw/2, c.y + d/2   ],
			[c.x + b/2,  c.y + d/2   ],
			[c.x + b/2,  c.y + d/2+tf],
			[c.x - b/2,  c.y + d/2+tf], 
			[c.x - b/2,  c.y + d/2   ],
			[c.x - tw/2, c.y + d/2   ],
			[c.x - tw/2, c.y - d/2   ],
			[c.x - b/2,  c.y - d/2   ],
		]
		
		self.pts = [Point(pt[0], pt[1]) for pt in self.list]
	
	@property
	def asArray(self):
		return np.array(self.list)
		
	def plot(self, showPoints=False, lw=2, fillColor=None, zorder=-10, **kwargs):
		
		pts = self.pts + [self.pts[0]] #repeat first point
		lines = []
		for i in range(len(pts)-1):
			lines.append(Line(pts[i], pts[i+1]))
			
		for line in lines:
			line.plot(lw=lw, **kwargs)
		
		if showPoints:
			for pt in self.pts:
				pt.plot()
				
		if fillColor is not None:
			plt.fill(self.asArray[:, 0], self.asArray[:, 1], color=fillColor, zorder=zorder)

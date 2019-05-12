import matplotlib.pyplot as plt
import math
import numpy as np

def RotationMatrix(theta):
	cos = np.cos(theta)
	sin = np.sin(theta)
	
	return np.array([[cos, -sin], 
									 [sin, cos]])

class Point(object):
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def asArray(self):
		return np.array([[self.x, self.y]])
		
	def deform(F):
		pass
		
	def rotate(self, theta, about=None):
		R = RotationMatrix(theta)
		# 2x2 @ (1x2).T
		x0 = self.asArray()
		new = R.dot(x0.T).T
		return Point(new[0, 0], new[0, 1])
	
	def plot(self, **kwargs):
		plt.scatter(self.x, self.y, **kwargs)
		
	def __repr__(self):
		return f'Point({self.x}, {self.y})'
		
		
class Line(object):
	
	def __init__(self, pt0, pt1):
		self.pt0 = pt0
		self.pt1 = pt1
		
	def rotate(theta):
		
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
		
	def plot(self, arrow=None, lw=1, color='k', **kwargs):
		pt0 = self.pt0
		pt1 = self.pt1
		plt.plot([pt0.x, pt1.x], [pt0.y, pt1.y], lw=lw, color=color, **kwargs)
		
		if arrow is not None:
			scale = 0.1*self.length
			dx = scale*self.unVec[0,0]
			dy = scale*self.unVec[0,1]
		
		# Plot arrow heads
		if arrow == '<->' or arrow == '->':
			start = Point(pt1.x - dx, pt1.y - dy)
			plt.arrow(start.x, start.y, dx, dy, scale, head_width=0.1, head_length=0.1,lw=lw,color=color,length_includes_head=True)
		
		if arrow == '<->' or arrow == '<-':
			start = Point(pt0.x + dx, pt0.y + dy)
			plt.arrow(start.x, start.y, -dx, -dy, scale, head_width=0.1, head_length=0.1,lw=lw,color=color,length_includes_head=True)

class Arc(object):
	
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
	
	def plot(self, lw=1, color='k', arrow=None, **kwargs):
		plt.plot(self.asArray()[:,0], self.asArray()[:,1], lw=lw, color=color,**kwargs)
		
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
			plt.arrow(start.x, start.y, dx, dy, head_width=0.1, head_length=0.1,lw=lw,color=color,length_includes_head=True)
		
		if arrow == '<->' or arrow == '<-':
			x0 = center.x + radius*np.cos(th0+dtheta)
			y0 = center.y + radius*np.sin(th0+dtheta)
			start = Point(x0, y0)
			dx = self.pt0.x - x0
			dy = self.pt0.y - y0
			plt.arrow(start.x, start.y, dx, dy, head_width=0.1, head_length=0.1,lw=lw,color=color,length_includes_head=True)


class Circle(Arc):
	
	def __init__(self, center, radius):
		Arc.__init__(self, center, radius, 0, 2*np.pi)
		
								
class Grid(object):
	
	def __init__(self, pt0, ptN, nLines):
		
		self.pt0 = pt0
		self.ptN = ptN
		self.nLines = nLines
		
		self.dx = (ptN.x - pt0.x)/(nLines + 1)
		self.dy = (ptN.y - pt0.y)/(nLines + 1)
		
		self.N = nLines + 1
		
	def plot(self, **kwargs):
		
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
			plt.plot([x0+i*dx, x0+i*dx], [y0, yN], **kwargs)
			plt.plot([x0, xN],           [y0+i*dy, y0+i*dy], **kwargs)



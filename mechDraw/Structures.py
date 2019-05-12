class Node(object):
	
	def __init__(self, x, y, fixity='free'):
		self.x = x
		self.y = y
		
		self.fixity = fixity
	
	def plot(self,
					 s=150,
					 lw=3,
					 scale=0.1,
					 angle=0    #angle of the support
					 ):
		
		if self.fixity == 'pin':
			x1 = self.x
			y1 = self.y
			h = math.sqrt(3)/2 # height of equilateral triangle
			x = [x1, x1 - h/2*scale, x1 + h/2*scale, x1]
			y = [y1, y1 - h*scale,   y1 - h*scale,   y1]
			
			plt.plot(x, y, zorder=-1, lw=lw, c='#000000')
			
		elif self.fixity == 'fixed':
			pass
		
		elif self.fixity == 'roller':
			x1 = self.x
			y1 = self.y
			h = math.sqrt(3)/2 # height of equilateral triangle
			x = [x1, x1 - h/2*scale, x1 + h/2*scale, x1]
			y = [y1, y1 - h*scale,   y1 - h*scale,   y1]
			
			plt.plot(x, y, zorder=-1, lw=lw, c='#000000')
			
			
			
			#x = [x1-val*scale, ]
			#y = 
			#plt.plot(x, y, lw=lw/2)
			
		plt.scatter(self.x, self.y, s=s, lw=lw, c='#FFFFFF')

class Element(object):
	
	def __init__(self, sn, en, width=None):
		self.sn = sn
		self.en = en

	def plot(self, c='#b6b6b6'):
		plt.plot([self.sn.x, self.en.x],
							[self.sn.y, self.en.y],
							lw=10,
							zorder=-1,
							c=c
						)
	@property
	def length(self):
		dx = self.en.x - self.sn.x
		dy = self.en.y - self.sn.y
		return math.sqrt(dx**2 + dy**2)			

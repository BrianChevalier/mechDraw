import matplotlib.pyplot as plt

#Microsoft color pallette

Microsoft = {
	"blue": "#DBE5F1",
	"orange": "#FCE9D9",
	"purple": "#E6E0EC",
	"green": "#EBF0DD",
	"red": "#F2DBDB"
}

Pamplemousse = {
	"darkPink": "#EA7580",
	"pink": "#F6A1A5",
	"yellow": "#F8CD9C",
	"teal": "#1BB6AF",
	"lightBlue": "#088BBE",
	"darkBlue": "#172869"
}

def show(colors, paletteName=None):
	"""
	Plot a color pallette
	
	Args:
		Dictionary of color names and hex values {"color":"HEX"}
	"""
	for i, (color, HEX) in enumerate(colors.items()):
		x = [i, i+1, i+1, i, i]
		y = [0, 0, 1, 1, 0]
		plt.fill(x, y, HEX)
		plt.annotate(color, (i, -0.25))
		plt.annotate(HEX, (i, -0.5))
	plt.axis('tight')
	plt.axis('equal')
	plt.axis('off')
	if paletteName is not None:
		plt.title(paletteName)
	plt.show()

palettes = {
	"Microsoft": Microsoft,
	"Pamplemousse": Pamplemousse
}

def main():
	"""
	Show all available color palettes
	"""
	for paletteName, palette in palettes.items():
		show(palette, paletteName=paletteName)
		
class dotdict(dict):
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__
	
Microsoft = dotdict(Microsoft)
Pamplemousse = dotdict(Pamplemousse)

if __name__ == "__main__":
	main()
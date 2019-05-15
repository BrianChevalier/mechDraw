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

Notability = {
	"darkBlue":"#444FAD",
	"medBlue":"#3498DB",
	"teal":"#14C7DE",
	"lightBlue":"#9DBBD8",
	"green":"#18B092",
	"lightGreen":"#2EDA77",
	"darkPurple":"#8C54D0",
	"lightPurple":"#B09CFF",
	"darkGray":"#515C5D",
	"lightGray":"#C7C3BD",
	"darkPink":"#CF366C",
	"orange":"#EF5F33",
	"darkRed":"#B51415",
	"pink":"#E26A6A",
	"darkOrange":"#CB670F",
	"yellow":"#F1C40F"
}

def show(colors, paletteName=None):
	"""
	Plot a color pallette
	
	Args:
		Dictionary of color names and hex values {"color":"HEX"}
	"""
	plt.figure(figsize=(10,5))
	yy = -2
	cols = 8
	for i, (color, HEX) in enumerate(colors.items()):
		if i % cols == 0:
			yy += 2
		i %= cols
		x = [i, i+1, i+1, i, i]
		y = [yy+0, yy+0, yy+1, yy+1, yy+0]
		plt.fill(x, y, HEX)
		plt.annotate(color, (i, yy-0.25))
		plt.annotate(HEX, (i, yy-0.5))
	plt.axis('tight')
	plt.axis('equal')
	plt.axis('off')
	if paletteName is not None:
		plt.title(paletteName)
	plt.show()

palettes = {
	"Microsoft": Microsoft,
	"Pamplemousse": Pamplemousse,
	"Notability": Notability
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
Notability = dotdict(Notability)


## Styles are dictionaries of key-value pairs
## which are unpacked with ** when passed to plt.plot()
guide = {
	"ls": "--",
	"lw": 1,
	"color": 'k'
}


poi = {
	"color": "#FFFFFF",
	"lw": 2,
	"edgecolors": "#000000",
	"zorder": 10
}

if __name__ == "__main__":
	main()

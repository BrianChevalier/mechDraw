
try:
	import mechDraw.Shapes
	import mechDraw.Styles as sty
except ImportError:
	import sys
	sys.path.append('/private/var/mobile/Containers/Shared/AppGroup/B1C8FA81-2026-48D2-B02B-72FD7AD1A56C/File Provider Storage/Repositories/mechDraw')
	import mechDraw.Shapes as md
	import mechDraw.Styles as sty

import numpy as np
import math
from py.test import raises, main, approx

def test_Point_rotation_trivial():
	pt0 = md.Point(0.0, 0.0)
	pt1 = pt0.rotate(0)
	
	# after rotating 0 rad, should remain the same.
	assert np.allclose(pt0.asArray, pt1.asArray)
	assert str(pt0) == str(pt1)
	
	# rotation about origin, should remain the same
	pt1 = pt0.rotate(np.pi)
	
	assert np.array_equal(pt0.asArray, pt1.asArray)
	assert str(pt0) == str(pt1)
	
def test_Point_rotation_notrivial():
	# Test unit circle angles and points
	pt0 = md.Point(1.0, 0.0)
	
	ths = [np.pi/2,
				 np.pi,
				 3*np.pi/2,
				 2*np.pi
				]
	ans = [md.Point(0.0, 1.0),
				 md.Point(-1.0, 0.0),
				 md.Point(0.0, -1.0),
				 md.Point(1.0, 0.0)
				]
	
	for th, an in zip(ths, ans):
		assert np.allclose(pt0.rotate(th).asArray, an.asArray)
	
def test_Rotate_Point_about_self():
	"""
	Rotating a point about itself yields the same Point
	Also tests multiple angles to rotate about
	"""
	
	a = [0, -1, 1]
	pts = [md.Point(x, y) for x, y in zip(a, a)]
	
	for pt in pts:
		for th in np.arange(0, 2*np.pi, 15):
			assert np.allclose(pt.asArray, pt.rotate(th, about=pt).asArray)
	
def test_Point_Rotation_about_Point():
	pt1 = md.Point(1.0, 0.0).rotate(np.pi/2, about=md.Point(0, 0))
	pt2 = md.Point(0.0, 1.0)
	
	assert np.allclose(pt1.asArray, pt2.asArray)

if __name__ == '__main__':
	main([__file__])

import unittest

from numpy import array
from pulse_signal.waveform import Waveform



class Test_to_deviceManager(unittest.TestCase):

	def test_to_deviceManager(self):
		x0 = 1
		dx = 0.5
		ydata = array([0,2,3])
		test_WF = Waveform(x0,dx,array([0,2,3]))
		self.assertEqual(test_WF.x0, x0)
		self.assertEqual(test_WF.dx, dx)
		self.assertEqual(test_WF.Y[0], ydata[0])

unittest.main()
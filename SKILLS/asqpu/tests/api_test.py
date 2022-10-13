import unittest
import sys
#sys.path.append(r"E:\Jacky\Github\ASQPU\src")
from abandon.api import to_deviceManager


fo = open("./tests/specification_deviceOnly.txt", "r")
spec = fo.read()
fo.close()

class Test_to_deviceManager(unittest.TestCase):

	def test_to_deviceManager(self):
		self.assertEqual(to_deviceManager(spec,["DAC","SG"]), {'DAC': 'SDAWG_1,SDAWG_2,SDAWG_3', 'SG': 'DDSLO_1'})
		test = to_deviceManager(spec,["DAC","SG"])
		print(test)

unittest.main()
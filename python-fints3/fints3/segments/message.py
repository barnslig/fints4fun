# See FinTS_3.0_Formals_2011-06-14_final_version.pdf
from collections import OrderedDict
from fints3.segments import FinTS3Segment

# See B.5.2
class FinTS3Header(FinTS3Segment):
	def __init__(self, version=300):
		self.elements = OrderedDict([
			('head', OrderedDict([
				('identifier', 'HNHBK'),
				('counter', 0),
				('version', 3)
			])),
			('size', 0),
			('version', version),
			('dialog', 0),
			('msg', 0)
		])

	def setSize(self, size):
		selfSize = len(self.toASCII()) + 1
		self.elements['size'] = size + selfSize

	def toASCII(self):
		self.elements['size'] = str(self.elements['size']).zfill(12)
		return super(FinTS3Header, self).toASCII()

# See B.5.3
class FinTS3Footer(FinTS3Segment):
	def __init__(self):
		self.elements = OrderedDict([
			('head', OrderedDict([
				('identifier', 'HNHBS'),
				('counter', 0),
				('version', 1)
			])),
		])

import base64
from fints3.segments.message import *

class FinTS3:
	def __init__(self, server=None, version=300):
		self.server = server
		self.version = version
		self.segments = []

		# these segments are special and have to be controlled by this class
		self.header = FinTS3Header(self.version)
		self.footer = FinTS3Footer()

	def append(self, segment):
		self.segments.append(segment)

	def toASCII(self):
		size = 0
		ascii = ''

		for i, segment in enumerate(self.segments):
			segment.setCounter(i+1)
			s = segment.toASCII()
			ascii += s + "'"
			size += len(s) + 1

		# footer stuff for correct size calculation
		self.footer.setCounter(self.segments[-1].getCounter() + 1 if len(self.segments) > 0 else 1)
		footer = self.footer.toASCII()
		size += len(footer) + 1

		# prepend header with correct size
		self.header.setSize(size)
		ascii = self.header.toASCII() + "'" + ascii

		# append footer
		ascii += footer

		return ascii

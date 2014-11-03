import base64
from fints3.segments.message import *
from fints3.segments.crypto import *

def segmentsToASCII(segments, counter=1):
	ascii = ''

	for segment in segments:
		# do only set counter if is 0; see B.8
		if segment.getCounter() == 0:
			counter += 1
			segment.setCounter(counter)

		s = segment.toASCII()
		ascii += s + "'"

	return counter, ascii

class FinTS3:
	def __init__(self, version=300):
		self.version = version
		self.segments = []
		
		# global segment counter; used for "sub-segments" in the crypto body
		self.i = 1

		# these segments are special and have to be controlled by this class
		self.header = FinTS3Header(self.version)
		self.footer = FinTS3Footer()

	def append(self, segment):
		self.segments.append(segment)

	def toASCII(self):
		self.i, ascii = segmentsToASCII(self.segments)
		size = len(ascii)

		# footer stuff for correct size calculation
		self.footer.setCounter(self.i + 1)
		footer = self.footer.toASCII() + "'"
		size += len(footer)

		# prepend header with correct size
		self.header.setCounter(1)
		self.header.setSize(size + 1)
		ascii = self.header.toASCII() + "'" + ascii

		# append footer
		ascii += footer

		return ascii

class FinTS3PinTan:
	def __init__(self, customer, blz, server=None, version=300):
		self.server = server
		self.fints = FinTS3(version)

		# these segments are embedded into the "crypto"
		self.segments = []

		# these segments are special and have to be controlled by this class
		self.header = FinTS3Header(version)
		self.footer = FinTS3Footer()
		self.crypto_header = FinTS3CryptoHeader(customer, blz)
		self.crypto_body = FinTS3CryptoBody()
		self.fints.append(self.crypto_header)
		self.fints.append(self.crypto_body)

	def append(self, segment):
		self.segments.append(segment)

	def toASCII(self):
		# create the crypto body
		self.fints.i, ascii = segmentsToASCII(self.segments, self.fints.i)
		self.crypto_body.setData(ascii)

		return self.fints.toASCII()


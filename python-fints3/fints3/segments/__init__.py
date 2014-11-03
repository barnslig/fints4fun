from collections import OrderedDict

class FinTS3Segment:
	def __init__(self):
		raise NotImplementedError()

		# Do not forget to keep the correct order!
		self.elements = OrderedDict([
			('head', OrderedDict([
				('identifier', ''),	# Segmentkennung, for example HNHBK or HNHBS
				('counter', 0),		# Automatically incremented by the FinTS3 class
				('version', 0)		# See H.1.3
			]))
		])

	def getCounter(self):
		return self.elements['head']['counter']

	def setCounter(self, counter):
		self.elements['head']['counter'] = counter

	# Parse/encode binary dataelements while ignoring the size
	def __parseBinary(self, DE):
		if DE[0:1] == '@':
			bdata = DE.split('@')
			return bytes(bdata[2], 'ISO-8859-2')
		return DE

	def __encodeBinary(self, DE):
		if type(DE) is bytes:
			return str('@{0}@{1}'.format(len(DE), str(DE, 'ISO-8859-2')))
		return str(DE)

	def fromASCII(self, ascii):
		for i, DG in enumerate(ascii.split('+')):
			key = list(self.elements.keys())[i]

			if type(self.elements[key]) is OrderedDict:

				for ii, DE in enumerate(DG.split(':')):
					kkey = list(self.elements[key].keys())[ii]
					self.elements[key][kkey] = self.__parseBinary(DE)

			else:
				self.elements[key] = self.__parseBinary(DG)

	def toASCII(self):
		ascii = ''

		for key in self.elements.keys():
			if type(self.elements[key]) is OrderedDict:
				for element in self.elements[key]:
					ascii += self.__encodeBinary(self.elements[key][element]) + ':'
				ascii = ascii[:-1]
			else:
				ascii += self.__encodeBinary(self.elements[key])
			ascii += '+'
		ascii = ascii[:-1]

		return ascii

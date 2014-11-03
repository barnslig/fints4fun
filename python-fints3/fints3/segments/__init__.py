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

	def fromASCII(self, ascii):
		for i, DG in enumerate(ascii.split('+')):
			key = list(self.elements.keys())[i]

			if type(self.elements[key]) is OrderedDict:

				for ii, DE in enumerate(DG.split(':')):
					kkey = list(self.elements[key].keys())[ii]
					self.elements[key][kkey] = DE

			else:
				self.elements[key] = DG

	def toASCII(self):
		ascii = ''

		for key in self.elements.keys():
			if type(self.elements[key]) is OrderedDict:
				for element in self.elements[key]:
					ascii += str(self.elements[key][element]) + ':'
				ascii = ascii[:-1]
			else:
				ascii += str(self.elements[key])
			ascii += '+'
		ascii = ascii[:-1]

		return ascii

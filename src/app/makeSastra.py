from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
def Makesastra(input):
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	output   = stemmer.stem(input)
	return output
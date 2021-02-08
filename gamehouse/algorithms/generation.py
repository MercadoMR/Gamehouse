from pickle import dump

def generate_tagger(route):
	import nltk
	from nltk.corpus import cess_esp
	patterns = [ (r".*o$","NMS"),
               (r".*os$","NMP"),
               (r".*a$","NFS"),
               (r".*as$","NFP"),
             ]
	cesp_tsents = cess_esp.tagged_sents()
	td = nltk.DefaultTagger("s")
	tr = nltk.RegexpTagger(patterns, backoff = td )
	tu = nltk.UnigramTagger(cesp_tsents, backoff = tr )
	output = open(route+'tagger.pkl','wb')
	dump(tu,output,-1)
	output.close()



def generate_lemmas(route):
	source = route + 'source_lemmas.txt'
	doc = open(source, encoding = "latin-1")
	lines = doc.readlines()
	doc.close()
	lines = [line.strip() for line in lines]
	lem_pos = {}
	for line in lines:
		if line != "":
			words = line.split() #List with splited line
			t = words[0]
			value = words[-1]
			pos = words[-2][0].lower()
			t = t.replace("#","")
			key = t + " " + pos
			lem_pos[key] = value
	output = open(route+'lemmas.pkl','wb') #web -- write bytes
	dump(lem_pos,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
	output.close()

from dataLayer import DataLayer
import numpy as np
dl = DataLayer()

#TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).

class LogicLayer:
	
	#converts input to output format for adding word
	def changeFormat(documentData,word):
		#calculate tf and idf
		tf = double(word["Count"]) / double(documentData["Words"]["NumWords"])
		numDocs = len(getDocs([word["Text"]])[0]) + 1
		idf = np.log(10 / numDocs)
                #TODO 10 is totalDocs hardcoded till we get that from dds
		#add word to list in proper format
		return {
			"text": word["Text"],
			"documentId": documentData["DocumentID"],
			"document":
			{
				"tf": tf,
				"idf": idf,
				"occurrences": word["Occurences"]
			}
		}

	def getDocs(list_of_ngrams):

		documentList = dl.get(list_of_ngrams)
		return documentList
		# for each document in documentList
			#attach scores (tf and idf) to document

	def removeDoc(documentData):
		#get list of words
		words = []
		for word in documentData["Words"]["WordCounts"]:
			words.append(word["Text"])
		#delete document from words
		return dl.delete_text(documentData["DocumentID"], words)
		# for each word in document data
			#remove document from documentList
			#update idf score for the word
	
	def addDoc(documentData):
		words = []
		for word in documentData["Words"]["WordCounts"]:
			words.append(changeFormat(documentData,word))
		for bigram in documentData["NGrams"]["BiGrams"]:
			words.append(changeFormat(documentData,bigram))
		for trigram in documentData["NGrams"]["TriGrams"]:
			words.append(changeFormat(documentData,trigram))
		return dl.put(words)

		# for each word in document data
			#add document from documentList
			#calculate tf
			#update idf score for the word

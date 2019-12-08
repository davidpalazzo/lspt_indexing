from dataLayer import DataLayer
import numpy as np
dl = DataLayer()

#TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
#  TF-IDF(t) = TF(t) * IDF(t)

#converts input to output format for adding word
def changeFormatAdd(documentData,word):
	#calculate tf
	tf = float(word["Count"]) / float(documentData["Words"]["NumWords"])

	#add word to list in proper format
	return {
		"text": word["Text"],
		"documentId": documentData["DocumentID"],
		"document":
		{
			"tf": tf,
			"occurrences": word["Occurences"]
		}
	}


class LogicLayer:

	def getDocs(self,liAddst_of_ngrams):
		documentGet = dl.get(list_of_ngrams)

		for doc in documentGet:


		docs =




		#calculate idf and tf-idf
		numDocs = 5#len(dl.get([word["Text"]])[0]) + 1
		#TODO 10 is totalDocs hardcoded till we get that from dds
		idf = np.log(10 / numDocs)
		tfidf = tf * idf


		return docs
		# for each document in documentList
			#attach scores (tf and idf) to document

	def removeDoc(self,documentData):
		#get list of words
		words = []
		for word in documentData["Words"]["WordCounts"]:
			words.append(word["Text"])
		#delete document from words
		return dl.delete_text(documentData["DocumentID"], words)
		# for each word in document data
			#remove document from documentList
			#update idf score for the word

	def addDoc(self,documentData):
		words = []
		for word in documentData["Words"]["WordCounts"]:
			words.append(changeFormatAdd(documentData,word))
		for bigram in documentData["NGrams"]["BiGrams"]:
			words.append(changeFormatAdd(documentData,bigram))
		for trigram in documentData["NGrams"]["TriGrams"]:
			words.append(changeFormatAdd(documentData,trigram))
		return dl.put(words)

		# for each word in document data
			#add document from documentList
			#calculate tf
			#update idf score for the word

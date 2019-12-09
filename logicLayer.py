from dataLayer import DataLayer
import numpy as np
dl = DataLayer()

#TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).

#converts input to output format for adding word
def changeFormatAdd(documentData,word):
	#calculate tf and idf
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

	def getDocs(self,list_of_ngrams):

		documentList = dl.get(list_of_ngrams)
		return documentList
		# for each document in documentList
			#attach scores (tf and idf) to document

	def removeDoc(self,documentData):
		#get list of words
		words = []
		for word in documentData["Words"]["WordCounts"]:
			words.append(word["Text"])
		for bigram in documentData["NGrams"]["BiGrams"]:
			words.append(bigram["Text"])
		for trigram in documentData["NGrams"]["TriGrams"]:
			words.append(trigram["Text"])
		#delete document from words in database
		return dl.delete_text(documentData["DocumentID"], words)
		# for each word in document data
			#remove document from documentList
			#update idf score for the word

	def addDoc(self,documentData):
		#get list of words
		words = []
		for word in documentData["Words"]["WordCounts"]:
			words.append(changeFormatAdd(documentData,word))
		for bigram in documentData["NGrams"]["BiGrams"]:
			words.append(changeFormatAdd(documentData,bigram))
		for trigram in documentData["NGrams"]["TriGrams"]:
			words.append(changeFormatAdd(documentData,trigram))
		#add word data to database
		return dl.put(words)

		# for each word in document data
			#add document from documentList
			#calculate tf
			#update idf score for the word

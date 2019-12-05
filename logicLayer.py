from dataLayer import DataLayer
dl = DataLayer()

#TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).

class LogicLayer:

	def getDocs(list_of_ngrams):
		
		documentList = dl.get(list_of_ngrams)
		return documentList
		# for each document in documentList
			#attach scores (tf and idf) to document

	def removeDoc(documentData):
		pass
		# for each word in document data
			#remove document from documentList
			#update idf score for the word

	def addDoc(documentData):
		pass

		# for each word in document data
			#add document from documentList
			#calculate tf
			#update idf score for the word
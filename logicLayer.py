dataLayer = DataLayer()

#TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).


getDocs(list_of_ngrams):
	
	documentList = dataLayer.get(list_of_ngrams)
	# for each document in documentList
		#attach scores (tf and idf) to document

removeDoc(documentData):
	
	# for each word in document data
		#remove document from documentList
		#update idf score for the word

addDoc(documentData):

	# for each word in document data
		#add document from documentList
		#calculate tf
		#update idf score for the word
from dataLayer import DataLayer
import numpy as np

dl = DataLayer()


# TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
#  TF-IDF(t) = TF(t) * IDF(t)

# converts input to output format for adding word
def changeFormatAdd(documentData, word):
    # calculate tf
    tf = float(word["Count"]) / float(documentData["Words"]["NumWords"])

    # add word to list in proper format
    return {
        "text": word["Text"],
        "documentId": documentData["DocumentID"],
        "document":
            {
                "tf": tf,
                "occurrences": word["Occurences"]
            }
    }


''' 
returns:
[
	{
	“_id”:“Cow”,
	“value”:{
		“documents”:
			{
				“docid1”:
					{
						“idf”:0.6931471805599453,
						“occurrences”:[10.0,11.0,12.0],
						“tf”:0.25,
						“ts”:1575842072.742201}
					},
				"docid2":
					{
						“idf”:0.6931471805599453,
						“occurrences”:[10.0,11.0,12.0],
						“tf”:0.25,
						“ts”:1575842072.742201}
					}
			}
	}
]


{
   “NGRAM1”:
    {
       “DocumentId1”:{documentData},
       “DocumentId2”: {documentData},...
    },
    “NGRAM2”:...
}
'''


class LogicLayer:
    def calculateIDF(self, word, numDocsForWord):
        # ask dds for num documents
        totalNumOfDocuments = 10
        # IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
        return np.log(totalNumOfDocuments / numDocsForWord)

    def getDocs(self, list_of_ngrams):
        contents = dl.get(list_of_ngrams)
        ret = dict()
        for content in contents:
            text, documents = content['_id'], content["value"]["documents"]
            idf = self.calculateIDF(text, len(documents))

            ret[text] = dict()
            for doc_id in documents:
                documentData = dict()
                documentData["idf"] = idf
                documentData["tf"] = documents[doc_id]["tf"]
                documentData['tf-idf'] = documentData["tf"] * idf
                ret[text][doc_id] = documentData

    def removeDoc(self, documentData):
        # get list of words
        words = []
        for word in documentData["Words"]["WordCounts"]:
            words.append(word["Text"])
        # delete document from words
        return dl.delete_text(documentData["DocumentID"], words)

    # for each word in document data
    # remove document from documentList
    # update idf score for the word

    def addDoc(self, documentData):
        words = []
        for word in documentData["Words"]["WordCounts"]:
            words.append(changeFormatAdd(documentData, word))
        for bigram in documentData["NGrams"]["BiGrams"]:
            words.append(changeFormatAdd(documentData, bigram))
        for trigram in documentData["NGrams"]["TriGrams"]:
            words.append(changeFormatAdd(documentData, trigram))
        return dl.put(words)

    # for each word in document data
    # add document from documentList
    # calculate tf
    # update idf score for the word

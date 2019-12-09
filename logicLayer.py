from dataLayer import DataLayer
import numpy as np


def changeFormatAdd(documentData, word):
    """
    changeFormatAdd change the input the data format to the one can be accepted by database
    :param documentData:
    :param word: the word of the document data refer to
    :return: the format could be accepted by database
    """
    # TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
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


def calculateIDF(numDocsForWord):
    """
    calculateIDF calculate the IDF for a word
    :param numDocsForWord: number of document associate with a specific word
    :return: the idf calculated
    """
    # ask dds for num documents
    # TODO: currently hard code the number of document as 10
    total = 10
    # IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
    return np.log(total / numDocsForWord)


class LogicLayer:
    """
    LogicLayer supposed to handle all the logic in component,
    for example calculate tf, idf, tf-idf, and transforming format, etc.
    It remain the extensibility of the system, and may involve the multiprocessing in future.

    TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).
    IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
    TF-IDF(t) = TF(t) * IDF(t)
    """

    def __init__(self):
        """
        constructor generate the constant of data layer
        """
        self.dataLayer = DataLayer()

    def getDocs(self, list_of_ngrams):
        """
        getDocs get the list of ngrams from data layer,
        then convert the format that needed by customer

        from data layer
        [
             {
                "_id": "my_word",
                "value": {
                    "documents": {
                        "5da65f292f67f000015296c":
                        {
                            "tf": 0.308,
                            "idf": 2.996,
                            "occurrences": [1, 4, 10, 13]
                            "ts": "20190817xxxx",
                        },

                        "2kn3sdf0012nh19287560d":
                        {
                            "tf": 0.416,
                            "idf": 3.0,
                            "occurrences": [1, 4]
                            "ts": "20190817xxxx",
                        }
                    }
                }
            }
        ]

        transformed format
        {
           "NGRAM1":
            {
               "DocumentId1":{documentData},
               "DocumentId2": {documentData},...
            },
            "NGRAM2":...
        }

        :param list_of_ngrams: list of words that need to query
        :return: the result of list of word
        """

        # get the documents from data layer
        contents = self.dataLayer.get(list_of_ngrams)

        # transform the format
        ret = dict()

        # loop through documents get, calculate the idf
        for content in contents:
            text, documents = content['_id'], content["value"]["documents"]
            idf = calculateIDF(len(documents))

            ret[text] = dict()
            for doc_id in documents:
                documentData = dict()
                documentData["idf"] = idf
                documentData["tf"] = documents[doc_id]["tf"]
                documentData['tf-idf'] = documentData["tf"] * idf
                ret[text][doc_id] = documentData
            return ret

    def removeDoc(self, documentData):
        """
        removeDoc remove the document given
        :param documentData: Words associate with a list of words
        :return: the result from data layer
        """
        # get list of words
        words = []
        for word in documentData["Words"]["WordCounts"]:
            words.append(word["Text"])
        for bigram in documentData["NGrams"]["BiGrams"]:
            words.append(bigram["Text"])
        for trigram in documentData["NGrams"]["TriGrams"]:
            words.append(trigram["Text"])

        # delete document from words
        return self.dataLayer.delete_text(documentData["DocumentID"], words)

    # for each word in document data
    # remove document from documentList
    # update idf score for the word

    def addDoc(self, documentData):
        """
        recieved document data from server layer,
         and transforming to the format could be accpeted by data layer
        :param documentData: documentData from server layer
        :return: the result output from data layer
        """
        words = []
        for word in documentData["Words"]["WordCounts"]:
            words.append(changeFormatAdd(documentData, word))
        for bigram in documentData["NGrams"]["BiGrams"]:
            words.append(changeFormatAdd(documentData, bigram))
        for trigram in documentData["NGrams"]["TriGrams"]:
            words.append(changeFormatAdd(documentData, trigram))
        return self.dataLayer.put(words)

        # for each word in document data
        # add document from documentList
        # calculate tf
        # update idf score for the word

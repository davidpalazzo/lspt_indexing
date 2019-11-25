# where data is of form:
# {
#     "Text": "Lambda",
#     "Count": 5,
#     "Occurences": [
#         1,
#         4,
#         10,
#         13,
#         400,
#         590
#     ]
# }
def addDocument(data):
	pass

#where words is a list of words	
#returns list of documents
def getIntersectingDocs(words):
	let intersectDocs = logicLayer.getDocumentsWithWord(words[0]);
    for i in range(length(words)):
    	if length(intersectDocs)>0:
        # //finds docs that have words[i] in it and 
        # //intersects the resulting docs with the original set of docs
        var docsForWord = getDocumentsWithWord(words[i])
        intersectDocs = intersectDocs.filter(value => docsForWord.includes(value))

#where words is a list of words	
#returns list of documents
def getDocsInOrder(words):
	#use getIntersectingDocs?
	#or use the locations of words by finding first occurrence, x of word0 in intersected doc0
	#then find the location after x in doc0 for word1
	#...
	pass

#length is the length of the ngram desired, length(words)
#returns list of documents
def getDocumentsWithNgram(words,length):
	pass

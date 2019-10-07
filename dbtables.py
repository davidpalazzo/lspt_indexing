import pickle


class serializer:
    @staticmethod
    def get_object(data):
        return pickle.loads(data)

    @staticmethod
    def serialize(obj):
        return pickle.dumps(obj)


class List1:
    # table prefix definition
    prefix = "word_doc_"

    @staticmethod
    def construct_key(self, word):
        return self.prefix + word

    def __init__(self, word):
        self.key = self.construct_key(self, word)
        self.documentList = set()

    def add(self, doc):
        self.documentList.add(doc)

    def is_exist(self, doc):
        return doc in self.documentList

    def get_key(self):
        return self.key

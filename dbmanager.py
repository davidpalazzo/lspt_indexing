import leveldb

from dbtables import List1, serializer


class DBManager:
    # prefix definition

    def __init__(self, location):
        self.location = location
        self.db = leveldb.LevelDB(location)

    def put_word_doc(self, word, doc):

        try:
            data = self.db.Get(bytearray(List1.construct_key(List1, word), 'utf8'))

        # if not exist
        except KeyError:
            list1 = List1(word)
            list1.add(doc)
            self.db.Put(bytearray(list1.key, 'utf8'), serializer.serialize(list1))
            return

        list1 = serializer.get_object(data)
        assert list1.construct_key(List1, word) == list1.get_key()
        list1.add(doc)
        self.db.Put(bytearray(list1.key, 'utf8'), serializer.serialize(list1))

    def get_word_doc(self, word):
        data = self.db.Get(bytearray(List1.construct_key(List1, word), 'utf8'))
        list1 = serializer.get_object(data)
        return list1

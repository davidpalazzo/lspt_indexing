import leveldb

from dbmanager import DBManager

if __name__ == '__main__':
    db = DBManager("./data")

    db.put_word_doc("test", 1)
    db.put_word_doc("test", 2)
    db.put_word_doc("test", 2)
    db.put_word_doc("test", 3)
    db.put_word_doc("test", 4)

    db.put_word_doc("test2", 4)
    db.put_word_doc("test2", 1)

    '''
    get word doc return a serialized object from byte code using 
    pickle, all the method in object could be called.
    '''

    list1 = db.get_word_doc("test")
    print("key: " + list1.get_key())
    print("documents: ")
    print(list1.documentList)
    print("check 1 is exist: ")
    print(list1.is_exist(1))
    print("check 100 is exist: ")
    print(list1.is_exist(100))

    print()
    print()

    list2 = db.get_word_doc("test2")
    print("key: " + list2.get_key())
    print("documents: ")
    print(list2.documentList)
    print("check 1 is exist: ")
    print(list2.is_exist(1))
    print("check 100 is exist: ")
    print(list2.is_exist(4))

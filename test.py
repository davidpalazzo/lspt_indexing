# content of test_sample.py
import pytest
from pymongo import MongoClient
from dataLayer import DataLayer, DataBaseCreateFail
import dataLayer
import logicLayer

'''
A series of tests testing the relevant document function
It tests on an empty database, on single line documents, and multi-line documents
'''

def test_relevant_empty():
    '''
    test relevant on an empty database
    '''
    #test with cow
    #test with jump
    #test with fox
    #test with random

def test_relevant_one_line():
    '''
    Returns single document
    Returns multiple documents
    Returns no documents as none exist
    '''
    #test with cow
    #test with jump
    #test with fox
    #test with random
    assert 1 == 1

def test_relevant_multi_line():
    '''
    Returns single document
    Returns multiple documents
    Returns no documents as none exist
    '''
    
    assert 1 == 1

'''
A series of tests testing the add document function

'''
def test_add_empty():
    '''
    test relevant on an empty database
    '''
    #test with cow
    #test with jump
    #test with fox
    #test with random
    assert 1 == 1
    
def test_add_one_line():
    '''
    add parsed sample data to document see if all there
    do multiple adds
    try to add existing data
    '''
    #test with cow, returns documents 1 and 2
    #test with jumped, returns documents 1 and 3
    #test with fox, returns documents 3 and 4
    #test with random, returns no documents
    assert 1 == 1
    
def test_add_multi_line():
    '''
    add parsed sample data to document see if all there
    do multiple adds
    try to add existing data
    '''
    assert 1 == 1

'''
A series of tests adding 
'''
def test_remove_empty():
    '''
    test remove on an empty database
    '''
    #all tests will return that database is empty
    assert 1 == 1

def test_remove_one_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    #test with document1, all trace of document one removed
    #test with document1, document should not exist
    #test with document5, document should not exist
    #test with document3 and document4, remove all traces
    assert 1 == 1

def test_remove_multiple_lines():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    assert 1 == 1
    
def test_update_empty():
    '''
    test update on empty database
    '''
    #all tests will fail as it's empty
    assert 1 == 1

def test_update_one_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    #test with document1 without cow, cow should no longer be in d1
    #test with document2, without cow, cow should no lonber be in d2
    #test with document3, without white and fox, both should no longer be in d3
    #test with document4, without small, should no longer be in d4
    #attempt to update a document that doesn't exist, should return error
    assert 1 == 1

def test_update_multiplpe_line():
    '''
    remove parsed sample data to document see if all there
    do multiple removes
    try to remove non-existent data
    '''
    #test updating d1 multiple tiems
    #test updating d2 multiple times
    #test updating d3 multiple times
    assert 1 == 1

def test_all():
    #test all commands here
    #return which ones fail, which ones don't
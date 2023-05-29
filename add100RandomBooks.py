#!/usr/bin/env python3

import requests
import json
from faker import Faker


APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic", 
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def getbooks():
    authCreds = (LOGIN, PASSWORD)
    r = requests.get(
        f"{APIHOST}/api/v1/books", 
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            },
        data = json.dumps(book)
    )
    if r.status_code == 200:
        print(f"Book {book} added.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book {book}.")

def GetBooksSize(books):
    size = 0
    for i in books:
        size = size + 1
    return size

def DeleteBookApiCall(id):
    r = requests.delete(
        f"http://library.demo.local/api/v1/books/{id}", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            },
    )
    if r.status_code == 200:
        print(f"Book {id} delete.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}")

def DeleteBooks():
    books = getbooks()
    size = GetBooksSize(books)

    # Delete Five First books
    for i in range(0, 5):
        id = books[i]["id"]
        DeleteBookApiCall(id)
    
    # Delete Five Last books
    for i in range(size-5, size):
        id = books[i]["id"]
        DeleteBookApiCall(id)

# Get the Auth Token Key
apiKey = getAuthToken()

# Using the faker module, generate random "fake" books
fake = Faker()
for i in range(0, 25):
    fakeTitle = fake.catch_phrase()
    fakeAuthor = fake.name()
    fakeISBN = fake.isbn13()
    book = {"id":i, "title": fakeTitle, "author": fakeAuthor, "isbn": fakeISBN}
    # add the new random "fake" book using the API
    addBook(book, apiKey) 
    

DeleteBooks()

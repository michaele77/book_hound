

#-----------------------------------------------------------------------------#
#                                  IMPORTS                                    #
#-----------------------------------------------------------------------------#

import sys
import pickle
import time
import os
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
import requests
import pymongo
from datetime import datetime
import random
import pyautogui
from pynput.keyboard import Key, Controller
from config import get_VPN_password


#-----------------------------------------------------------------------------#
#                             GLOBAL DEFINES                                  #
#-----------------------------------------------------------------------------#



#-----------------------------------------------------------------------------#
#                                Functions                                    #
#-----------------------------------------------------------------------------#


def Mongo_get_book_JSON(book_id):
    return [*bookCol.find({"_id": book_id})][0]

def Mongo_get_user_JSON(user_id):
    return [*userCol.find({"_id": user_id})][0]


# -----------------------------------------------------------------------------#
#                                   MAIN                                       #
# -----------------------------------------------------------------------------#

if __name__ == "__main__":

    ## Let's load in our mongoDB and convert stuff to lists

    dbName = "bookhound_mongodb_toMend"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[dbName]
    print("Got it")

    bookCol = mydb["books"]
    userCol = mydb["users"]

    DB_books = [*bookCol.find()]
    DB_users = [*userCol.find()]

    checkList = []

    ## BEFORE WE LOOP, let's sort through all of the books by order of users pointing to them!
    ## That way we can take care of the most popular books first

    print("Will start sorting now")
    DB_books.sort(key=lambda x:len(x['ratersID']), reverse=True)
    print("finished sorting")
    print("Testing sorting! First book in popularity is {0}".format(DB_books[0]['title']))
    print("Testing sorting! Last book in popularity is {0}".format(DB_books[-1]['title']))

    notCloseFlag = True
    streakCount = 0
    ## Now we can loop through every book ID
    for i, curBook in enumerate(DB_books):
        if 'dateUpdated' in curBook.keys():
            if 'genreWeight' in curBook.keys():
                print("skipping!")
                continue
            curGenreList = curBook['genres']
            ## We have the current genre list, which should be a list of lists with ints and stuff
            ## We want to split it up:
            ##  -List of dictionary objects
            ##      -List of Strings ['A', 'B', 'C']
            ##      -Int for the stringlist ie 736
            if curGenreList == 'NO_GENRES':
                print('updating with no genres!')
                genreObjList = []
                weightSum = 1
            else:
                weightList = [i[1] for i in curGenreList]
                weightSum = sum(weightList)

                genreObjList = []

                for thisTuple in curGenreList:
                    stringList = thisTuple[0]
                    singNum = thisTuple[1] / weightSum

                    dicObj = {}
                    dicObj['genreLabelList'] = stringList
                    dicObj['normalizedWeight'] = singNum

                    genreObjList.append(dicObj)

            myquery = {"_id": curBook['_id']}
            newvalues = {"$set": {"genres": genreObjList, \
                                  "genreWeight": weightSum, \
                                  "dateUpdated": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}}

            bookCol.update_one(myquery, newvalues)

            if i % 100 == 0:
                print('finished with {0} books'.format(i))

        else:
            print('Non-updated book, skipping~~ [{0}]'.format(i))
            continue




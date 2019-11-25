"""
Utitlity functions for summarizing and analyzing data from the litter database. Used with a jupyter notebook.

Creates folder structures, groups data, creates graphs and outputs JSON format data.

See the repo @hammerdirt/three_year_final for the accompanying notebooks and intended use.

Contact roger@hammerdirt.ch or @hammerdirt

"""
import os
import json
import requests
import pandas as pd
import numpy as np
import datetime

idx = pd.IndexSlice

def makeDirectory(needed, here):
    """
    Makes a directory with names from a list.
    """
    for folder in needed:
        place = here +"/"+ folder
        os.mkdir(place)

def check_for_folders(folders, here):
    """
    Checks the names of the folder list against the currrent directory. If the result is not
    an empty set then the required names are added to the directory structure.
    """

    current_dir = os.listdir()
    curr_dir_set = set(current_dir)
    folder_set = set(folders)
    needed = folder_set.difference(curr_dir_set)
    if needed:
        makeDirectory(needed, here)
        print("Added folders to the local working directory")
    else:
        print("Directory already in place")

def make_folders(folders, here):
    """
    A dcitionary for locating folders in the directory.
    """
    my_folders = {}
    for folder in folders:
        place = here +"/"+ folder
        my_folders[folder] = place
    return my_folders
def getTheData(end_points):
    """
    Takes an api url and returns a response object
    """
    data = {}
    for pair in end_points:
        data[pair[0]] = requests.get(pair[1])
    return data
def writeTheData(aDict, here):
    """
    Writes the response objects to local in JSON
    """
    file_names = list(aDict.keys())
    outPut = []
    for name in file_names:
        file_name = here + '/Data/'+name+ ".json"
        outPut.append(file_name)
        with open(file_name, 'w') as outfile:
            json.dump(aDict[name].json(), outfile)

    print(outPut)

def putTheDataToLocal(end_points, here):
    """
    Gets the data and writes it to a local JSON file
    """
    the_dict = getTheData(end_points)
    writeTheData(the_dict, here)
def jsonFileGet(this_path):
    """
    Reads the local JSON in
    """
    with open(this_path, 'r') as infile:
        data = json.load(infile)
        return data
def getIndexValues(aDf, anInt):
    return aDf.index.get_level_values(anInt).unique()
def getSummaryByKeyValue(aDf, anInt):
    aList = list(getIndexValues(aDf, anInt))
    theSummaries = {}
    for key in aList:
        aSummary = aDf.loc[key].describe().to_dict()
        theSummaries.update({key:aSummary["pcs_m"]})
    return aList, theSummaries
def convertStringToDate(aTuple):
    convertedDates = []
    for pair in aTuple:
        newPair = (datetime.datetime.strptime(pair[0], "%Y-%m-%d"), datetime.datetime.strptime(pair[1], "%Y-%m-%d"))
        convertedDates.append(newPair)
    return convertedDates
def getSummaryByKeyValueMulti(aDf, anInt):
    aList = list(getIndexValues(aDf, anInt))
    theSummaries = {}
    for key in aList:
        aSummary = aDf.loc[idx[:,key,:,:], :].describe().to_dict()
        theSummaries.update({key:aSummary["pcs_m"]})
    return aList, theSummaries
def makeListOfBars(aDict, aKey):
    aList = []
    theKeys = aDict.keys()
    for key in theKeys:
        values = aDict[key][aKey]
        aList.append([key,values])
    return aList
def sortInReverse(the_data, anIndex):
    the_data_sorted = sorted(the_data, key=lambda row: row[anIndex], reverse=True)
    return the_data_sorted
# def stackBarChartFromSummary(aDict, aKey, anIndex):
#     the_data = makeListOfBars(aDict, aKey)
#     the_data_sorted = sortInReverse(the_data, anIndex)
#     iterateBarchartBlocks(the_data_sorted)

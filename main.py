import argparse
import os
import sys
from os import path
from datetime import datetime

def runOverFolders(dir, deleteBefore, list):
    deleteList = []
    for x in os.listdir(dir):
        location = path.join(dir, x)
        if(path.isdir(location)):
            if(runOverFolders(location, deleteBefore, list)):
                deleteList.append(location)
        elif (deleteBefore.timestamp() > path.getmtime(location)):
            deleteList.append(location)

    list.extend(deleteList)
    if (set(listDirWithFullPath(dir)) == set(deleteList)):
        return True


def listDirWithFullPath(path):
    return [os.path.join(path, file) for file in os.listdir(path)]

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def runDeleteBot(dir, datetime):
    toDelete = []

    runOverFolders(dir, datetime, toDelete)

    folderList = []
    fileList = []

    countErrors = 0
    countFiles = 0
    countFolders = 0
    fileSize = 0

    for x in toDelete:
        if(os.path.isdir(x)):
            folderList.append(x)
        else:
            fileList.append(x)
    for f in fileList:
        countFiles += 1
        fileSize += os.stat(f).st_size
        #print(str(datetime.fromtimestamp(path.getmtime(f)).isoformat()) + "   " + f)
        os.remove(f)

    print(len(folderList))
    print(folderList)
    print(len(set(folderList)))

    for folder in folderList:
        print(folder)
        countFolders += 1
#        try:
#            os.removedirs(folder)
#        except WindowsError as error:
#            print(error)
#            countErrors += 1

    endSize = get_dir_size(usrDir)

    print(f"Deleted {countFiles} Files and {countFolders} Folders with {countErrors} Errors")
    print(f"Deleted a total of {fileSize} Bytes / {fileSize / (1024*1024)} MB / {fileSize / (1024*1024*1024)} GB")
    print(f"End size of {usrDir}  = {endSize} Bytes / {endSize / (1024*1024)} MB / {endSize / (1024*1024*1024)} GB")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Simple delete Bot")

    parser.add_argument('dir',  help="A Directory in your File-System", type=str)
    parser.add_argument('date',  help="A date in ISO 8601 Format", type=str)

    args = parser.parse_args()

    usrDatetime = args.date
    usrDir = args.dir

    try:
        usrDatetime = datetime.fromisoformat(usrDatetime)
    except:
        print(usrDatetime + " is not a valid ISO date")
        exit()
    if not path.exists(usrDir):
        print(usrDir + " is not a valid Path.")

    runDeleteBot(usrDir, usrDatetime)



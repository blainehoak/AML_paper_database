import requests
import json


def check_update():
    # pull json file containing papers information
    papersreq = requests.get(
        "https://nicholas.carlini.com/writing/2019/advex_papers.json"
    )
    # get json format
    webpapersj = papersreq.json()

    # now loading in local version of the json file
    with open("advex_papers.json") as f:
        locpapersj = json.load(f)

    if len(locpapersj) == len(webpapersj):
        print("Local copy is already up to date :)")
    else:
        # updating the local copy
        print("Local copy out of date, calling update method.")
        update(locpapersj, webpapersj)


def update(localcopy, webcopy):

    # assuming that if the paper is out of date, new new content has been added to the top
    updatelen = len(webcopy) - len(localcopy)

    # getting the missing papers
    missingcontent = webcopy[:updatelen]
    print("{} new papers available, updating local copy.".format(len(missingcontent)))

    # updating our copy
    localcopy = missingcontent + localcopy

    with open("advex_papers.json", "w") as fd:
        json.dump(localcopy, fd)

    print("Local copy updated :)")

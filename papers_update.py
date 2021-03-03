import requests
import json
import os


def check_update():
    # pull json file containing papers information
    papersreq = requests.get(
        "https://nicholas.carlini.com/writing/2019/advex_papers.json"
    )
    # get json format
    webpapersj = papersreq.json()

    # checking to see if there is a local copy
    if os.path.exists("advex_papers.json") == False:
        print("Creating advex_papers.json file")
        # setting our local copy to be empty and updating the entire file
        update([], webpapersj)
    else:
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

    # calculating the relative date in quarters
    updatedcontent = quartercalc(missingcontent)
    # updating our copy
    localcopy = updatedcontent + localcopy

    with open("advex_papers.json", "w") as fd:
        json.dump(localcopy, fd)

    print("Local copy updated :)")


def quartercalc(content):
    counter = 0
    for paper in content:

        # getting dates and date info
        date = paper[0]
        splitdate = date.split("-")
        year = int(splitdate[0])
        month = int(splitdate[1])

        # getting the quarter number for that year
        quarter = int((month - 1) / 3)

        # four quarters in a year
        yearquarters = (2021 - year) * 4

        # assuming we are in 2nd quarter of year 2021
        totalquarters = yearquarters + (1 - quarter)
        paper[0] = [date, totalquarters]
        content[counter] = paper
        counter += 1

    return content

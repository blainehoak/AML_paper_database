import json
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import papers_update

# TODO: figure out rate of requests that can be made before captcha check initiates
# first making sure that our local json object is up to date with https://nicholas.carlini.com/writing/2019/all-adversarial-example-papers.html, returning the up to date list
papers_update.check_update()

with open("advex_papers.json") as f:
    papersj = json.load(f)

counter = 0
# cycling through all the papers
for currentpaper in papersj:
    # skipping over the current paper if we already have the citation information
    if len(currentpaper) == 6:
        continue
    # link is stored in the first element
    arxreq = requests.get(currentpaper[1])
    # using beautiful soup to parse html text
    arxsoup = BeautifulSoup(arxreq.text, "html.parser")

    # parsing the html doc for the google scholar citation link
    scholarlinklist = arxsoup.find_all(class_="cite-google-scholar")

    scholarlink = scholarlinklist[0]["href"]

    # now moving over to google scholar, need to make sure the requests don't cap out, can only make a request every 10 seconds
    time.sleep(10)
    scholarreq = requests.get(scholarlink)
    scholarsoup = BeautifulSoup(scholarreq.text, "html.parser")

    # doing captcha check to make sure we haven't processed too many requests
    captchacheck = scholarsoup.find_all(attrs={"id": "captcha-form"})

    if len(captchacheck) != 0:
        print("Too many requests have been made for this IP address")
        break

    # if there are nay google scholar citations, there will be an href to the citers
    citeref = scholarsoup.find_all(href=re.compile("cites"))

    # checking if the link produced any results, if not, we assume the paper has 0 citations
    # if google scholar has a result for the paper, but the paper has no citations this list will also have a length of zero
    if len(citeref) != 0:
        # getting the string from the list, extracting the text
        citetext = citeref[0].text

        # splitting the string and getting the last element, which will contain the number of citations, then casting that as an int
        numcites = int(citetext.split()[-1])
    else:
        numcites = 0

    print("{} citations found for {}".format(numcites, currentpaper[2]))

    # appending the number of citations to the end of the json file
    currentpaper.append(numcites)

    # storing the citation information back into the papersj array
    papersj[counter] = currentpaper
    counter += 1
    print("Total Papers Checked:", counter)

# dumping the updated array into the json file
with open("advex_papers.json", "w") as outfile:
    json.dump(papersj, outfile)

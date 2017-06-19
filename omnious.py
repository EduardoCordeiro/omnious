from urllib.request import urlopen
from html.parser import HTMLParser
from urllib import parse

import datetime
import sys

class LinkParser(HTMLParser):

    # looking for links
    def handle_starttag(self, tag, attrs):

        if tag == 'a' or tag == 'link':

            for(key, value) in attrs:

                if key == 'href':
                    # grabbing the new url
                    #combining relative and base url
                    newUrl = parse.urljoin(self.baseUrl, value)

                    # Store in the collection
                    self.links = self.links + [newUrl]

    def getLinks(self, url):

        # Collection of links stored
        self.links = []

        self.baseUrl = url

        response = urlopen(url)

        htmlString = ""

        # Check all the responses.
        # Let's actually log all of them and see what is interesting after
        contentType = response.getheader('Content-Type')

        #print("Response from link is =", contentType, '\n')

        if contentType.find('text/html') > -1:

            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")

            # Printing to a file all the information for now
            #fileWriter('text/html', htmlString)

        elif contentType.find('text/plain') > -1:

            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")

            # Printing to a file all the information for now
            #fileWriter('text/plain', htmlString)

        elif contentType.find('text/css') > -1:

            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")

            # Printing to a file all the information for now
            #fileWriter('text/css', htmlString)

        else:
            return htmlString,[]

        #sys.stdout.flush()
        #print("feed")
        self.feed(htmlString)
        #print("feeded")
        return htmlString, self.links

def fileWriter(contentType, data):

    if contentType == 'text/html':

        fileObject = open('htmlFile', "r+")

    elif contentType == 'text/plain':

        fileObject = open('plainFile', "r+")

    elif contentType == 'text/css':

        fileObject = open('cssFile', "r+")

    else:
        print("Did not find a suitable Content Type to store")

    fileObject.write(data)

    fileObject.close()

def websiteLog(url):

    # Check the date
    # Purely cosmetical, looks nice in the file
    dateCheck = open("websiteLog", "r")

    lines = dateCheck.readlines()

    dateCheck.close()

    siteFile = open('websiteLog', "a+")

    # Trailing \n in the files really makes this line ugly
    if str(datetime.date.today()) + "\n" not in lines:
        siteFile.write(str(datetime.date.today()))
        siteFile.write("\n")

    siteFile.write(url)
    siteFile.write("\n")

    siteFile.close()

def spider(url, word, maxPages):

    pagesToVisit = [url]

    pagesVisited = 0

    foundWord = False

    # Main Loop
    # Create a LinkParser and get all the links
    # Search for the word in that page
    while pagesVisited < maxPages and pagesToVisit != [] and not foundWord:

        pagesVisited = pagesVisited + 1

        url = pagesToVisit[0]

        pagesToVisit = pagesToVisit[1:]

        try:

            print(pagesVisited, url)

            websiteLog(url)

            parser = LinkParser()

            data, links = parser.getLinks(url)

            # index of the word we are looking for
            index = data.find(word)

            #dataSplit = data.split("\n")

            if word in data:
                foundWord = True

            # Add the pages that we visited to the end of our collection
            # of pages to visit:

            pagesToVisit = pagesToVisit + links

            # update the progress on every site
            sys.stdout.flush()

        except:
            # deal with errors here, i want to know what this is
            print("Failed with error ....")

    if  foundWord:
        print("The word:", word, " was found @", url)
    else:
        print("The word:", word, "was not found.")

def main():

    # Parse args
    # Usage: URL  WORD  MAXPAGES
    startingUrl = "http://" + str(sys.argv[1])

    startingWord = str(sys.argv[2])

    maxPageCount = int(sys.argv[3])

    print("Searching", startingUrl, "for word", startingWord, "with level", maxPageCount, "\n")

    spider(startingUrl, startingWord, maxPageCount)


if __name__ == '__main__':
    main()

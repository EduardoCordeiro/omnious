from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

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

        # Check all the responses.
        # Let's actually log all of them and see what is interesting after
        contentType = response.getheader('Content-Type')

        print("Response from link is =", response.getheader('Content-Type'), '\n')

        if contentType.find('text/html') > -1:

            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")

            # Printing to a file all the information for now
            fileWriter('text/html', htmlString)

            self.feed(htmlString)

            return htmlString, self.links

        elif contentType.find('text/plain') > -1:

            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")

            # Printing to a file all the information for now
            fileWriter('text/plain', htmlString)

            self.feed(htmlString)

            return htmlString, self.links

        elif contentType.find('text/css') > -1:

            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")

            # Printing to a file all the information for now
            fileWriter('text/css', htmlString)

            self.feed(htmlString)

            return htmlString, self.links

        else:
            return "",[]

def fileWriter(contentType, data):

    print("Printing to file!\n")

    if contentType == 'text/html':

        fileObject = open('htmlFile', "w+")

    elif contentType == 'text/plain':

        fileObject = open('plainFile', "w+")

    elif contentType == 'text/css':

        fileObject = open('cssFile', "w+")

    else:
        print("Did not find a suitable Content Type to store")

    fileObject.write(data)

    fileObject.close()

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

            print(pagesVisited, "Visiting:", url)

            parser = LinkParser()

            data, links = parser.getLinks(url)

            if data.find(word) > -1:

                foundWord = True

                # Add the pages that we visited to the end of our collection
                # of pages to visit:

            pagesToVisit = pagesToVisit + links
            print("Page Visited Succesfully.")

        except:
            # deal with errors here, i want to know what this is
            print("Failed with error ....")

    if  foundWord:
        print("The word: ", word, " was found @ ", url, ".")
    else:
        print("The word: ", word, " was not found.")

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

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class LinkParser(HTMLParser):

    # looking for links
    def handle_starttag(self, tag, attrs):

        if tag == 'a':

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

        if response.getheader('Content-Type') == 'text/html':

            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")

            self.feed(htmlString)

            return htmlString, self.links

        else:

            return "",[]

def spider(url, word, maxPages):

    pagesToVisit = [url]

    pagesVisited = 0

    foundWord = False

    # Main Loop
    # Create a LinkParser and get all the links
    # Search for the word in that page
    #

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

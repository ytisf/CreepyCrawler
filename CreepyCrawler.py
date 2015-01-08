#!/usr/bin/python

import re
import sys
import urllib
import urllib2
from progressbar import *
from BeautifulSoup import BeautifulSoup


class CreepyCrawler():
    def __init__(self):
        self._Search = ""
        self._ResPerPage = 100

    def get_links(self, query, pages=0, site=""):
        """
        Google for a query and get a list of links.
        :param query: Search query.
        :param pages: Amount of pages to search.
        :param site: If the search should be restricted to a domain.
        :return:Returns list of links from Google.
        """
        results = []

        pages *= self._ResPerPage            # Since Google likes working with offsets instead of pages.

        if pages != 0:
            print "Starting search for '%s' over %s pages." % (query, pages/self._ResPerPage)
        else:
            print "Starting search for '%s' over 1 page." % query

        fh = open(self._Search + "all_links.txt", "w")

        for i in range(0, pages, 100):

            if i != 0:
                print "Getting page %s of %s." % (i/self._ResPerPage+1, pages/self._ResPerPage)
            else:
                print "Getting first page."

            if site == "":
                address = "http://www.google.com/search?q=%s&num=%s&hl=en&start=%s" % ((urllib.quote_plus(query)),self._ResPerPage,  i)
            else:
                address = "http://www.google.com/search?q=%s%s&num=%s&hl=en&start=%s" % (urllib.quote_plus(query), "+site:" + str(site),self._ResPerPage, i)

            request = urllib2.Request(address, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4_CrCrw) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
            urlfile = urllib2.urlopen(request)
            page = urlfile.read()
            soup = BeautifulSoup(page)

            for li in soup.findAll('li', attrs={'class': 'g'}):
                slink = li.find('a')
                results.append(slink['href'])
                fh.write(slink['href'] + "\n")

        fh.close()
        return results

    def get_source(self, links):
        """
        Gets the HTML source for each link.
        :param links: Array of links.
        :return:Array of sources
        """
        source_array = []
        failed = []

        print("Getting %s pages." % len(links))
        widgets = ['Getting HTML: ', Percentage(), ' ', Bar(marker='-', left='[', right=']'), ' ', ETA(), ' ', FileTransferSpeed()]

        pbar = ProgressBar(widgets=widgets, maxval=len(links))
        pbar.start()

        for i in range(1, len(links), 1):
            try:
                response = urllib2.urlopen(links[i])
                source_array.append(response.read())
            except:
                failed.append(i)

            pbar.update(i)
            time.sleep(0.01)

        pbar.finish()
        print ""
        return source_array

    def extract_emails(self, sources):
        """
        Extract emails (regex) from an array.
        :param sources:an array to search for in.
        :return:an array of emails.
        """
        fh = open(self._Search + "all_emails.txt", "w")

        emails = []
        email_regex = r'([A-Za-z0-9\.\-\_]+@[A-Za-z0-9\.\-\_]+\.[A-Za-z]+)'

        for source in sources:
            a = re.findall(email_regex, source)
            for each in a:
                emails.append(each)
                fh.write(each + "\n")

        fh.close()

        s = []
        for i in emails:
            if i not in s:
                s.append(i)

        fh = open(self._Search + "filtered_emails.txt", "w")
        for mail in s:
            fh.write(mail + "\n")
        fh.close()

        return emails

    def RunSearchOnQuery(self, query, pages=0, search_results_per_page=100):
        """
        A dummy function to bundle it all together.
        :param query: Search query
        :param pages: Number of pages
        :param search_results_per_page: How many results per page. Default is 100.
        :return:List of emails
        """

        self._Search = query
        self._ResPerPage = search_results_per_page

        links = self.get_links(query, pages)
        sources = self.get_source(links)
        return self.extract_emails(sources)


if __name__ == "__main__":
    print("This should not be ran as a standalone.\nCall it as a method.")
    sys.exit(1)

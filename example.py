#!/usr/bin/python

"""
A simple python script to crawl Google and get email.
Just couldn't find a normal functioning script so there you go.
"""

import CreepyCrawler

if __name__ == '__main__':

    CripHandlr = CreepyCrawler.CreepyCrawler()

    appendix = "Digital Whisper"
    emails = CripHandlr.RunSearchOnQuery(appendix, 1, 20)

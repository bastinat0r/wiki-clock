#!/usr/bin/python2.7

import pyttsx
import wikipedia
import argparse
from time import sleep
from datetime import datetime
from apscheduler.scheduler import Scheduler

#argument parser
parser = argparse.ArgumentParser(description='Wiki-Clock')
parser.add_argument('-l', '--lang', help='wikipedia language to use', default='en')

#initialisation
engine = pyttsx.init()
parser.add_argument('-r', '--rate', help='reading speed in words per minute, defaults to 170', default='170')
parser.add_argument('-v', '--voice', help='reading voice', default="english")
parser.add_argument('-s', '--silent', help='silent mode - text output only', action="store_true")
parser.add_argument('--loop', help='read stuff all the time', action="store_true")

voices = [voice.id for voice in engine.getProperty('voices')]
voices = ", ".join(voices)
parser.epilog = "Aviable options for --voice are: %s" %voices

args = parser.parse_args()
print args
wikipedia.set_lang(args.lang)
engine.setProperty('rate', int(args.rate))
engine.setProperty('voice', args.voice)

# Start the scheduler
sched = Scheduler()
sched.start()

def say(text):
    if args.silent:
        print "say: %s" %text
    else:
        engine.say(text)
        engine.runAndWait()
    sleep(0.5)


def read_clocktime():
    """ read n articles from the wikipedias

    """
    d = datetime.now()
    hours = d.hour
    if hours % 12 == 0:
        hours = 12
    else:
        hours = hours % 12

    for _ in range(hours):
        read_article()
        sleep(1)

def read_article():
    """
    read random article
    """
    article_title = None
    options = None
    while article_title == None:
        if options == None or options == []:
            article_title = wikipedia.random()
        else:
            article_title = options.pop()
        try:
            summary = wikipedia.summary(article_title)
            options = None
        except wikipedia.exceptions.DisambiguationError, e:
            print "DISAMBIGUATION: %s" %article_title
            if options == None:
                options = e.options
            article_title = None
    print(article_title)
    say(article_title)
    say(summary)

if not args.loop:
    sched.add_cron_job(read_clocktime, minute=0)

if __name__ == '__main__':
    if args.loop:
        while True:
            read_article()
            sleep(1)
    while True:
        sleep(60)


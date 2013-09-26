import pyttsx
import wikipedia
from time import sleep
from datetime import datetime
from apscheduler.scheduler import Scheduler

#initialisation
engine = pyttsx.init()
engine.setProperty('rate', 170)
engine.setProperty('voice', 'english')
#wikipedia.set_lang('simple')

# Start the scheduler
sched = Scheduler()
sched.start()


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

def read_article():
    """
    read random article
    """
    article_title = wikipedia.random()
    try:
        summary = wikipedia.summary(article_title)
    except wikipedia.exceptions.DisambiguationError, e:
        print "DISAMBIGUATION: %s" %article_title
        article_title = e.options[0]
        summary = wikipedia.summary(e.options[0])
    finally:
        print article_title
    engine.say(article_title)
    engine.runAndWait()
    sleep(0.5)

    engine.say(summary)
    engine.runAndWait()

sched.add_cron_job(read_clocktime, minute=0)

if __name__ == '__main__':
    read_clocktime()
    while True:
        sleep(60)


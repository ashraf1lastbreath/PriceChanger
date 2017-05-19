# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from tw_fetch import tw_fetch
from tw_post import tw_post
import sys

sched = BlockingScheduler()


@sched.scheduled_job('interval', id='initial_fun', minutes= 10)
def initial_fun( ):
    tw_fetch( )


@sched.scheduled_job('interval', id='final_fun', hours= 1)
def final_fun( ):
    tw_post( )


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
    sys.stdout.flush()

sched.start()
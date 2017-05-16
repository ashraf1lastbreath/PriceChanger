# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
from initial import initial
from final import final
import sys

sched = BlockingScheduler()


@sched.scheduled_job('interval', id='initial_fun', minutes= 5)
def initial_fun( ):
    initial( )


@sched.scheduled_job('interval', id='final_fun', hours= 1)
def final_fun( ):
    final( )


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
    sys.stdout.flush()

sched.start()

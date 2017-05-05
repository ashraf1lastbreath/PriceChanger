from apscheduler.schedulers.blocking import BlockingScheduler
from initial import initial

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    initial()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')
    sys.stdout.flush()

sched.start()
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .jobs import *

already_started = None


def start_2():
    global already_started
    if already_started: return

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_sms, trigger=CronTrigger(hour=19, minute=41))
    scheduler.start()
    already_started = True

    # jobs = scheduler.get_jobs()
    # for job in jobs:
    #     print(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}")
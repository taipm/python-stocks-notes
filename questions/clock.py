from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import UTC
import questions.teleBot as Bot
sched = BlockingScheduler()

print('Schedule')
@sched.scheduled_job('interval', minutes=1, timezone=UTC)
def timed_job():
    print('Schedule')
    Bot.send_message('Trong giờ')
    # if(IsRunTime()):
    #     Bot.send_message('Trong giờ')
    # else:
    #     Bot.send_message('Ngoài giờ')


#job = scheduler.add_job(myfunc, 'interval', minutes=2)

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')


sched.start()

from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import UTC
import questions.teleBot as Bot
sched = BlockingScheduler()

print('Schedule')
@sched.scheduled_job('interval', minutes=1, timezone=UTC)
def timed_job():
    print('Schedule')
    Bot.send_message('Trong giờ')

#sched.start()

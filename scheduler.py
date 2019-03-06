from apscheduler.schedulers.blocking import BlockingScheduler

def some_job():
    print("Decorated job")

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', minutes=2)
scheduler.start()
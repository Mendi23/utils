# first couple of options are from: https://martinheinz.dev/blog/39

#--------------------
# built-in module: `sched`. best for deferred tasks in the program
import sched, threading, time
scheduler = sched.scheduler(time.time, time.sleep)
def some_deferred_task(name):
    print('Event time:', time.time(), name)
event_1_id = scheduler.enter(2, 2, some_deferred_task, ('first',)) # delay(sec), priority, func, args
t = threading.Thread(target=scheduler.run)
t.start()
# scheduler.cancel(event_1_id)
t.join()
#--------------------


#--------------------
# corn-tab from python
# pip install python-crontab

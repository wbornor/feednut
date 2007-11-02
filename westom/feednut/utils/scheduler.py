from westom.feednut.utils import feed_accomplice
import time, threading


class Task(threading.Thread):
    """
    A Scheduler Task
    """
    def __init__(self, action, loopdelay, initdelay):
        self._action = action
        self._loopdelay = loopdelay
        self._initdelay = initdelay
        self._running = 1
        threading.Thread.__init__(self)

    def __repr__(self):
        return '%s %s %s' % (
            self._action, self._loopdelay, self._initdelay)

    def run(self):
        if self._initdelay:
            time.sleep(self._initdelay)
        self._runtime = time.time()
        while self._running:
            start = time.time()
            print 'about to run task'
            self._action()
            self._runtime += self._loopdelay
            time.sleep(self._runtime - start)

    def stop(self):
        self._running = 0
    
class Scheduler:
    """
    A Multi-Purpose Scheduler
    """
    def __init__(self):
        self._tasks = []
        
    def __repr__(self):
        rep = ''
        for task in self._tasks:
            rep += '%s\n' % task
        return rep
        
    def addtask(self, action, loopdelay, initdelay = 0):
        task = Task(action, loopdelay, initdelay)
        self._tasks.append(task)
    
    def startall(self):
        print 'Starting tasks'
        for task in self._tasks:
            task.start()
    
    def stopall(self):
        for task in self._tasks:
            print 'Stopping task', task
            task.stop()
            task.join()
            print 'Stopped'


class FeedUpdateScheduler(Scheduler):
    """ Scheduler for updating the feeds """
    def __init__(self):
        Scheduler.__init__(self)
        #wait 5 minutes between updates
        self.addtask(feed_accomplice.update_feeds, 15, 0)
        print 'HERE!'
    
    def __del__(self):
        self.stopall()

feed_update_scheduler = FeedUpdateScheduler()
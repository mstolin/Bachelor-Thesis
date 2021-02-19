from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler:
    def __init__(self, interval_seconds: int):
        self._interval_seconds = interval_seconds
        self._async_scheduler = AsyncIOScheduler()

    def run(self, main_loop):
        self._async_scheduler.add_job(main_loop.run,
                                      'interval',
                                      seconds=self._interval_seconds,
                                      max_instances=10)
        self._async_scheduler.start()

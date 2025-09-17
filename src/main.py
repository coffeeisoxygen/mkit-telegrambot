# example of scheduler running in async mode

import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main():
    scheduler = AsyncIOScheduler()

    def job_function():
        print("Hello World! The time is: %s" % datetime.now())

    scheduler.add_job(job_function, "interval", seconds=5)
    scheduler.start()

    # Contoh task async lain yang berjalan bersamaan
    while True:
        print("Async task berjalan di waktu: %s" % datetime.now())
        await asyncio.sleep(2)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Scheduler dihentikan.")

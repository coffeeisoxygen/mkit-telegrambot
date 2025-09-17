"""Module Setup The Scheduler.

ThreadPoolExecutor(20): Menjalankan job di thread (dalam satu proses Python). Cocok untuk tugas I/O-bound (misal: akses database, HTTP request). Maksimal 20 job bisa berjalan paralel di thread berbeda.
ThreadPool = lebih efisien untuk I/O, lebih ringan, tapi tetap satu proses.
ProcessPoolExecutor(5): Menjalankan job di proses terpisah. Cocok untuk tugas CPU-bound (misal: komputasi berat, data processing) karena setiap proses punya interpreter Python sendiri, sehingga tidak terpengaruh GIL. Maksimal 5 job bisa berjalan paralel di proses berbeda.
ProcessPool = lebih efisien untuk komputasi berat, bisa memanfaatkan banyak core CPU, tapi lebih berat resource.
"""

from functools import lru_cache

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.settings import get_settings

settings = get_settings().SCHEDULER

jobstores = {"default": SQLAlchemyJobStore(url=settings.sqlite_url)}
executors = {"default": ThreadPoolExecutor(settings.thread_pool_size)}
job_defaults = {"coalesce": settings.coalesce, "max_instances": settings.max_instances}

scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=settings.timezone,
)


@lru_cache
def get_scheduler() -> AsyncIOScheduler:
    """Get the configured scheduler instance."""
    return scheduler

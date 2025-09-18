import asyncio
import logging

from loguru import logger
from src.main import main

logging.basicConfig(
    format="[%(levelname) %(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
logging.getLogger("telethon").setLevel(logging.WARNING)


# intercept logging to loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while (
            frame
            and hasattr(frame, "f_code")
            and frame.f_code.co_filename == logging.__file__
        ):
            frame = frame.f_back if frame and hasattr(frame, "f_back") else None
            depth += 1

        # Pass the log message to Loguru
        args = record.args if record.args else ()
        logger.log(level, record.getMessage(), *args)


# propagate logging to loguru
logging.getLogger().handlers = [InterceptHandler()]  # Hapus propagateHandler

if __name__ == "__main__":
    asyncio.run(main())

#

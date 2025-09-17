import logging

from src.main import run_bot

logging.basicConfig(
    format="[%(levelname) %(asctime)s] %(name)s: %(message)s", level=logging.DEBUG
)


if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nAplikasi dihentikan oleh pengguna (Ctrl+C)")

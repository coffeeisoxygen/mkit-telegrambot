from src.main import run_bot

if __name__ == "__main__":
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nAplikasi dihentikan oleh pengguna (Ctrl+C)")

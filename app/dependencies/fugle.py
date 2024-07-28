import schedule
import time
from threading import Thread
from configparser import ConfigParser
from fugle_trade.sdk import SDK
from app.core.config import settings

class TraderSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TraderSingleton, cls).__new__(cls)
            cls._instance._initialize()
            cls._instance._start_scheduler()
        return cls._instance

    def _initialize(self):
        self.config = ConfigParser()
        self.config.read(settings.config_file)
        self.trader = SDK(self.config)
        self.trader.login()

    def _login(self):
        print("Logging in again...")
        self.trader.login()

    def _start_scheduler(self):
        # Schedule the login to happen every day at midnight
        schedule.every().day.at("00:00").do(self._login)

        # Run the scheduler in a separate thread
        scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()

    def _run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_trader(self):
        return self.trader

# Function to get the trader instance
def get_trader():
    return TraderSingleton().get_trader()

# Example usage
if __name__ == "__main__":
    trader = get_trader()
    # Keep the main thread alive to allow the scheduler to run
    while True:
        time.sleep(10)

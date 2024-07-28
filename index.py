from configparser import ConfigParser
from fugle_trade.sdk import SDK
from dotenv import load_dotenv
import os

load_dotenv()
FUGLE_TRADE_CONFIG = os.getenv('FUGLE_TRADE_CONFIG')
# load config
config = ConfigParser()
config.read(FUGLE_TRADE_CONFIG)
sdk = SDK(config)
# login
sdk.login()

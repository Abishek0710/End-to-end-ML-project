import logging
import os
from datetime import datetime
import sys

from src.exception import CustomException


LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# setting a file format for log

logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
# os.getcwd() → Gets the current working directory (CWD).
# os.path.join() → Joins multiple path components into a valid file path.
# "logs" → Subdirectory inside the current working directory.
# LOG_FILE → The filename (e.g., "app.log").

os.makedirs(logs_path,exist_ok=True)
# Creates directories recursively, avoiding errors if they exist

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)
# logs_path → The directory where logs are stored
# LOG_FILE → The filename



logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
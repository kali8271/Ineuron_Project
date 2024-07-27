import logging
import os
from datetime import datetime

# Determine the date and time when the project is created
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)  # Corrected os.makedirs instead of os.makekdirs
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    filename=LOG_FILEPATH,
                    format="[%(asctime)s]%(lineno)d %(name)s-%(levelname)s-%(message)s")

# Example log message to test the configuration
logging.info("Logger is configured and ready to use.")

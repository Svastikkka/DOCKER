#!/usr/bin/env python
import logging
import logging_loki
import os
from multiprocessing import Queue
import datetime
import time

def cruiser(LOGGER_POD_NAME,LOGGER_CONTAINER_NAME,LOGGER_LOKI_URL,LOGGER_POD_NAMESPACE,LOGGER_SERVICE,LOG_FILE_PATH):
    # Create a Loki handler for logging
    handler = logging_loki.LokiQueueHandler(
        Queue(-1),
        url=LOGGER_LOKI_URL, 
        tags={"application":LOGGER_CONTAINER_NAME, "namespace": LOGGER_POD_NAMESPACE},
        version="1",
    )
    logger = logging.getLogger("loki")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    while True:
        # Check if the log file exists
        if os.path.isfile(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r") as file:
                # Read existing logs
                logs = file.readlines()
                
                # Process existing logs
                for log in logs:
                    log_entry = {
                        "stream": LOG_FILE_PATH,
                        "values": [[int(time.time() * 1000), log.strip()]]
                    }
                    print(log_entry)
                
                # Seek to the last position read
                file.seek(0, 2)

                # # Continuously monitor the log file for new logs
                while True:
                    line = file.readline()
                    if not line:
                        # No new logs, wait before checking again
                        time.sleep(1)
                        continue
                    
                    # Create a log entry with timestamp
                    log_entry = {
                        "stream": LOG_FILE_PATH,
                        "values": [[int(time.time() * 1000), line.strip()]]
                    }
                    
                    print(log_entry)
        else:
            print("Log file not found: " + LOG_FILE_PATH)
        
if __name__ == "__main__":

    # Read logs from a file
    LOG_FILE_PATH = "./waitTimeLogDetails.log"

    LOGGER_POD_NAME=os.getenv("LOGGER_POD_NAME")
    LOGGER_CONTAINER_NAME=os.getenv("LOGGER_CONTAINER_NAME")
    LOGGER_LOKI_URL="http://loki.observability.svc.cluster.local:3100/loki/api/v1/push"
    LOGGER_POD_NAMESPACE=os.getenv("LOGGER_POD_NAMESPACE")
    LOGGER_SERVICE="python-logging-loki 0.3.1"

    cruiser(LOGGER_POD_NAME,LOGGER_CONTAINER_NAME,LOGGER_LOKI_URL,LOGGER_POD_NAMESPACE,LOGGER_SERVICE,LOG_FILE_PATH)

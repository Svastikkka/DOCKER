#!/usr/bin/env python
import logging
import logging_loki
import os
from multiprocessing import Queue
import datetime
import time
import re
import json
def parse_logfmt(log):
    pattern = r"([^-^\s^;=]+)=([^;]+)"
    matches = re.findall(pattern, log)
    return {key: value.strip() for key, value in matches}

def extract_field(log, field):
    log_data = parse_logfmt(log)
    try:
        value = log_data[field]
        return value.strip() if value.strip() != '' else ''
    except KeyError:
        return ""


def cruiser(LOGGER_POD_NAME,LOGGER_CONTAINER_NAME,LOGGER_LOKI_URL,LOGGER_POD_NAMESPACE,LOGGER_SERVICE,LOG_FILE_PATH):
    # Create a Loki handler for logging
    handler = logging_loki.LokiQueueHandler(
        Queue(-1),
        url=LOGGER_LOKI_URL, 
        tags={"application": LOGGER_CONTAINER_NAME, "namespace": LOGGER_POD_NAMESPACE},
        version="1",
    )
    logger = logging.getLogger("loki")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # Create a console handler for logging
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    console_logger = logging.getLogger("console")
    console_logger.addHandler(console_handler)
    console_logger.setLevel(logging.DEBUG)

    #  Infinite loop to check log file exist or not
    while True:
        # Check if the log file exists
        if os.path.isfile(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r") as file:
                # Read existing logs
                logs = file.readlines()
                
                # Process existing logs
                for log in logs:
                    log_entry = json.dumps({
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "stream": LOG_FILE_PATH,
                        "message": {"Module_Name": extract_field(log, 'Module_Name'),
                                    "Element_business_name": extract_field(log, "Element_business_name"),
                                    "Web_page": extract_field(log, 'Web_page'),
                                    "WaitTime": extract_field(log, "WaitTime"),
                                    "Current_URL": extract_field(log, "Current_URL"),
                                    "Locator_strategy": extract_field(log, "Locator_strategy"),
                                    "Element_locator": extract_field(log, "Element_locator")}
                        # "Web_page": extract_field(log, 'Web_page'),
                        # "WaitTime": extract_field(log, "WaitTime"),
                        # "Current_URL": extract_field(log, "Current_URL"),
                        # "Locator_strategy": extract_field(log, "Locator_strategy"),
                        # "Element_locator": extract_field(log, "Element_locator")
                    })
                    try:
                        logger.debug(log_entry)
                    except Exception as e:
                        logger.error("Error occurred while sending logs to Loki: {}".format(str(e)))
                        time.sleep(5)
                    console_logger.debug(log_entry)
                # Seek to the last position read
                file.seek(0, 2)

                # Continuously monitor the log file for new logs
                while True:
                    line = file.readline()
                    if not line:
                        # No new logs, wait before checking again
                        time.sleep(1)
                        continue
                    
                    # Create a log entry with timestamp
                    log_entry = json.dumps({
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "stream": LOG_FILE_PATH,
                        "message": {"Module_Name": extract_field(line, 'Module_Name'),
                                    "Element_business_name": extract_field(line, "Element_business_name"),
                                    "Web_page": extract_field(line, 'Web_page'),
                                    "WaitTime": extract_field(line, "WaitTime"),
                                    "Current_URL": extract_field(line, "Current_URL"),
                                    "Locator_strategy": extract_field(line, "Locator_strategy"),
                                    "Element_locator": extract_field(line, "Element_locator")}
                        # "Web_page": extract_field(line, 'Web_page'),
                        # "WaitTime": extract_field(line, "WaitTime"),
                        # "Current_URL": extract_field(line, "Current_URL"),
                        # "Locator_strategy": extract_field(line, "Locator_strategy"),
                        # "Element_locator": extract_field(line, "Element_locator")
                    })
                    
                    try:
                        logger.debug(log_entry)
                    except Exception as e:
                        logger.error("Error occurred while sending logs to Loki: {}".format(str(e)))
                        time.sleep(5)
                    console_logger.debug(log_entry)
        else:
            console_logger.error("Error occurred while reading the log file: {}".format(LOG_FILE_PATH))
            time.sleep(5)
        
if __name__ == "__main__":

    # Read logs from a file
    LOG_FILE_PATH = "/home/jenkins/agent/workspace/nightly/nimble/nightly-tests/logs/waitTimeLogDetails.log"

    LOGGER_POD_NAME=os.getenv("LOGGER_POD_NAME")
    LOGGER_CONTAINER_NAME=os.getenv("LOGGER_CONTAINER_NAME")
    LOGGER_LOKI_URL="http://loki.observability.svc.cluster.local:3100/loki/api/v1/push"
    LOGGER_POD_NAMESPACE=os.getenv("LOGGER_POD_NAMESPACE")
    LOGGER_SERVICE="python-logging-loki 0.3.1"

    cruiser(LOGGER_POD_NAME,LOGGER_CONTAINER_NAME,LOGGER_LOKI_URL,LOGGER_POD_NAMESPACE,LOGGER_SERVICE,LOG_FILE_PATH)

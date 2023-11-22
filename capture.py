import requests
import sys
import os
import json
import requests
import TermTk as ttk
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import threading

class Requester:
    def __init__(self, url, outputDir, requestMode):
        self.url = url
        self.outputDir = outputDir
        self.requestMode = requestMode # request mode 1,2,3
        curr_dt = datetime.now()
        self.timestamp = str(int(round(curr_dt.timestamp())))
    def writeRequestOutputToFile(self, output, fileName, requestType):
        output_file_name = self.outputDir + "/" + self.timestamp + str(requestType)
        f = open(output_file_name, "w")
        f.write(output)
        f.close()
    def http_request(self):
        http_url = "http://" + self.url
        try:
            r = requests.get(http_url)
            self.writeRequestOutputToFile(r.text, http_url, 1)
        except:
            ttk.TTkLog.error(f"Could not make request with {http_url}")
            return
        return
    def https_request(self):
        https_url = "https://" + self.url
        try:
            #print(f"Attempting to preform request on {https_url}")
            r = requests.get(https_url)
            self.writeRequestOutputToFile(r.text, https_url, 2)
        except:
            ttk.TTkLog.error(f"Could not make request with {https_url}")
            return
        return
    def https_www_request(self):
        https_www_url = "https://www." + self.url
        try:
            #print(f"Attempting to preform request on {https_www_url}")
            r = requests.get(https_www_url)
            self.writeRequestOutputToFile(r.text, https_www_url, 3)
        except:
            return
        return
    def runRequest(self):
        # runs requests based on request mode
        if (self.requestMode[0] == 1):
            self.http_request()
        if (self.requestMode[1] == 1):
            self.https_request()
        if (self.requestMode[2] == 1):
            self.https_www_request()

class Capture:
    def __init__(self, captureFilePath, requestMode, outputDir):
        self.numFilesCaptured = 0
        self.numFilesTotal = 0
        self.numFilesCleaned = 0
        self.captureFilePath = captureFilePath
        self.requestMode = requestMode
        self.outputDir = outputDir
    def display_capture_progress(self):
        print(f"Captured: {self.numFilesCaptured} / {self.numFilesTotal}")
    def display_cleaning_progess(self):
        print(f"Cleaned: {self.numFilesCleaned} / {self.numFilesTotal}")
    def start_capture(self):
        ttk.TTkLog.info(f"Starting capture for {self.captureFilePath}")
        with open(self.captureFilePath, 'r') as file:
            for line in file:
                line = line.strip()
                req = Requester(line, self.outputDir, self.requestMode)
                req.runRequest()

class CaptureDaemon:
    def __init__(self, config_data):
        self.config = config_data
        self.captures = []
    def start_capture_daemon(self):
        ttk.TTkLog.info("Starting Capture Daemon")
        for capture_file in self.config["capture_files"]:
            cap = Capture(capture_file["file_path"], capture_file["request_mode"], capture_file["output_file_path"])
            cap_thread = threading.Thread(target=cap.start_capture)
            self.captures.append(cap_thread)
            cap_thread.start()
        for capture in self.captures:
            capure.join()

def loadJsonFromFile(configFilePath):
    # Opening JSON file
    f = open(configFilePath)
    # returns JSON object as dict
    data = json.load(f)
    f.close()
    return data

# Check if command-line arguments are provided
if len(sys.argv) > 1:
    configFilePath = sys.argv[1]
    ttk.TTkLog.use_default_stdout_logging()

    config_data = loadJsonFromFile(configFilePath)
    capture_daemon = CaptureDaemon(config_data)
    capture_daemon.start_capture_daemon()
else:
    print("No command-line arguments provided.")
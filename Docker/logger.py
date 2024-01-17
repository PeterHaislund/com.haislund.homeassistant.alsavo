import sys
from constants import STATUS_LOG
from datetime import datetime
from config import Config

class logger:
    # latency for truncating log, so we don't do it at every write
    truncate_latency = 10
    log_writes = 0

    def log(self, entry):
        self.log_writes = self.log_writes + 1

        if (self.log_writes % self.truncate_latency) == 0:
            self.truncate_log()

        with open(STATUS_LOG, 'a') as sys.stdout:
            print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " " + entry)
            
    def truncate_log(self):
        config_loader = Config()
        config = config_loader.load_config()
        log_size = config["log_size"]

        with open(STATUS_LOG, 'r+') as log_file:
            # read and store all lines into list
            lines = log_file.readlines()
            # move file pointer to the beginning of a file
            log_file.seek(0)
            # truncate the file
            log_file.truncate()

            # find first line to keep
            first_line = max(0, len(lines) - log_size - 1)

            # start writing lines
            log_file.writelines(lines[first_line:])

      
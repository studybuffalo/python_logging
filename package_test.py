import python_logging
import configparser

config = configparser.ConfigParser()
config.read("E:\My Documents\GitHub\config\logging_config.cfg")

log = python_logging.start(config)

log.info("test")

for i in range(40):
    log.info("i = %d" % i)
import python_logging

log = python_logging.start() 

log.critical("test")

for i in range(40):
    log.info("i = %d" % i)
def start():
    import logging, logging.handlers
    import sys
    from python_logging.handlers import FileHandlerDate, BufferingSMTPHandler
    import configparser

    priCon = configparser.ConfigParser()
    priCon.read("E:\My Documents\GitHub\config\logging_config.cfg")
    
    server = priCon.get("email", "server")
    fromEmail = priCon.get("email", "user")
    password = priCon.get("email", "password")
    toEmail = "torrancj@gmail.com"
    subject = "Test Log Email"

    fh = FileHandlerDate("E:\My Documents\GitHub\python_logging", "a")
    ch = logging.StreamHandler(sys.stdout,)
    eh = BufferingSMTPHandler(server, fromEmail, password, toEmail, subject, 100)

    fh.setLevel(logging.CRITICAL)
    ch.setLevel(logging.DEBUG)
    eh.setLevel(logging.CRITICAL)

    ff = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    cf = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ef = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    fh.setFormatter(ff)
    ch.setFormatter(cf)
    eh.setFormatter(ef)

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log.addHandler(fh)
    log.addHandler(ch)
    log.addHandler(eh)

    return log
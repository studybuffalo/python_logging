def start(config=None):
    """Generates a functioning logging object for log recording

        args:
            config  optional, sets log settings; if absent, uses 
                    package defaults

        returns:
            log     a logging object

        raises:
            none.
    """
    
    import logging, logging.handlers
    import sys
    from python_logging.handlers import FileHandlerDate, BufferingSMTPHandler
    
    def set_level(section):
        """Returns a proper logging log level based on string"""
        # Default Level
        default = logging.WARN

        # Check if option exists before attemping retrieval
        if config.has_option(section, "level"):
            try:
                # Retrieve the level string
                level = config.get(section, "level").upper()

                # Convert string into a logging level
                if level == "DEBUG":
                    return logging.DEBUG
                elif level == "INFO":
                    return logging.INFO
                elif level == "WARN":
                    return logging.WARN
                elif level == "WARNING":
                    return logging.WARNING
                elif level == "ERROR":
                    return logging.ERROR
                elif level == "CRITICAL":
                    return logging.CRITICAL
                elif level == "FATAL":
                    return logging.FATAL
                else:
                    raise ValueError("Incorrect log level provided in config file")
            except Exception as e:
                errmsg.append("unable to set level for console handler: %s" 
                              % e)
                return default
        else:
            errmsg.append("%s - no log level set" % section)

            return default
      
    def set_format(section):
        """Returns a proper logging format based on config file"""
        # Default format
        default = "%(asctime)s - %(levelname)-8s  %(message)s"

        # Check if option exists before attemping retrieval
        if config.has_option(section, "format"):
            return config.get(section, "format", raw=True)
        else:
            errmsg.append("%s - no format set" % section)

            return default
    
    def set_date_format(section):
        """Returns a proper logging date format based on config file"""
        # Default date format
        default = "%Y-%m-%d %H:%M"

        if config.has_option(section, "date_format"):
            return config.get(section, "date_format", raw=True)
        else:
            errmsg.append("%s - no date format set" % section)

            return default

    def add_console_handler():
        """Adds a console handler to log"""
        section = "handler_console"

        # Create the console handler
        ch = logging.StreamHandler(sys.stdout,)

        # Get the log level, set a default if possible
        level = set_level(section)
        
        # Set the log level
        try:
            ch.setLevel(level)
        except Exception as e:
            errmsg.append("%s - unable to set level: %s" % (section, e))

        # Get format (or set default)
        format = set_format(section)
        dateFormat = set_date_format(section)

        # Create and set formatter
        try:
            cf = logging.Formatter(format, dateFormat)
            ch.setFormatter(cf)
        except Exception as e:
            errmsg.append("%s - unable to set format: %s" % (section, e))

        # Add handler to log
        log.addHandler(ch)

        # Confirms handler added
        handlerAdded.append(True)

    def add_file_handler():
        """Add a file handler to log"""

        section = "handler_file"

        # Get the file location and opening details
        if config.has_option(section, "file"):
            location = config.get(section, "file")
        else:
            errmsg.append("%s - no log file set" % section)
            location = ""

        if config.has_option(section, "mode"):
            mode = config.get(section, "mode")
        else:
            errmsg.append("%s - no file mode set" % section)
            mode = "a"

        # Create the handler
        fh = logging.FileHandler(location, mode)

        # Get the log level, set a default if possible
        level = set_level(section)

        # Set the log level
        try:
            fh.setLevel(level)
        except Exception as e:
            errmsg.append("%s - unable to set level: %s" % (section, e))

        # Get format (or set default)
        format = set_format(section)
        dateFormat = set_date_format(section)

        # Create and set formatter
        try:
            ff = logging.Formatter(format, dateFormat)
            fh.setFormatter(ff)
        except Exception as e:
            errmsg.append("%s - unable to set format: %s" % (section, e))

        # Add handler to log
        log.addHandler(fh)

        # Confirms handler added
        handlerAdded.append(True)

    def add_file_date_handler():
        """Add a file handler that generates a log with current date"""

        section = "handler_file_date"

        # Get the file location and opening details
        if config.has_option(section, "location"):
            location = config.get(section, "location")
        else:
            errmsg.append("%s - no log location set" % section)
            location = ""

        if config.has_option(section, "mode"):
            mode = config.get(section, "mode")
        else:
            errmsg.append("%s - no file mode set" % section)
            mode = "a"

        # Create the handler
        fdh = FileHandlerDate(location, mode)

        # Get the log level, set a default if possible
        level = set_level(section)

        # Set the log level
        try:
            fdh.setLevel(level)
        except Exception as e:
            errmsg.append("%s - unable to set level: %s" % (section, e))

        # Get format (or set default)
        format = set_format(section)
        dateFormat = set_date_format(section)

        # Create and set formatter
        try:
            fdf = logging.Formatter(format, dateFormat)
            fdh.setFormatter(fdf)
        except Exception as e:
            errmsg.append("%s - unable to set format: %s" % (section, e))

        # Add handler to log
        log.addHandler(fdh)

        # Confirms handler added
        handlerAdded.append(True)

    def add_email_handler():
        """Add an email handler that emails buffered logs"""

        section = "handler_email"

        # Get the email details
        if config.has_option(section, "server"):
            server = config.get(section, "server")
        else:
            errmsg.append("%s - no email server set" % section)
            server = ""

        if config.has_option(section, "user"):
            fromEmail = config.get(section, "user")
        else:
            errmsg.append("%s - no email user set" % section)
            fromEmail = ""

        if config.has_option(section, "password"):
            password = config.get(section, "password")
        else:
            errmsg.append("%s - no password set" % section)
            password = ""

        if config.has_option(section, "to_email"):
            toEmail = config.get(section, "to_email")
        else:
            errmsg.append("%s - no to email set" % section)
            toEmail = ""

        if config.has_option(section, "subject"):
            subject = config.get(section, "subject")
        else:
            errmsg.append("%s - no subject set" % section)
            subject = "Python Logs"

        if config.has_option(section, "capacity"):
            capacity = config.getint(section, "capacity")
        else:
            errmsg.append("%s - no capacity set" % section)
            capacity = 100

        # Create the handler
        eh = BufferingSMTPHandler(server, fromEmail, password, toEmail, 
                                  subject, capacity)
        

        
        # Get the log level, set a default if possible
        level = set_level(section)

        # Set the log level
        try:
            eh.setLevel(level)
        except Exception as e:
            errmsg.append("%s - unable to set level: %s" % (section, e))

        # Get format (or set default)
        format = set_format(section)
        dateFormat = set_date_format(section)

        # Create and set formatter
        try:
            ef = logging.Formatter(format, dateFormat)
            eh.setFormatter(ef)
        except Exception as e:
            errmsg.append("%s - unable to set format: %s" % (section, e))

        # Add handler to log
        log.addHandler(eh)

        # Confirms handler added
        handlerAdded.append(True)


    # Set up log object
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    
    # Variable to check if any logger was used
    handlerAdded = []

    # Variable to hold any errors to log (once logger setup)
    errmsg = []
   
    # If there is a config file, try to add handlers
    if config:
        import configparser

        # If in config, create the console handler
        if config.has_section("handler_console"):
            add_console_handler()
            
        # If in config, create the file handler
        if config.has_section("handler_file"):
            add_file_handler()

        # If in config, create the file handler (with date)
        if config.has_section("handler_file_date"):
            add_file_date_handler()

        # If in config, create the email handler
        if config.has_section("handler_email"):
            add_email_handler()

    # If no handlers added, add a default console handler
    if len(handlerAdded) == 0:
        # Default is just a console handler
        ch = logging.StreamHandler(sys.stdout,)

        # Set log level
        ch.setLevel(logging.WARNING)

        # Set formatting
        cf = logging.Formatter("%(asctime)s - %(levelname)-8s  %(message)s", 
                               "%H:%M")

        ch.setFormatter(cf)

        # Add handler to log
        log.addHandler(ch)

        log.warn("No handlers were added during setup, using defaults")

    # Display any error message
    if len(errmsg):
        log.warn("\n".join(errmsg))

    return log
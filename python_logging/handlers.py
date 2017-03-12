import logging, logging.handlers

class FileHandlerDate(logging.FileHandler):
    """Update FileHandler to name logs with current date
    
        Args:
            filepath: The path to log to
            mode: the file mode to open the log in
    
        Returns:
            None.
        
        Raises:
            None.
    """
    
    def __init__(self, filepath, mode):
        import datetime
        from unipath import Path

        # Get todays date
        today = datetime.date.today()
        year = today.year
        month = "%02d" % today.month
        day = "%02d" % today.day
        date = "%s-%s-%s" % (year, month, day)

        # Takes the provided path and appends the date as the log name
        filename = Path(filepath, "%s.log" % date).absolute()

        super(FileHandlerDate,self).__init__(filename, mode)

class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, server, fromEmail, password, toEmail, subject, capacity):
        self.server = server
        self.fromEmail = fromEmail
        self.password = password
        self.toEmail = toEmail
        self.subject = subject
        
        super(BufferingSMTPHandler, self).__init__(capacity)

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib

                # Construct email form buffered logs
                msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" 
                       % (self.fromEmail, self.toEmail, self.subject))
                
                for record in self.buffer:
                    s = self.format(record)
                    msg = msg + s + "\r\n"

                # Connect to email server and send messag
                server = smtplib.SMTP(self.server)
                server.ehlo()
                server.starttls()
                server.login(self.fromEmail, self.password)
                server.sendmail(self.fromEmail, self.toEmail, msg)
                server.quit()
            except:
                self.handleError(None)  # no particular record
            
            # Clear buffer of sent messages
            self.buffer = []
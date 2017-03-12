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

        super().__init__(filename, mode)

class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, server, fromEmail, password, toEmail, subject, capacity):
        self.server = server
        self.fromEmail = fromEmail
        self.password = password
        self.toEmail = toEmail
        self.subject = subject
        
        super().__init__(capacity)

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText

                content = MIMEMultipart('alternative')
                content['From'] = self.fromEmail
                content['To'] = self.toEmail
                content['Subject'] = self.subject

                text = []
                html = []

                # Initial HTML Setup
                html.append("<html>")
                html.append("<head></head>")
                html.append("<body>")
                html.append("<pre>")

                # Convert buffer to text and html email contents
                
                for record in self.buffer:
                    line = self.format(record)
                    text.append(line)
                    html.append("%s\n" % line)

                # HTML finishing
                html.append("</pre>")
                html.append("</body>")
                html.append("</html>")

                # Assemble final html and txt email content
                text = "\r\n".join(text)
                html = "".join(html)

                textBody = MIMEText(text, 'plain')
                htmlBody = MIMEText(html, 'html')
                
                content.attach(textBody)
                content.attach(htmlBody)
                
                # Connect to email server and send messag
                server = smtplib.SMTP(self.server)
                server.ehlo()
                server.starttls()
                server.login(self.fromEmail, self.password)
                server.sendmail(self.fromEmail, self.toEmail, content.as_string())
                server.quit()
            except:
                self.handleError(None)  # no particular record
            
            # Clear buffer of sent messages
            self.buffer = []
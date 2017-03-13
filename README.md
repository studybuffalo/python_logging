# python_logging
A python package to streamline logging for current and future Python projects. It is capable of generating up to 4 handlers:
- A console handler
- A file handler
- A modified file handler that names the log the current date
- A modified buffering handler that emails the logs to a specified email
The package is built and tested in Python 3.6.

## Package Dependencies
- logging
- configparser
- smtplib (if using the Email Handler)
- email (if using the Email Handler)
- datetime (if using the File Date Handler)
- unipath (if using the File Date Handler)

## Usage
The python_logging folder contains all the needed files to output a logging object. Simply import the python_logging package and create a logging object and run the start function. A config file can be passed in to specify the loaded handlers. If no config file is passed in, the log will default to a console handler.

```
import python_logging
import configparser

config = configparser.ConfigParser()
config.read("\home\user\my_config_file.cfg")

log = python_logging.start(config)

log.info("This is a test of the log")
> 00:00:00 - INFO      This is a test of the log
```

## Testing
The package_test.py can be used to confirm the module and handlers are working properly. You will need to update the config location to a correct directory to test this part out.

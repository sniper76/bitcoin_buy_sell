import logging

# Configure the logger
logger = logging.getLogger("CustomLogger")
logger.setLevel(logging.DEBUG)  # Set base level to DEBUG to capture all logs

# Create handlers for info and debug logs
info_handler = logging.FileHandler("logs/info.log")
info_handler.setLevel(logging.INFO)  # Logs INFO and above

debug_handler = logging.FileHandler("logs/debug.log")
debug_handler.setLevel(logging.DEBUG)  # Logs DEBUG and above

# Create a formatter
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

# Attach the formatter to the handlers
info_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(debug_handler)

class PrintLogger:
    def __init__(self, name):
        self.name = name
        self.logger = logger

    def debug_method(self, message):
        """
        Logs a debug message along with the class name and a custom message.

        Args:
            message (str): The debug message to log.
        """
        self.logger.debug(f"in {self.name}: {message}")

    def info_method(self, message):
        """
        Logs a info message along with the class name and a custom message.

        Args:
            message (str): The info message to log.
        """
        self.logger.info(f"in {self.name}: {message}")


# Example usage
if __name__ == "__main__":
    obj = PrintLogger("TestObject")
    obj.debug_method("This is a debug message.")
    obj.info_method("This is an info message.")

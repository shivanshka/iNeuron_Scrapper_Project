import logging

class Logger:
    def __init__(self):
        logging.basicConfig(filename="scrapper.log", level=logging.INFO,
                            format="%(asctime)s %(levelname)s \t%(message)s")
    def INFO(self,msg):
        logging.info(msg)

    def WARN(self,msg):
        logging.warning(msg)

    def ERROR(self,msg):
        logging.error(msg)

    def __str__(self):
        print("This is logger module")
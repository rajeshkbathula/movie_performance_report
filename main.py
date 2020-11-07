"""
Python script that reads opensource movies metadata filter
required fileds by mapping it to IMDB wiki file
"""

import logging
import sys
import os
from pythonjsonlogger import jsonlogger

logger_name = os.environ.get('logger_name', 'local')
logger = logging.getLogger(logger_name)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = jsonlogger.JsonFormatter(
    '%(name)s - %(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate=False
logger.setLevel(logging.INFO)


def main() -> bool:
    '''
    This function is the starting point that calls other functions
            that does filter adn do other jobs
        Parameters:
            a (int): A decimal integer

        Returns:
            value (bool): True or False
    '''
    logger.info("main function called!")
    return True



if __name__ == '__main__':
    main()
    
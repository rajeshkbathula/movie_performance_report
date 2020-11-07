import logging,sys,os
from pythonjsonlogger import jsonlogger

logger_name = os.environ.get('logger_name', 'local')
logger = logging.getLogger(logger_name)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = jsonlogger.JsonFormatter(
'%(name)s - %(levelname)s - %(asctime)s - %(filename)s - %(lineno)d - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate=False
logger.setLevel(logging.INFO)


def main():
    logger.info("main function called!")
    return True



if __name__ == '__main__':
    main()
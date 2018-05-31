import logging


def doLog(loggerName, logFile):
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)

    fl = logging.FileHandler(logFile)
    fl.setLevel(logging.DEBUG)

    cl = logging.StreamHandler()
    cl.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fl.setFormatter(formatter)
    cl.setFormatter(formatter)

    logger.addHandler(fl)
    logger.addHandler(cl)

    return logger
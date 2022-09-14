import logging

logger = logging.getLogger(__name__)
stream_hendler = logging.StreamHandler
logger.info('info')
print(logger)

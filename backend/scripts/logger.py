import logging

logger = logging.getLogger("CMDB populator")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

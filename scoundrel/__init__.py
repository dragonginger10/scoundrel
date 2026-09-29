from loguru import logger

logger.remove()

logger.add("scoundrel.log")

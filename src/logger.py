import logging
from environ import LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s, %(levelname)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)

logger = logging.getLogger(__name__)
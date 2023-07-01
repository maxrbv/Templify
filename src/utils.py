from pathlib import Path

import logging
import yaml

logger = logging.getLogger(__name__)


def read_yaml(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as stream:
        try:
            data = yaml.safe_load(stream)
            return data
        except yaml.YAMLError as exc:
            logger.error(exc)

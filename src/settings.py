from pathlib import Path
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

BASE_DIR = Path(__file__).parent.parent.resolve()
ASSETS_DIR = BASE_DIR / 'assets'

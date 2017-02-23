from flask.helpers import get_debug_flag

from buggy.buggy import create_app
from buggy.settings import DevConfig, ProdConfig


CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

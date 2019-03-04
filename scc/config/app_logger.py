import logging
import pathlib
import logging.handlers

# current_path: scc/scc/config
__CURRENT_PATH = str(pathlib.Path(__file__).resolve().parent)  # can also do: os.path.dirname(os.path.abspath(__file__))


# Using personal logger in place of app.logger for the sake of control
class AppLogger:
    # Logging levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    log_path = str(pathlib.Path(__file__).resolve().parents[2]) + '/logs'   # log_path: scc/logs
    log_file = log_path + '/app.log'     # make this concatenation operation more efficient

    def __init__(self, logger_name, logger_level):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.handlers.RotatingFileHandler(AppLogger.log_file, mode='a', maxBytes=100*1024,   # 100KB of 1 log file
                                                         backupCount=2, encoding='utf-8')
        c_handler.setLevel(logger_level)
        f_handler.setLevel(logging.INFO)

        # Create formatters and add to it handlers
        c_format = logging.Formatter('%(levelname)s in %(name)s: %(message)s')
        f_format = logging.Formatter('%(asctime)s | %(levelname)s in %(name)s [%(threadName)s]: %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)

    @staticmethod
    def ensure_log_dir():
        path = pathlib.Path(AppLogger.log_path)
        path.mkdir(parents=True, exist_ok=True)

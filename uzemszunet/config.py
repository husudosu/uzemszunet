import sys
import os
import shutil
import configparser
import logging
from pathlib import Path


def init_logger(logfilename):
    logger = logging.getLogger('uzemszunet')
    formatter = logging.Formatter(
        '[%(asctime)s][%(module)s][%(levelname)s]:%(message)s'
    )

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    fh = logging.FileHandler(logfilename, delay=True)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    return logger


def copy_config(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    package_dir = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(package_dir, 'uzemszunet.cfg'), path)


def get_config_path():
    platform = sys.platform
    if platform == 'win32':
        return os.path.join(
            os.getenv('APPDATA'), 'uzemszunet', 'uzemszunet.cfg'
        )
    else:
        # Unix alapú rendszereken talán ezt meg fogja enni (Linuxon tuti megy)
        # TODO ^ Kivizsgálni
        return os.path.join(
            Path.home(), '.config', 'uzemszunet', 'uzemszunet.cfg'
        )


cfg_path = get_config_path()

if not os.path.isfile(cfg_path):
    copy_config(cfg_path)
    sys.exit(
            'Konfigurációs fájl létrehozva. Állítsd  be az E-mail címed: {0}'.format(
                cfg_path
            )
    )

cfg = configparser.ConfigParser()
cfg.read(cfg_path)

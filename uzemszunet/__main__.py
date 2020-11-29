import os
import sys
import shutil
import argparse
from pprint import pprint
from uzemszunet.utils import get_config_path


def copy_config(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    package_dir = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(package_dir, 'uzemszunet.cfg'), path)


def main():
    cfg_path = get_config_path()
    if not os.path.isfile(cfg_path):
        copy_config(cfg_path)
        sys.exit(
            f'Konfigurációs fájl létrehozva. Állítsd  be az E-mail címed: {cfg_path}'
        )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--email',
        help='E-mail-ben ki lesz küldve az eredmény.',
        action='store_true'
    )
    args = parser.parse_args()

    from uzemszunet.uzemszunet import lekerdez
    res = lekerdez(args.email)

    if not args.email:
        pprint(res)


if __name__ == "__main__":
    main()

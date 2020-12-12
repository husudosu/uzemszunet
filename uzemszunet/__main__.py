import os
import argparse
import logging
import json
from datetime import datetime, date
from pprint import pprint

from uzemszunet.utils import order_list, encode_json
from uzemszunet.sendmail import (
    EmailTipus, handle_email
)
from uzemszunet.config import cfg, init_logger

from uzemszunet.eon import Eon
from uzemszunet.emasz import Emasz

logfile = 'uzemszunet_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'

# Init logger
logger = init_logger(logfile)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--email',
        help='E-mail-ben ki lesz küldve az eredmény.',
        action='store_true'
    )
    parser.add_argument(
        '--egyszeru_lista',
        help="Csak egyszerű zanzásított lista készül.",
        action="store_true"
    )

    args = parser.parse_args()

    res = []

    eon = Eon(
        telepulesek=json.loads(cfg.get('EON', 'telepulesek')),
        notification_days=json.loads(cfg.get('EON', 'notifcation_days'))
    )
    res += eon.run()

    emasz = Emasz(
        telepulesek=json.loads(cfg.get('EMASZ', 'telepulesek')),
        notifcation_days=json.loads(cfg.get('EMASZ', 'notifcation_days'))
    )

    res += emasz.run()

    # Dátum szerint rendezi az összes szolgáltató üzemszüneteit
    res = sorted(res, key=lambda i: i['datum_tol'])

    email_tipus = EmailTipus.EGYSZERU_LISTA

    # Majd ha több szolgáltató lesz, itt lesz ellenőrizve hogy történt e hiba.
    have_error = eon.have_error or emasz.have_error

    # Rendezés dátum & település szerint
    if not args.egyszeru_lista:
        res = order_list(res)
        email_tipus = EmailTipus.RENDEZETT_LISTA

    if args.email:
        handle_email(res, email_tipus, have_error, logfile)
    else:
        res = json.dumps(
            res,
            default=encode_json,
            ensure_ascii=False,
            indent=4,
            sort_keys=True
        ).encode("utf-8")

        pprint(json.loads(res))


if __name__ == "__main__":
    main()

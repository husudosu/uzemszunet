import os
import argparse
import logging
from datetime import datetime
from pprint import pprint

from uzemszunet.utils import order_list
from uzemszunet.sendmail import (
    send_email, EmailTipus, create_email
)
from uzemszunet.config import cfg, init_logger
from uzemszunet.eon import Eon

logfile = 'uzemszunet_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'

# Init logger
logger = init_logger(logfile)


def handle_email(results, email_tipus, have_error):
    to_mail = cfg.get('Email', 'to_mail')
    if len(results) > 0:
        html = create_email(results, email_tipus, have_error)
        if have_error:
            send_email(html, to_mail, 'Üzemszünetek', [logfile])
        else:
            send_email(html, to_mail, 'Üzemszünetek')
    else:
        heartbeat = cfg.getboolean('Email', 'send_heartbeat')
        if heartbeat:
            html = create_email(results, EmailTipus.HEARTBEAT, have_error)
            if have_error:
                send_email(html, to_mail, 'Üzemszünetek', [logfile])
            else:
                send_email(html, to_mail, 'Üzemszünetek')


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

    eon = Eon()
    res = eon.run()

    email_tipus = EmailTipus.EGYSZERU_LISTA

    # Majd ha több szolgáltató lesz, itt lesz ellenőrizve hogy történt e hiba.
    have_error = eon.have_error

    # Rendezés dátum & település szerint
    if not args.egyszeru_lista:
        res = order_list(res)
        email_tipus = EmailTipus.RENDEZETT_LISTA

    if args.email:
        handle_email(res, email_tipus, have_error)
    else:
        pprint(res)


if __name__ == "__main__":
    main()

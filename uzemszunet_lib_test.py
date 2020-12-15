import logging
from datetime import datetime
from pprint import pprint

from uzemszunet.eon import Eon
from uzemszunet.emasz import Emasz
from uzemszunet.utils import order_list
from uzemszunet.sendmail import (EmailTipus, handle_email)


# logájl neve.
LOGFILE = \
    'uzemszunet_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'


def init_logger():
    # Logolást célszerű használni, ha szeretnél értesülni a hibákról!

    logger = logging.getLogger('uzemszunet')
    formatter = logging.Formatter(
        '[%(asctime)s][%(module)s][%(levelname)s]:%(message)s'
    )

    # Konzolban is jelenjenek meg a hibák.
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    # Legyen fájl is, hisz E-mail-ben ezt küldjük el.
    fh = logging.FileHandler(LOGFILE, delay=True)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)

    return logger


def get_sql_data():
    """
    Ide elkészítheted a saját adatforrásod.
    Tömbnek kell visszatérnie.
    """
    return ["Debrecen", "Balkány"]


logger = init_logger()


# Városok lekérdezése dinamikusan, ha változó adatforással dolgozol.
logger.info("Települések lekérdezése 'SQL-ből'.")
telepulesek = get_sql_data()

# Értesítési napok
notification_days = [0, 1, 3, 7]

# Eon konfiguráció
eon = Eon(
    telepulesek=telepulesek,
    notification_days=notification_days,
    forras_mentese=False,
    helyi_forras=False
)

# Émász konfiguráció
emasz = Emasz(
    telepulesek=telepulesek,
    notification_days=notification_days,
    forras_mentese=False,
    helyi_forras=False
)

# Üzemszünetek eltárolása tömbben
logger.info("Üzemszünetek lekérdezése")
res = []
res += eon.run()
res += emasz.run()

# Megnézi hogy van e hiba, hogy küldjünk e E-mailt róla
have_error = eon.have_error or emasz.have_error

# Célszerű rendezni dátum szerint az eredményeket.
res = sorted(res, key=lambda i: i['datum_tol'])

# Ezután lehet {"Dátum": ["Város": "Üzemszünetek"]} formába rendezni
res = order_list(res)  # Ha az egyszerű listát akarod kommenteld ki ezt a sort.

# Email beállítások:
email_config = {
    'to_mail': 'ide_megy_az_email@gmail.com',
    'smtp_host': 'smtp.gmail.com',
    'smtp_port': 465,
    'user': 'felhasznalo@gmail.com',
    'password': 'jelszo'
}
pprint(res)
# EmailTipus.RENDEZETT_LISTA: Rendezett lista
# EmailTipus.EGYSZERU_LISTA: Egyszerű lista

# Ha a belső sablonrendszert akarod használni itt a lehetőség
if len(res) > 0:
    handle_email(
        results=res,
        email_tipus=EmailTipus.RENDEZETT_LISTA,
        have_error=have_error,
        email_config=email_config,
        logfile=LOGFILE
    )
else:
    # Ilyenkor csak heartbeat fog menni
    handle_email(
        results=res,
        email_tipus=EmailTipus.HEARTBEAT,
        have_error=have_error,
        email_config=email_config,
        logfile=LOGFILE
    )

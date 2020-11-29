import sys
import traceback
import configparser
import json
from tempfile import NamedTemporaryFile
from datetime import datetime

from uzemszunet.utils import send_email, format_email, get_config_path

import requests
import pandas


cfg = configparser.ConfigParser()
cfg.read(get_config_path())


TELEPULESEK = json.loads(cfg.get('Uzemszunet', 'telepulesek'))
NOTIFICATION_DAYS = json.loads(cfg.get('Uzemszunet', 'notifcation_days'))


def dl_eon_file():
    """
    Letölti az EON üzemszünet fájlt.
    """
    dl_url = cfg.get('EON', 'xls_url')
    r = requests.get(dl_url, stream=True)
    r.raise_for_status()

    f = NamedTemporaryFile(mode="wb+")
    f.write(r.content)
    return f


def parse_eon_file(f, aramszunetek):
    """
    Analizálja a fájlt és az összes konfigurációban megadott
    településre lekérdezi az tervezett üzemszüneteket!
    """
    xls = pandas.read_excel(f, sheet_name="Áram", header=1)
    xls_dict = xls.to_dict()

    telepulesek = xls_dict["Település"]
    now = datetime.now().date()

    for index, telepules in enumerate(telepulesek.items()):
        if telepules[1] in TELEPULESEK:
            datum = xls_dict["Dátum"][index]
            dt = datetime.strptime(datum[0:10], "%Y-%m-%d").date()
            diff = (dt - now).days

            if diff not in NOTIFICATION_DAYS:
                continue

            if aramszunetek.get(datum) is None:
                aramszunetek[datum] = {}
            if aramszunetek.get(datum).get(telepules[1]) is None:
                aramszunetek[datum][telepules[1]] = []

            aramszunetek[datum][telepules[1]].append(
                {
                    "utca": xls_dict["Utca"][index],
                    "terulet": xls_dict["Terület"][index],
                    "hazszam_tol": xls_dict["Házszám(tól)"][index],
                    "hazszam_ig": xls_dict["Házszám(ig)"][index],
                    "idopont_tol": xls_dict["Időpont(tól)"][index],
                    "idopont_ig": xls_dict["Időpont(ig)"][index],
                    "megjegyzes": xls_dict["Megjegyzés"][index],
                    "szolgaltato": "EON"
                }
            )
    return aramszunetek


def lekerdez(email=False):
    try:
        eon_file = dl_eon_file()
        uzemszunetek = {}

        parse_eon_file(eon_file, uzemszunetek)

        if len(uzemszunetek) > 0 and email:
            html = format_email(uzemszunetek)
            send_email(
                html,
                cfg.get('Email', 'smtp_host'),
                cfg.get('Email', 'user'),
                cfg.get('Email', 'password'),
                cfg.get('Email', 'to_mail'),
                'Tervezett üzemszünetek'
            )
        return uzemszunetek
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        exc_text = traceback.format_exception(exc_type, exc_value, exc_tb)

        if email:
            send_email(
                'Hiba történt:' + str(exc_text),
                cfg.get('Email', 'smtp_host'),
                cfg.get('Email', 'user'),
                cfg.get('Email', 'password'),
                cfg.get('Email', 'to_mail'),
                'Tervezett üzemszünetek HIBA'
            )
        print(exc_text)

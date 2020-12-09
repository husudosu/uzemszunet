import json
import logging
import numpy

from tempfile import NamedTemporaryFile
from datetime import datetime

import requests

import pandas

from uzemszunet.config import cfg

URL = 'https://fbapps.cloudwave.hu/eon/eonuzemzavar/page/xls'

logger = logging.getLogger('uzemszunet')


class Eon:

    def __init__(self, url=URL):
        self.url = url
        self.have_error = False
        self.file = None

        self.ses = requests.session()
        self.ses.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            }
        )

        # Konfiguráció betöltése
        self.telepulesek = json.loads(cfg.get('EON', 'telepulesek'))
        self.notification_days = json.loads(cfg.get('EON', 'notifcation_days'))

    def dl_eon_file(self):
        """
        Letölti az EON weboldaláról az üzemszünetek listáját.
        """
        try:
            r = self.ses.get(URL, stream=True)
            r.raise_for_status()

            self.file = NamedTemporaryFile(mode="wb+")
            self.file.write(r.content)
        except requests.exceptions.RequestException as re:
            logger.error(
                "Probléma az EON fájl letöltésével:" + str(
                    re.response.status_code)
            )
            self.have_error = True

    def parse_eon_file(self):
        """
        Analizálja a fájlt és az összes konfigurációban megadott
        településre lekérdezi az tervezett üzemszüneteket!
        """

        # Ha hiba történt a letöltéskor
        if not self.file and self.have_error:
            logger.error(
                'Nem sikerült az üzemszüneteket letölteni, nincs mit értelmezni.'
            )
            return []

        uzemszunetek = []

        xls = pandas.read_excel(self.file, sheet_name="Áram", header=1)
        xls_dict = xls.to_dict()

        telepulesek = xls_dict["Település"]
        now = datetime.now().date()

        for index, telepules in enumerate(telepulesek.items()):
            try:
                if telepules[1] in self.telepulesek:
                    datum = xls_dict["Dátum"][index]
                    dt = datetime.strptime(datum[0:10], "%Y-%m-%d")
                    diff = (dt.date() - now).days

                    # Ellenőrzi, hohgy kell e a felhasználónak az adat.
                    if diff not in self.notification_days:
                        continue

                    # Tól-ig dátumok létrehozása
                    datum_tol = datum + xls_dict["Időpont(tól)"][index]
                    datum_ig = datum + xls_dict["Időpont(ig)"][index]
                    datum_tol = datetime.strptime(datum_tol, '%Y-%m-%d%H:%M:%S')
                    datum_ig = datetime.strptime(datum_ig, '%Y-%m-%d%H:%M:%S')

                    # Cím lekezelése
                    hazszam_tol = xls_dict["Házszám(tól)"][index]
                    hazszam_ig = xls_dict["Házszám(ig)"][index]
                    cim = xls_dict["Utca"][index]

                    if hazszam_ig is not numpy.nan:
                        cim = "{0} {1}-{2}".format(
                            xls_dict["Utca"][index],
                            hazszam_tol,
                            hazszam_ig
                        )
                    elif hazszam_tol is not numpy.nan:
                        cim = "{0} {1}".format(cim, hazszam_tol)

                    uzemszunetek.append(
                        {
                            "telepules": telepules[1],
                            "datum_tol": datum_tol,
                            "datum_ig": datum_ig,
                            "utca": cim,
                            "terulet": xls_dict["Terület"][index],
                            "megjegyzes": xls_dict["Megjegyzés"][index],
                            "szolgaltato": "EON"
                        }
                    )
            except Exception as e:
                logger.error(str(e))
                self.have_error = True
        return uzemszunetek

    def run(self):
        """
        Az egész procedúrát elvégzi és visszadja az üzemszünet listát.
        """
        self.have_error = False
        self.dl_eon_file()
        if self.have_error:
            return []
        return self.parse_eon_file()

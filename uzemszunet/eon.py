import json
import logging
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

        # Konfiguráció betöltése
        self.telepulesek = json.loads(cfg.get('EON', 'telepulesek'))
        self.notification_days = json.loads(cfg.get('EON', 'notifcation_days'))

    def dl_eon_file(self):
        """
        Letölti az EON weboldaláról az üzemszünetek listáját.
        """
        try:
            r = requests.get(URL, stream=True)
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
                    dt = datetime.strptime(datum[0:10], "%Y-%m-%d").date()
                    diff = (dt - now).days

                    # Ellenőrzi, hohgy kell e a felhasználónak az adat.
                    if diff not in self.notification_days:
                        continue

                    uzemszunetek.append(
                        {
                            "telepules": telepules[1],
                            "datum": datum,
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

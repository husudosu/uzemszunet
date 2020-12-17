import json
import logging
from datetime import datetime

import requests

from uzemszunet.utils import convert_dotnet_date
from uzemszunet.exceptions import DownloadError

URL = 'https://elmuemasz.hu/elmu/ZavartatasTerkep/GetZavartatasok?vallalat=ELMUEMASZ'

logger = logging.getLogger('uzemszunet')


class Emasz:

    def __init__(
        self,
        telepulesek,
        notification_days,
        url=URL,
        forras_mentese=False,
        helyi_forras=False
    ):
        self.url = url

        self.have_error = False

        self.ses = requests.session()
        self.ses.headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            }
        )

        self.telepulesek = telepulesek
        self.notification_days = notification_days
        self.forras_mentese = forras_mentese
        self.helyi_forras = helyi_forras

        # Session által letöltött JSON.
        self.json = []

    def process_cim(self, cim):
        """
        Feldolgozza az adott cím dict-jét
        :param cim: Émász JSON-ból jövő Cim.
        """

        if cim["Telepules"] not in self.telepulesek:
            return []
        uzemszunetek = []
        now = datetime.now().date()

        for datum in cim["Datumok"]:
            # ! Datetime object jön vissza!
            datum['From'] = convert_dotnet_date(datum['From'])
            datum['To'] = convert_dotnet_date(datum['To'])

            diff = (datum['From'].date() - now).days

            # Hozzáadás az eredményekhez
            if diff in self.notification_days:
                uzemszunetek.append(
                    {
                        "telepules": cim["Telepules"],
                        "datum_tol": datum['From'],
                        "datum_ig": datum['To'],
                        "utca": cim["Cim"],
                        "szolgaltato": "Émász",
                        "terulet": "",
                        "megjegyzes": "",
                    }
                )
        return uzemszunetek

    def parse_json(self):
        uzemszunetek = []
        if self.have_error and self.json is None or len(self.json) == 0:
            logger.error(
                'Nem sikerült az üzemszüneteket letölteni, nincs mit értelmezni.'
            )
            return []

        for uzemszunet in self.json['zavartatasok']:
            try:
                # Csak tervezett üzemszüneteket vegye figyelembe
                if uzemszunet['Tervezett'] is False:
                    continue

                # Címek lekezelése
                for cim in uzemszunet['Cimek']:
                    uzemszunetek += self.process_cim(cim)
            except Exception as e:
                logger.exception('Hiba történt:')
                self.have_error = True

        return uzemszunetek

    def get_uzemszunetek(self):
        try:
            r = self.ses.get(self.url)
            r.raise_for_status()

            if self.forras_mentese:
                with open('emasz.json', 'w') as f:
                    json.dump(r.json(), f, indent=4)

            return r.json()
        except requests.exceptions.RequestException as re:
            logger.error(
                "Probléma az Émász forrás letöltésével:" + str(
                    re.response.status_code)
            )
            self.have_error = True
            raise DownloadError(
                "Probléma az ÉMÁSZ fájl letöltése közben",
                re.response.status_code,
                re.response.status_text
            )

    def run(self):
        self.have_error = False
        if self.helyi_forras:
            with open('emasz.json', 'r') as f:
                self.json = json.load(f)
        else:
            self.json = self.get_uzemszunetek()

        return self.parse_json()

        self.have_error = True
        logger.exception('Hiba történt:')
        return []

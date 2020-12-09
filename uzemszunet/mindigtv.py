from datetime import datetime
import locale
# import lxml

# from uzemszunet.utils import get_month


URL = 'https://mindigtv.hu/aktualitasok/'

# Vannak országos üzemszünetek is, erre ügyelni kell!


class MindigTV:

    def __init__(self, url=URL):
        self.url = url

    def create_url(self, month):
        """
        Létrehozza a megfelelő URL-t.
        :param month: Hónap száma
        """
        monthname = get_month(month)
        year = datetime.now().year()
        return '{0}{1}-{2}-{3}'.format(
            self.url, 'karbantartas', year, monthname
        )

    def run(self):
        pass

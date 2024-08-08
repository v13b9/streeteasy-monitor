import requests

from src.streeteasymonitor.search import Search
from src.streeteasymonitor.database import Database
from src.streeteasymonitor.messager import Messager
from src.streeteasymonitor.config import Config


class Monitor:
    def __init__(self, **kwargs):
        self.config = Config()
        self.db = Database()

        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())

        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.session.close()

    def run(self):
        self.search = Search(self)
        self.listings = self.search.fetch()
        self.messager = Messager(self, self.listings)
        self.messager.send_messages()

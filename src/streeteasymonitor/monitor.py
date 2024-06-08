import requests

from src.streeteasymonitor.search import Search
from src.streeteasymonitor.database import Database
from src.streeteasymonitor.messager import Messager
from src.streeteasymonitor.config import Config


class Monitor:
    def __init__(self):
        self.config = Config()
        self.db = Database(self.config)

        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())

        self.search = Search(self)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.session.close()

    def __repr__(self):
        return f'< {self.session.headers} >'

    def fetch(self):
        return self.search.fetch()

    def run(self):
        listings = self.search.fetch()
        messager = Messager(self, listings)
        messager.send_messages()

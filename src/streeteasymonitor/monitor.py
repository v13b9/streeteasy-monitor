import requests

from src.streeteasymonitor.search import Search
from src.streeteasymonitor.database import Database
from src.streeteasymonitor.messager import Messager
from src.streeteasymonitor.config import Config

class Monitor:
    def __init__(self, **kwargs):
        self.config = Config()
        self.db = Database(self.config)

        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())

        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.session.close()

    def run(self):
        search = Search(self)
        listings = search.fetch()
        messager = Messager(self, listings)
        messager.send_messages()


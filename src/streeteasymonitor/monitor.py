import requests
import time

from src.streeteasymonitor import Search, Database, Messager, Config

class Monitor:
    def __init__(self):
        self.config = Config()
        self.db = Database(self.config)

        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())

        # self.search = Search(self)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.session.close()

    def run(self):
        start_time = time.perf_counter()
        
        search_start_time = time.perf_counter()
        search = Search(self)
        listings = search.fetch()
        search_end_time = time.perf_counter()

        messager_start_time = time.perf_counter()
        messager = Messager(self, listings)
        messager.send_messages()
        messager_end_time = time.perf_counter()

        end_time = time.perf_counter()

        print(f"Total execution time: {end_time - start_time:.2f} seconds")
        print(f"Search time: {search_end_time - search_start_time:.2f} seconds")
        print(f"Messager time: {messager_end_time - messager_start_time:.2f} seconds")

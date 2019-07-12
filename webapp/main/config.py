import json
from pymongo import MongoClient


class Config(object):

    def __init__(self, config_json):
        config = config_json
        with open(config_json, 'r') as file_:
            file_config = json.load(file_)
            uri_local = 'mongodb://localhost'
            uri_remote = (config['compose-for-mongodb'][0]['credentials']['uri'] +
                          '&ssl_cert_reqs=CERT_NONE')
            cli = MongoClient(uri_remote)
            mockdb = config["domain-db"]["db-name"]
            COLL_NAME = config["domain-db"]["coll_domain_data"]
            coll_data = cli[mockdb][COLL_NAME]
            coll_chat = cli[mockdb][config["domain-db"]["coll_chat_data"]]
            coll_chat_test = cli[mockdb][config["domain-db"]["coll_chat_data_test"]]
            coll_crowd = cli[mockdb][config["domain-db"]["coll_cf_data"]]
            coll_crowd_test = cli[mockdb][config["domain-db"]["coll_cf_data_test"]]

            MTS_API_URL = config["mts-api"]["mts-endpoint"]
            MTS_API_CID = config["mts-api"]["mts-api-cid"]
            MTS_API_CONTEXT = config["mts-api"]["mts-api-context"]
            MTS_API_MESSAGE = config["mts-api"]["mts-api-message"]
            MTS_API_KB = config["mts-api"]["mts-api-kb"]

            APP_URL = config["app-url"]
            DOMAIN = config["domain-name"]
            LST_META = config["metadata"]["LST_META"]
            SORTING_KEY = config["metadata"]["SORTING_KEY"]
            SORTING_ORDER = config["metadata"]["SORTING_ORDER"]
            TEXT4DEBUG = config["metadata"]["TEXT4DEBUG"]

            CHAT_HTML = DOMAIN + '.chat.html'
            # self.override(file_config)
            # for key, value in file_config.items():
            #     setattr(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __getstate__(self):
        return self.as_dict()

    def __setstate__(self, state):
        self.override(state)

    def items(self):
        return list(self.__dict__.items())

    def as_dict(self):
        return dict(list(self.items()))

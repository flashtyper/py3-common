import requests
import logging
import urllib

def format_json_for_import(metric_name: str, values: list, timestamps: list, labels: dict = None) -> dict:
    # Assembels a new dictionary accordingly the json line protocol of victoriametrics and returns it
    js = {}
    if len(values) != len(timestamps):
        return js
    js['metric'] = {
        '__name__': metric_name
    }
    js['values'] = values
    js['timestamps'] = timestamps
    if labels:
        js['metric'] |= labels
    return js


def quote(s: str) -> str:
    # Quotes a query string for VictoriaMetrics
    s1 = urllib.parse.quote(s, safe='')
    return s1.replace('-', '%5C-')


class VictoriaMetrics:
    def __init__(self, host):
        self.session = requests.Session()
        self.host = host
        self.logger = logging.getLogger('VictoriaMetrics')

    def __post_data(self, url, data):
        self.logger.debug('Posting data: {}'.format(url))
        response = self.session.post(url, headers={'Content-Type': 'application/json'}, json=data)
        return response.status_code, response

    def __get_data(self, endpoint: str, selector: str):
        base_q = f'http://{self.host}/api/v1/{endpoint}?{selector}'
        response = self.session.get(base_q, headers={'Accept': 'application/json'})
        try:
            js = response.json()
        except Exception as e:
            js = {}
        return response.status_code, js

    def import_series(self, data: Union[dict, list[dict]]):
        # Sends metrics in json line protocol to victoriametrics host. 
        base_q = f'http://{self.host}/api/v1/import'
        if isinstance(data, list):
            results = []
            for line in data:
                results.append(self.__post_data(base_q, line))
            return results
        return self.__post_data(base_q, data)

    def query_last_point(self, selector: str):
        resp, js = self.__get_data('query', selector)
        return js

    def query_range(self, selector: str, from_ts: str, to_ts: str, step: str = '5m'):
        sel = 'query=' + quote(selector) + f'&start={from_ts}&end={to_ts}&step={step}'
        print(sel)
        resp, js = self.__get_data('query_range', sel)
        return js



import requests
import logging


def format_json_for_import(metric_name: str, values: list, timestamps: list, labels: dict = None) -> dict:
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


class VictoriaMetrics:
    def __init__(self, host):
        self.session = requests.Session()
        self.host = host
        self.logger = logging.getLogger('VictoriaMetrics')

    def __post_data(self, url, data):
        self.logger.debug('Posting data: {}'.format(url))
        response = self.session.post(url, headers={'Content-Type': 'application/json'}, json=data)
        return response.status_code, response

    def import_series(self, data):
        base_q = f'http://{self.host}/api/v1/import'
        if isinstance(data, list):
            results = []
            for line in data:
                results.append(self.__post_data(base_q, line))
            return results
        return self.__post_data(base_q, data)



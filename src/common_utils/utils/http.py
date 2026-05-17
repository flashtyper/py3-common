import requests as rq


class HTTP:
    def __init__(self):
        self.session = rq.Session()

    def make_request(self, url: str, method: str = 'GET', cookies=None, headers=None, body=None, params=None) -> dict:
        response = None
        if method == 'GET':
            response = self.session.get(url, headers=headers, cookies=cookies, data=body, params=params)
        elif method == 'POST':
            response = self.session.post(url, headers=headers, cookies=cookies, data=body, params=params)

        if response.status_code != 200:
            return {'ok': response.ok, 'status_code': response.status_code, 'reason': response.reason, 'response_header': response.headers, 'response_cookies': response.cookies}
        try:
            js = response.json()
        except Exception as e:
            js = {}
        return {'ok': response.ok, 'status_code': response.status_code, 'reason': '', 'json': js, 'response_header': response.headers, 'response_cookies': response.cookies, 'content': response.text}


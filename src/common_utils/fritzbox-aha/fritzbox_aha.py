import requests
import re
import hashlib
import xml.etree.ElementTree as ET
from fritzbox_aha_interface.models.devices import EnergyMeter


class FritzBoxAHA:
    def __init__(self, ip: str, username: str, password: str, path_to_ca_file: str, verify_ca=True):
        self.ip = ip
        self.username = username
        self.password = password
        self.path_to_ca_file = path_to_ca_file
        self.session = requests.Session()
        self.verify_ca = verify_ca
        self.sid = ''
        if not self.login():
            raise ValueError('Failed to login to FritzBox!')

    def __http_get(self, url: str, params=None) -> str:
        """
        Sends an HTTP GET request to the specified API endpoint.

        The request is executed using the current session object and automatically
        prepends the configured base IP address. SSL certificate verification is
        controlled by the instance's ``verify_ca`` setting.

        Args:
            url (str):
                Relative API endpoint URL.
            params (dict | None, optional):
                Query parameters to include in the request.

        Returns:
            str:
                The response body as a string if the request succeeds and contains
                content. Returns an empty string if the request fails, the response
                status is not successful, or no content is returned.

        Raises:
            No exceptions are raised directly. All exceptions are caught internally
            and logged to stdout.
        """
        response = None
        try:
            response = self.session.get(self.ip + url, params=params, verify=self.verify_ca)
        except Exception as e:
            print(f'{e.__class__.__name__}: {str(e)}')
            return ''

        if not response.ok:
            print('API Call was not successful!')
            print(f'[{response.status_code} {response.reason}] {response.text}')
            return ''

        if not response.text:
            print('API Call returned no content!')
            return ''

        return response.text



    def login(self) -> bool:
        """
        Authenticates against the remote API and retrieves a session ID (SID).

        The method first requests an authentication challenge from the API and
        supports both modern PBKDF2-based challenge-response authentication and
        legacy MD5-based authentication schemes. After generating the appropriate
        response hash, it submits the login request and stores the returned session
        ID in ``self.sid``.

        Returns:
            bool:
                ``True`` if authentication succeeds and a valid SID is received,
                otherwise ``False``.

        Side Effects:
            - Updates ``self.sid`` with the authenticated session ID.
            - Prints error messages to stdout if authentication fails or expected
              XML fields cannot be found.

        Notes:
            - PBKDF2 authentication is used when the challenge starts with ``"2$"``.
            - Legacy authentication falls back to an MD5 hash encoded as UTF-16LE.
            - Relies on ``__http_get()`` for API communication.
        """
        xml = self.__http_get("/login_sid.lua?version=2")
        if (m := re.search(r"<Challenge>(.*?)</Challenge>", xml)) is None:
            print('Could not find regex "<Challenge>(.*?)</Challenge>" in response content!')
            return False

        challenge = m.group(1)
        if challenge.startswith("2$"):
            _, iter1, salt1, iter2, salt2 = challenge.split("$")
            hash1 = hashlib.pbkdf2_hmac("sha256", self.password.encode("utf-8"), bytes.fromhex(salt1), int(iter1))
            hash2 = hashlib.pbkdf2_hmac("sha256", hash1, bytes.fromhex(salt2), int(iter2))
            final_salt = salt2 + "$" + hash2.hex()
        else:
            text = challenge + "-" + self.password
            md5 = hashlib.md5(text.encode("utf-16le")).hexdigest()
            final_salt = challenge + "-" + md5

        xml2 = self.__http_get('/login_sid.lua?version=2', params={'username': self.username, 'response': final_salt})
        if (m := re.search(r"<SID>(.*?)</SID>", xml2)) is None:
            print('Could not find regex "<SID>(.*?)</SID>" in response content!')
            return False

        self.sid = m.group(1)
        return True


    def get_powermeter(self) -> list:
        """
        Retrieves information about all available home automation devices.

        The method requires an active session ID and requests the device list from
        the home automation web service. Each returned device is converted into a
        dictionary containing basic metadata, and optional battery or power meter
        values are added when available.

        Returns:
            list[dict]:
                A list of device dictionaries. Each dictionary may contain:

                - ``identifier``: Unique device identifier.
                - ``fwversion``: Firmware version of the device.
                - ``productname``: Product name of the device.
                - ``battery``: Battery level, if reported by the device.
                - ``kWh``: Energy consumption in kilowatt-hours, if a power meter
                  is available.

                Returns an empty list if no session ID is available.

        Side Effects:
            Prints an error message to stdout if the method is called before login.
        """
        if not self.sid:
            print('No cid. Please login first!')
            return []
        url = '/webservices/homeautoswitch.lua'
        xml = self.__http_get(url, params={"switchcmd": "getdevicelistinfos", "sid": self.sid})
        print(xml)
        tree = ET.ElementTree(ET.fromstring(xml))
        root = tree.getroot()

        devices = []
        for device in root.findall('.//device'):
            identifier = device.get('identifier', '')
            device_id = device.get('id', 0)
            fwversion = device.get('fwversion', '')
            productname = device.get('productname', '')
            manufacturer = device.get('manufacturer', 'AVM')
            bitmask = int(device.get('functionbitmask'))
            fb_device = None
            if bitmask & (1 << 7):
                # Bit 7 is set -> EnergyMeter
                fb_device = EnergyMeter(identifier=identifier, fwversion=fwversion, productname=productname, manufacturer=manufacturer, id=device_id, functionbitmask=bitmask)
                fb_device.parse(device)
            else:
                print(f'Unknown device: Bitmask "{bin(bitmask)}" not known. Please extend the parser.')
                continue

            devices.append(fb_device)

        return devices


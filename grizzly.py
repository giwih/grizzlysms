import requests

from exceptions import NoIdActivationError, BadActionError, SqlError, BadServiceError, BadStatusError, InvalidServiceCodeError, InvalidCountryCodeError

# нужно посмотреть другие raise, убрать acces_number, добавить обработку ошибок get
ALL_SERVICE_CODES = {
    'hn', 'wj', 'qi', 'hk', 'an', 'uk', 'zl', 'bt', 'ab', 'hx', 'hw', 'yo', 'am', 'pm', 'wx',
    'av', 'ff', 'gr_bf', 'ie', 'vd', 'zu', 'bl', 'zs', 'lt', 'ua', 'bz', 'tx', 'mo', 'ip', 'ls',
    'gr_rd', 'dd', 're', 'wc', 'ox', 'fr', 'zk', 'zz', 'os', 'xk', 'ds', 'sd', 'ak', 've', 'hz',
    'fi', 'rz', 'dh', 'gr_dh', 'fb', 'se', 'cn', 'gr_fw', 'nz', 'mv', 'gr_fx', 'cg', 'gr_gc',
    'ul', 'gt', 'jd', 'bp', 'ni', 'go', 'gf', 'gr_gs', 'gr_ed', 'yw', 'xs', 'gx', 'en', 'ss',
    'vz', 'ks', 'jl', 'gr_hb', 'pd', 'im', 'gr_im', 'ju', 'ig', 'zo', 'kt', 'ol', 'bf', 'fz',
    'sq', 'vp', 'sb', 'dl', 'do', 'xf', 'gr_lc', 'me', 'tn', 'tu', 'ma', 'lb', 'fd', 'ry', 'lv',
    'dg', 'bv', 'mc', 'mm', 'bg', 'gy', 'py', 'bu', 'da', 'ae', 'nv', 'nf', 'ew', 'vm', 'ly',
    'sn', 'dr', 'xh', 'sg', 'gg', 'zr', 'wo', 'gr_pp', 'ts', 'jq', 'at', 'fx', 'ev', 'ro', 'pf',
    'oz', 'po', 'cm', 'dp', 'vf', 'cc', 'co', 'gr_re', 'ij', 'mn', 'fl', 'gs', 'vv', 'ka', 'gr_sg',
    'wg', 'sf', 'mt', 'vj', 'lc', 'wh', 'qd', 'ih', 'tg', 'qq', 'lf', 'gr_tl', 'oi', 'xd', 'bs',
    'gc', 'pr', 'tl', 'jt', 'hb', 'tw', 'ub', 'cp', 'hh', 'of', 'yy', 'vi', 'kc', 'sc', 'wb', 'kf',
    'wa', 'qj', 'uu', 'mp', 'rr', 'bd', 'mb', 'yl', 'yi', 'mj', 'mz', 'dy', 'mi', 'yd', 'st', 'nb',
    'vk', 'sh', 'we', 'ot', 'gr_lt', 'mg', 'ok', 'jr', 'xj', 'be', 'gr_sber', 'yk', 'ym', 'ya'
}

ALL_COUNTRY_CODES = {
    '175', '50', '35', '155', '58', '181', '16', '76', '169', '39', '148', '179', '74', '122', '60', '118', '145', '51',
    '124', '82', '120', '83', '92', '108', '123', '73', '121', '152', '119', '158', '84', '70', '91', '10', '154', '26',
    '131', '28', '38', '160', '94', '68', '130', '43', '88', '14', '127', '129', '128', '172', '168', '126', '109', '21',
    '147', '96', '13', '22', '6', '116', '47', '10016', '23', '132', '56', '86', '30', '186', '2', '170', '24', '41', '36',
    '111', '8', '77', '11', '3', '33', '133', '150', '18', '93', '27', '100', '25', '49', '136', '135', '153', '102', '44',
    '10348', '165', '157', '114', '17', '20', '137', '7', '69', '159', '37', '54', '80', '85', '144', '72', '180', '5',
    '138', '81', '139', '19', '48', '90', '67', '185', '174', '95', '107', '66', '112', '79', '87', '65', '15', '117',
    '97', '146', '0', '140', '32', '101', '10231', '178', '53', '106', '183', '184', '61', '166', '134', '164', '29',
    '10351', '10349', '141', '59', '149', '142', '12', '187', '115', '143', '52', '55', '9', '99', '10227', '104', '89',
    '161', '62', '75', '40', '1', '156', '4', '163', '78', '162', '45', '125', '42', '171', '63', '151', '173', '46', '64',
    '105', '167', '176', '34', '71', '31', '10350', '177', '103', '182'
}

ALL_STATUSES = {'-1', '1', '3', '6', '8'}

class Grizzly:
    """"
    The main class of the grizzlysms library

    :param api_key: the api_key of the accunt.
    :type api_key: :obj:`str`
    """

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        """api key from the account"""
        self.checking_key()
        """checking the API key"""


    def get_balance(self) -> float:
        """
        Sends a request to Grizzly CMS. Gets the account balance.
        """
        response = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={self.api_key}&action=getBalance").text
        return response.split(":")[1]
    

    def get_cost(self, service: str, country:str) -> int:
        """
        Sends a request to Grizzly CMS. Gets the price of the room for the service from the specified country.

        :param service: The ID service to which the request will go.
        :type service: :obj:`str`

        :param country: The ID country to which the request will go.
        :type country: :obj:`str`
        """
        if service not in ALL_SERVICE_CODES:
            raise InvalidServiceCodeError
        elif country not in ALL_COUNTRY_CODES:
            raise InvalidCountryCodeError
        
        response = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={self.api_key}&action=getPrices&service={service}&country={country}").json()
        return int(response[country][service]["cost"])
    

    def get_count(self, service: str, country: str) -> int:
        """
        Sends a request to Grizzly CMS. Gets the count of the room for the service from the specified country.

        :param service: The ID service to which the request will go.
        :type service: :obj:`str`

        :param country: The ID country to which the request will go.
        :type country: :obj:`str`
        """
        if service not in ALL_SERVICE_CODES:
            raise InvalidServiceCodeError
        elif country not in ALL_COUNTRY_CODES:
            raise InvalidCountryCodeError
        
        response = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={self.api_key}&action=getPrices&service={service}&country={country}").json()
        return int(response[country][service]["count"])
    

    def get_number(self, service: str, country: str) -> str:
        """
        Sends a request to Grizzly CMS. Get the order ID and phone number for the specified service and country.

        :param service: The ID service to which the request will go.
        :type service: :obj:`str`

        :param country: The ID country to which the request will go.
        :type country: :obj:`str`
        """
        if service not in ALL_SERVICE_CODES:
            raise InvalidServiceCodeError
        elif country not in ALL_COUNTRY_CODES:
            raise InvalidCountryCodeError
        
        response = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={self.api_key}&action=getNumber&service={service}&country={country}").text
        if response == 'NO_NUMBERS':
            raise ValueError("Grizzly sms: There are no numbers; the number has not been issued — repeat the request or select another country.")
        else:
            return str(response.split("ACCESS_NUMBER:")[1])
        

    def change_status(self, id: str, status: str) -> str:
        """
        Sends a request to Grizzly CMS. Changes the activation status.

        :param id: The order ID to which the request will go.
        :type id: :obj:`str`

        :param status: The status you want to change to.
        :type status: :obj:`str`

        -1 — cancel activation;
        1 — inform about the readiness of the number (SMS sent to the number);
        3 — inform about waiting for a new code to the same number;
        6 — complete activation;
        8 — cancel activation.
        """
        if status not in ALL_STATUSES:
            raise ValueError("Grizzly sms: Invalid status code.")
        
        response = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={self.api_key}&action=setStatus&status={status}&id={id}").text
        
        error_classes = {
            'NO_ACTIVATION': NoIdActivationError,
            'BAD_ACTION': BadActionError,
            'ERROR_SQL': SqlError,
            'BAD_SERVICE': BadServiceError,
            'BAD_STATUS': BadStatusError
        }

        if response in error_classes:
            raise error_classes[response]
        else:
            return response
        
    def get_code(self, id: str):
        """
        Sends a request to Grizzly CMS. Gets the order status or code if already available.

        :param id: the order ID to which the request will go.
        :type id: :obj:`str`

        """
        response = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={self.api_key}&action=getStatus&id={id}").text

        error_classes = {
            'NO_ACTIVATION': NoIdActivationError,
            'BAD_ACTION': BadActionError,
        }

        if response in error_classes:
            raise error_classes[response]
        else:
            return response



    def checking_key(self) -> bool:
        response = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={self.api_key}&action=getBalance").text
        if response in ("NO_KEY", "BAD_KE"):
            raise ValueError("Grizzly sms: Invalid API key.")
            return False
        else:
            return True
import re
import requests
from collections import OrderedDict


class PublicIPHelper(object):
    '''
    Get public IP
    '''
    time_out = 3
    ip_finders = {
        "http://icanhazip.com": 0,
        "https://checkip.amazonaws.com": 0,
        "http://members.3322.org/dyndns/getip": 0,
        "https://ipapi.co/ip/": 0,
        "https://ipv4.ngx.hk": 0,
        "https://api.ipify.org": 0,
        "http://icanhazip.com/": 0,
        "http://www.loopware.com/ip.php": 0,
        "https://ident.me": 0,
        "http://myip.dnsomatic.com": 0,
        "https://ipecho.net/plain": 0
    }
    ipv4_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')

    @staticmethod
    def sort_dict_by_value(dic, reverse=False):
        return OrderedDict((k, dic[k]) for k in
                           sorted(dic, key=dic.get, reverse=reverse))

    @classmethod
    def get_my_public_ip(cls):
        """
        Get public IP

        @return  public IP address or None
        """
        exist_bad_finder = False
        for finder, _ in cls.ip_finders.items():
            ip = cls._get_ip(finder)
            if ip is None:
                exist_bad_finder = True
                cls.ip_finders[finder] += 1
            else:
                break
        if exist_bad_finder:
            cls.ip_finders = cls.sort_dict_by_value(cls.ip_finders)
        return ip

    @classmethod
    def _get_ip(cls, finder):
        """
        Get public IP

        @param finder: url for finding IP
        @return  public IP address or None
        """
        try:
            ret = requests.get(finder, timeout=cls.time_out)
        except requests.RequestException as ex:
            return None

        if ret.status_code != requests.codes.ok:
            return None

        ip = ret.content.decode('utf-8').strip()
        if cls.ipv4_pattern.match(ip):
            return ip
        else:
            return None


if __name__ == "__main__":
    print(PublicIPHelper.ip_finders)
    ip = PublicIPHelper.get_my_public_ip()
    print(PublicIPHelper.ip_finders)
    print(ip)


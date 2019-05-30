#!/usr/bin/env python3

from requests import get
import argparse
import warnings
from sys import stderr

warnings.filterwarnings('ignore')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        '''Fingerprint an iLo server. All unimportant output is printed
        to sterr, so 2>/dev/null to mute that.
        ''')
    parser.add_argument('--url','-u',required=True,
        help='''URL to fingerprint. Do not include a path as it is hardcoded
        in this terrible script.
        ''')
    parser.add_argument('--path','-p',
        default='/json/login_session',
        help='''Path to JSON object containing the version. Should this devate
        from the default, the script will likely fail. This is a "just in case"
        option. Default: %(default)s.
        ''')

    args = parser.parse_args()

    url = args.url+args.path

    print('- HP iLO Fingerprinter',file=stderr)
    print('- Checking url: '+args.url)
    print('- Making the request',file=stderr)
    print('- If this times out, check the http_proxy and https_proxy variables!',file=stderr)
    
    resp = get(url,verify=False)
    j = resp.json()
    
    print('- Done! Printing Useful information.',file=stderr)

    output = f'full_url: {url}'
    output += '\nversion: '+j['langs'][0]['version']
    for k in ['ldap_enabled','kerberos_enabled','license_directory_auth']:

        output += f'\n{k}: '+str(j[k])

    print(output)

    

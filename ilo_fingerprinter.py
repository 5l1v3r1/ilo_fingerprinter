#!/usr/bin/env python3

from requests import get
import argparse
import warnings
from pathlib import Path
from sys import stderr


warnings.filterwarnings('ignore')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        '''Fingerprint an iLo server. All unimportant output is printed
        to sterr, so 2>/dev/null to mute that.
        ''')
    parser.add_argument('--urls','-us',required=True,
        nargs='+',
        help='''URL to fingerprint. Do not include a path as it is hardcoded
        in this terrible script. Will accept either a series of static URLs
        or a file name.
        ''')
    parser.add_argument('--path','-p',
        default='/json/login_session',
        help='''Path to JSON object containing the version. Should this devate
        from the default, the script will likely fail. This is a "just in case"
        option. Default: %(default)s.
        ''')

    args = parser.parse_args()
    
    print('- HP iLO Fingerprinter',file=stderr)
    print('- If this times out, check the http_proxy and https_proxy variables!\n',file=stderr)

    urls = []

    for u in args.urls:

        if not Path(u).exists():
            urls.append(u+args.path)
        else:
            with open(u) as infile:
                for iu in infile:
                    urls.append(iu.strip()+args.path)


    for url in urls:

        try:

            print('- Checking url: '+url,file=stderr)
            print('- Making the request',file=stderr)
            
            resp = get(url,verify=False)
            j = resp.json()
            
            print('- Done! Printing Useful information.\n',file=stderr)
            ml = 'license_directory_auth'.__len__()
        
            output = '{s: <{ml}} {url}'.format(s='full_url:',ml=ml,url=url)
            output += '\n{s: <{ml}} {v: <{ml}}'.format(s='version:',v=j['langs'][0]['version'],ml=ml)
            for k in ['ldap_enabled','kerberos_enabled','license_directory_auth']:
        
                output += '\n{k: <{ml}} {v: <{v}}'.format(k=k,v=str(j[k]),ml=ml)
        
            print(output+'\n')

        except Exception as e:

            print('Fingerprint failed',file=stderr)
            print(e,file=stderr)

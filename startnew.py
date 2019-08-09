from __future__ import print_function

import os
import os.path
import subprocess
import sys
import time

import requests
from requests.exceptions import ConnectionError

from browser_automate import automated_browser
from zapv2 import ZAPv2


class zap_scanner:
    def __init__(self, proxy_port="http://127.0.0.1:9999/", api_key='zap'):
        self.proxy_port = proxy_port
        self.proxy = {
            "httpProxy": proxy_port,
            "ftpProxy": proxy_port,
            "sslProxy": proxy_port,
            "noProxy": None,
            "proxyType": "MANUAL",
            "autodetect": False
        }

        self.api_key = api_key
        self.zap = ZAPv2(apikey=api_key, proxies=self.proxy)

    def create_session(self, sessionName):
        self.zap.core.new_session(name=sessionName, overwrite=True)

    def run_active_scan(self, target):
        """
        run a active scan against target using the initialized zap object
        a active scan will run through all available plugins like SQLi, Path Traversal, etc. just like when you would
        use the UI and start an attack against TARGET
        """
        print('Scanning target {0}'.format(target))
        self.zap.ascan.scan(target, True, apikey=self.api_key)
        time.sleep(3)
        while int(self.zap.ascan.status()) < 3:
            print('Scan progress %: ' + self.zap.ascan.status(), end='\r')
            time.sleep(0.5)

    def scan_all_sites(self):
        for site in self.zap.core.sites:
            self.run_active_scan(site)
        print('scan completed')

    def gen_report(self, report_file, force=True):
        '''
        generates a report in `reporttype`
        :param reporttype: html or xml
        '''

        # zap.core.htmlreport seems to be broken so we're using json2html for a very basic report in html
        # report = zap.core.htmlreport()

        if os.path.isfile(report_file) and force:
            try:
                os.remove(report_file)
            except IOError as e:
                print('Unable to remove {0}'.format(report_file))
        elif os.path.isfile(report_file):
            print('File {0} exists and --force was not used. '
                  'Please remove file and re-run your scan. Exiting.'.format(report_file))
            sys.exit(1)
            # try:
        with open(report_file, 'w') as f:
            url = f'{self.proxy_port}OTHER/core/other/htmlreport/?apikey={self.api_key}'
            data = requests.get(url)
            f.write(data.text)
        print(f'report saved to  {report_file}')
        # print('Success: {1} report saved to {0}'.format(report_file))

    def start_zap(self, zapsh='zap.sh'):
        """
        starts zap
        """
        print('Starting ZAP ...')
        subprocess.Popen([zapsh, '-config', 'api.key=' + self.api_key], stdout=open(os.devnull, 'w'))
        print('Waiting for ZAP to load, 10 seconds ...')
        print('Use api-key {0} to interact with my API ...'.format(self.api_key))
        while True:
            try:
                requests.get(self.proxy['httpProxy'])
                break
            except ConnectionError as e:
                time.sleep(1)
        print('zap is running')

    def stop_zap(self):
        """
        stops zap
        """
        self.zap.core.shutdown()


scanner = zap_scanner()
scanner.start_zap()
scanner.create_session('newsession.session')
automated_browser('127.0.0.1:9999')
scanner.scan_all_sites()
scanner.gen_report('reppp.html')
scanner.stop_zap()

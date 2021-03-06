from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

import os
app = Flask(__name__)
PORT = os.environ.get('PORT') or 5057

#Working Path: /usr/local/bin:/usr/bin:/bin:/app/vendor/:/app/vendor/firefox:/app/vendor/geckodriver
#firefox_binary = FirefoxBinary('/app/vendor/firefox/firefox')
FF_options = webdriver.FirefoxOptions()
FF_profile = webdriver.FirefoxProfile()
FF_options.add_argument("-headless")
FF_profile.set_preference("dom.webdriver.enabled", False)
FF_profile.set_preference('useAutomationExtension', False) 
FF_profile.set_preference("media.peerconnection.enabled", False) #Disable WebRTC
FF_profile.set_preference("network.proxy.socks_remote_dns", True) #Make DNS requests through the proxy (By default, DNS requests wont be made through the proxy)
FF_profile.update_preferences()


@app.route("/get")
def getcurrIp():
    try:
        #driver = webdriver.Firefox(options=FF_options, firefox_profile=FF_profile, executable_path='/app/vendor/geckodriver/geckodriver', firefox_binary=firefox_binary)
        driver = webdriver.Firefox(options=FF_options, firefox_profile=FF_profile, executable_path=os.environ.get("GECKODRIVER_PATH"),firefox_binary=FirefoxBinary(os.environ.get("FIREFOX_BIN")))
        driver.get("https://icanhazip.com")
        ipaddr = driver.page_source
        driver.close()
        return jsonify({'status': 1, 'ip': ipaddr})
    except Exception as e:
        return jsonify({'status': 0, 'error': str(e)}), 500

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(port=PORT, debug=True)

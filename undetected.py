import time

import undetected_chromedriver
from undetected_chromedriver.options import ChromeOptions
import time

def main():

    options = ChromeOptions()
    options.add_argument()
    # options.add_argument("--no-startup-window")
    browser = undetected_chromedriver.Chrome(options)
    browser.get('https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/497')
    time.sleep(100)

if __name__ == '__main__':
    main()
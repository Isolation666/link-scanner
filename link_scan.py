import ssl, sys
import urllib.request
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List


class LinkScanner(unittest.TestCase):

    def setUp(self):
        """Set up an browser driver before each test."""
        my_options = Options()
        my_options.headless = True

        assert my_options.headless

        path_to_driver = ''  # Your PATH/TO/DRIVER
        self.browser = webdriver.Chrome(path_to_driver, options=my_options)
        self.browser.implicitly_wait(10)

        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def get_links(self, link: str) -> List[str]:
        """Find all links on page at the given url.

        Returns:
            a list of all unique hyperlinks on the page,
            without page fragments or query parameters.
        """
        list_link = []
        self.browser.get(link)
        tag_name = self.browser.find_elements_by_tag_name('a')
        for web in tag_name:
            href = web.get_attribute('href')
            if href.split('#')[0] not in list_link:
                list_link.append(href)
            elif href.split('?')[0] not in list_link:
                list_link.append(href)
        return list_link

    def is_valid_url(self, link: str) -> bool:
        request_link = urllib.request.Request(link)
        request_link.get_method = lambda: 'HEAD'
        if urllib.request.urlopen(request_link, context=self.context):
            return True
        else:
            return False

    def invalid_urls(self, link_list: List[str]) -> List[str]:
        """Validate the urls in link_list and return a new list containing
        the invalid or unreachable urls.
        """
        list_of_invalid = []
        for link in link_list:
            if not self.is_valid_url(link):
                list_of_invalid.append(link)
        return list_of_invalid


if __name__ == '__main__':
    scanner = LinkScanner()
    if len(sys.argv) > 1:
        get_list = scanner.get_links(sys.argv[1])
        for link in get_list:
            print(link)
        print('Bad Links:')
        bad_link_list = scanner.invalid_urls(get_list)
        for bad in bad_link_list:
            print(bad)
    else:
        print(f'Usage:  python3 {sys.argv[0]} url')
        print()
        print('Test all hyperlinks on the given url.')

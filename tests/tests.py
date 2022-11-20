from mock_server import MockServer
import unittest
import requests

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from web_scrapper import scrape


def generate_url_mapping():
    base_dir = os.path.split(__file__)[0]

    mapping = {}
    with open(os.path.join(base_dir, 'templates/lvl_1.html')) as f:
        mapping['/'] = f.read()

    with open(os.path.join(base_dir, 'templates/lvl_2.html')) as f:
        mapping['/lvl_2'] = f.read()

    with open(os.path.join(base_dir, 'templates/lvl_3.html')) as f:
        mapping['/lvl_3'] = f.read()

    with open(os.path.join(base_dir, 'templates/lvl_4.html')) as f:
        mapping['/lvl_4'] = f.read()

    return mapping


class Tests(unittest.TestCase):
    def test_level_1(self):
        address = ("http://127.0.0.1/", )

        output = scrape(address)
        expected = map(lambda x: address[0] + x, ['', '?hi', 'lvl_2'])    
                
        self.assertCountEqual(expected, output)
    
    def test_level_2(self):
        address = ("http://127.0.0.1/", )

        output = scrape(address, depth=1)
        expected = map(lambda x: address[0] + x, ['', '?hi', 'lvl_2', 'lvl_3', 'lvl_2?hi'])    
                
        self.assertCountEqual(expected, output)


if __name__ == "__main__":
    server = MockServer(generate_url_mapping())
    server.start()
    unittest.main(exit=False)    
    server.stop()

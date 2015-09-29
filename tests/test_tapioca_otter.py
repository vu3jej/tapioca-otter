# coding: utf-8

import unittest

from tapioca_otter import Otter


class TestTapiocaOtter(unittest.TestCase):

    def setUp(self):
        self.wrapper = Otter()


if __name__ == '__main__':
    unittest.main()

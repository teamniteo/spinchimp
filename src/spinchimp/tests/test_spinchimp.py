# -*- coding: utf-8 -*-

from spinchimp import SpinChimp

import unittest2 as unittest
import mock


class TestApi(unittest.TestCase):

    def setUp(self):
        """Utility code shared among all tests."""
        self.sc = SpinChimp('foo@bar.com', 'test_api_key', 'test_api_name')

    def test_init(self):
        """Test initialization of SpinChimp.

        SpinChimp is initialized on every test run and stored as self.sc.
        We need to test for stored values if class was
        initialized correctly.
        """
        self.assertEquals(self.sc._email, 'foo@bar.com')
        self.assertEquals(self.sc._apikey, 'test_api_key')
        self.assertEquals(self.sc._aid, 'test_api_name')
        self.assertIsInstance(self.sc, SpinChimp)

    @mock.patch('spinchimp.urllib2')
    def test_unique_variation_default_call(self, urllib2):
        """Test call of unique_variation() with default values."""
        # mock response from SpinChimp
        mocked_response = 'My cat is über cold.'
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.sc.unique_variation(u'My cat is über cool.'),
            u'My cat is über cold.',
        )

    @mock.patch('spinchimp.urllib2')
    def test_text_with_spintax_default_call(self, urllib2):
        """Test call of text_with_spintax_call() with default values."""
        # mock response from SpinChimp
        mocked_response = 'My cat is über {cold|cool}.'
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.sc.text_with_spintax(u'My cat is über cool.'),
            u'My cat is über {cold|cool}.',
        )

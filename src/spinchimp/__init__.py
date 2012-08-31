# -*- coding: utf-8 -*-

import urllib
import urllib2

from spinchimp import exceptions as ex


class SpinChimp(object):
    """A class representing the Spin Chimp API
    (http://spinchimp.com/api).
    All articles must be in UTF-8 encoding!
    """
    URL = 'http://api.spinchimp.com/{method}?'
    """URL for invoking the API"""

    TIMEOUT = 10

    DEFAULT_PARAMS_SPIN = {
        'quality': '4',
        'posmatch': '3',
        'protectedterms': '',
        'rewrite': '0',
        'phraseignorequality': '0',
        'spinwithinspin': '0',
        'spinwithinhtml': '0',
        'applyinstantunique': '0',
        'fullcharset': '0',
        'spintidy': '0',
        'tagprotect': '',
        'maxspindepth': '0',
    }

    def __init__(self, email, apikey, aid=''):
        """AID is Application ID or application name"""
        self._email = email
        self._apikey = apikey
        self._aid = aid

    def _get_param_value(self, param_name, params, def_params=DEFAULT_PARAMS_SPIN):
        """ Returns parameter value or use default.
        """
        if param_name in params:
            return params[param_name]

        elif param_name in def_params:
            return def_params[param_name]

        else:
            raise ex.WrongParameterName(param_name)

    def _value_has(self, param, values, params):
        """ Raise WrongParameterVal if
        value of param is not in values.
        """
        val = self._get_param_value(param, params)
        if not val in values:
            raise ex.WrongParameterVal(param, val)

    def _value_is_int(self, param, params):
        """ Raise WrongParameterVal if
        value of param is not integer.
        """
        val = self._get_param_value(param, params)
        try:
            int(val)
        except ValueError:
            raise ex.WrongParameterVal(param, val)

    def _validate(self, params):
        """ Checks every single parameter and
        raise error on wrong key or value.
        """

        # remove entries with None value
        for i, j in params.iteritems():
            if j is None:
                del(i)

        self._value_has('quality', ['1', '2', '3', '4', '5'], params)

        self._value_has('posmatch', ['0', '1', '2', '3', '4'], params)

        self._value_has('rewrite', ['0', '1'], params)

        self._value_has('phraseignorequality', ['0', '1'], params)

        self._value_has('spinwithinspin', ['0', '1'], params)

        self._value_has('spinwithinhtml', ['0', '1'], params)

        self._value_has('applyinstantunique', ['0', '1'], params)

        self._value_has('fullcharset', ['0', '1'], params)

        self._value_has('spintidy', ['0', '1'], params)

        self._value_has('maxspindepth', ['0', '1'], params)

        return True

    def unspun(self, text, dontincludeoriginal=0, reorderparagraphs=0):
        """ Generates an unspun doc from one with spintax.
        Optionally reorders paragraphs and removes original word.

        :param text: text in spintax format
        :type text: string
        :param dontincludeoriginal: 0 (False) or 1 (True)
        :type dontincludeoriginal: integer
        :param reorderparagraphs: 0 (False) or 1 (True)
        :type reorderparagraphs: integer

        :return: unique text
        :rtype: dictionary
        """

        params = {
            'dontincludeoriginal': str(dontincludeoriginal),
            'reorderparagraphs': str(reorderparagraphs)
        }

        self._value_has('dontincludeoriginal', ['0', '1'], params)
        self._value_has('reorderparagraphs', ['0', '1'], params)

        response = self._send_request(
            method='GenerateSpin',
            text=text,
            params=params
        )
        return response

    def word_density(self, text, minlength=3):
        """ Calculates the word densities of words and phrases in the article.

        :param text: original text
        :type text: string
        :param minlength: minimum length
        :type minlength: integer

        :return: words as keys in dictionary and percents as values
        :rtype: dictionary
        """

        params = {'minlength': str(minlength)}

        self._value_is_int('minlength', params)

        response = self._send_request(
            method='CalcWordDensity',
            text=text,
            params=params
        )
        return dict([atr.split(',') for atr in response.split('|')])

    @staticmethod
    def test_connection():
        """ Static method that checks server status.
        The server returns 'OK' on successful connection.
        """
        urldata = SpinChimp.URL.format(method='TestConnection')
        req = urllib2.Request(urldata, data='')
        try:
            response = urllib2.urlopen(req, timeout=SpinChimp.TIMEOUT)
        except urllib2.URLError as e:
            raise ex.NetworkError(str(e))

        return response.read()

    def quota_all(self):
        """ The server returns:
        daily limit, remaining daily limit, extended quota and bulk quota
        in dictionary for this account.
        """
        response = self._send_request(
            method='QueryStats',
            text='',
            params={'simple': '0'}
        )
        return dict([atr.split(',') for atr in response.split('|')])

    def quota_left_total(self):
        """ The server returns remaining query times of this account.
        """
        return self._send_request(
            method='QueryStats',
            text='',
            params={'simple': '1'}
        )

    def text_with_spintax(self, text, params=None):
        """ Return processed spun text with spintax.

        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: processed text in spintax format
        :rtype: string
        """

        if not params:
            params = self.DEFAULT_PARAMS_SPIN.copy()
        else:
            self._validate(params)

        params['rewrite'] = '0'

        return self._send_request(
            method='GlobalSpin',
            text=text,
            params=params
        )

    def unique_variation(self, text, params=None):
        """ Return a unique variation of the given text.

        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: processed text
        :rtype: string
        """

        if not params:
            params = self.DEFAULT_PARAMS_SPIN.copy()
        else:
            self._validate(params)

        params['rewrite'] = '1'

        return self._send_request(
            method='GlobalSpin',
            text=text,
            params=params
        )

    def _send_request(self, method, text, params):
        """ Invoke Spin Chimp API with given parameters and return its response.

        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: API's response (article)
        :rtype: string
        """

        for k, v in params.items():
            params[k] = v.encode("utf-8")

        params['email'] = self._email
        params['apikey'] = self._apikey
        params['aid'] = self._aid

        url = self.URL.format(method=method) + urllib.urlencode(params)
        textdata = text.encode('utf-8')

        try:
            response = urllib2.urlopen(url, data=textdata, timeout=self.TIMEOUT)
        except urllib2.URLError as e:
            raise ex.NetworkError(str(e))

        result = response.read().decode("utf-8")

        if result.lower().startswith('failed:'):
            self._raise_error(result[8:])

        return result

    def _raise_error(self, api_response):
        raise ex.SpinChimpError(api_response)

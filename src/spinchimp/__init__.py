# -*- coding: utf-8 -*-

import urllib
import urllib2

from spinchimp import exceptions as ex


class SpinChimp(object):
    """A class representing the Spin Chimp API
    (http://spinchimp.com/api).
    """
    URL = u'http://api.spinchimp.com/{method}?'
    """URL for invoking the API"""

    TIMEOUT = 10

    DEFAULT_PARAMS_CALC = {
        'minlength': '3',
    }

    DEFAULT_PARAMS_GEN = {
        'dontincludeoriginal': '0',
        'reorderparagraphs': '0',
    }

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

    def _get_param_value(self, param_name, params, def_params):
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

    # TODO
    def _validate(self, params):
        """ Checks every single parameter and
        raise error on wrong key or value.
        """
        # remove entries with None value
        for i, j in params.iteritems():
            if j is None:
                del(i)

        self._value_has('protecthtml', ['0', '1'], params)

        self._value_has('usehurricane', ['0', '1'], params)

        self._value_has('spinhtml', ['0', '1'], params)

        self._value_has('percent', map(lambda x: str(x), range(0, 101)), params)

        self._value_has('phrasecount', ['2', '3', '4', 'X'], params)

        self._value_has('Chartype', ['1', '2', '3'], params)

        self._value_has('replacetype', map(lambda x: str(x), range(0, 6)), params)

        self._value_has('autospin', ['0', '1'], params)

        self._value_has('convertbase', ['0', '1'], params)

        self._value_has('pos', ['0', '1'], params)

        self._value_has('Orderly', ['0', '1'], params)

        self._value_is_int('Wordscount', params)

        self._value_is_int('spinfreq', params)

        # allow any combination of '[]','()','<-->'
        val = self._get_param_value('tagprotect', params)
        if Set(val.split(',')).difference(Set(['[]', '()', '<-->'])):
            raise ex.WrongParameterVal('tagprotect', val)

        self._value_has('spintype', ['0', '1'], params)

        self._value_has('UseGrammarAI', ['0', '1'], params)

        self._value_has('onecharforword', ['0', '1'], params)

        self._value_has('wordquality', ['0', '1', '2', '3', '9'], params)

        self._value_has('original', ['0', '1'], params)

        return True

    def test_connection(self):
        """ The server returns 'OK' on successful connection.
        """
        urldata = self.URL.format(method='TestConnection')
        req = urllib2.Request(urldata, data='')
        try:
            response = urllib2.urlopen(req, timeout=self.TIMEOUT)
        except urllib2.URLError as e:
            raise ex.NetworkError(str(e))

        result = response.read()

        if result.lower().startswith('failed:'):
            self._raise_error(result[8:])
        return result

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

    # TODO
    def text_with_spintax(self, text, params=None):
        """ Return processed spun text with spintax.

        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: processed text in spintax format
        :rtype: string
        """

        if params is None:
            params = self.DEFAULT_PARAMS
        else:
            self._validate(params)

        params['spintype'] = '0'

        return self._send_request(text=text, params=params)

    # TODO
    def unique_variation(self, text, params=None):
        """ Return a unique variation of the given text.

        :param text: original text that needs to be changed
        :type text: string
        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: processed text
        :rtype: string
        """

        if params is None:
            params = self.DEFAULT_PARAMS
        else:
            self._validate(params)

        params['spintype'] = '1'

        return self._send_request(text=text, params=params)

    def _send_request(self, method, text, params):
        """ Invoke Spin Chimp API with given parameters and return its response.

        :param params: parameters to pass along with the request
        :type params: dictionary

        :return: API's response (article)
        :rtype: string
        """

        for k,v in params.items():
            params[k] = v.encode("UTF8")

        params['email'] = self._email
        params['apikey'] = self._apikey
        params['aid'] = self._aid

        urldata = self.URL.format(method=method) + urllib.urlencode(params)
        textdata = text.encode("UTF8")
        req = urllib2.Request(urldata, data=textdata)
        try:
            response = urllib2.urlopen(req, timeout=self.TIMEOUT)
        except urllib2.URLError as e:
            raise ex.NetworkError(str(e))

        result = response.read()

        if result.lower().startswith('failed:'):
            self._raise_error(result[8:])

        return result

    def _raise_error(self, api_response):
        lower = api_response.lower()
        error = None

        if lower.startswith("login error"): # TODO
            error = ex.LoginError(api_response)

        raise error if error else ex.SpinChimpError(api_response)

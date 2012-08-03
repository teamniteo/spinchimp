==================================
Python bindings for SpinChimp API.
==================================

`Spin Chimp <http://spinchimp.com>`_ is an online
service for spinning text (synonym substitution) that creates unique version(s)
of existing text. This package provides a way to easily interact with
`SpinChimp API <http://spinchimp.com/api>`_.
Usage requires an API subscription, `get it at <http://spinchimp.com/api>`_.

* `Source code @ GitHub <https://github.com/niteoweb/spinchimp>`_


Install within virtualenv
=========================

.. sourcecode:: bash

    $ virtualenv foo
    $ cd foo
    $ git clone https://github.com/niteoweb/spinchimp
    $ bin/pip install spinchimp/

    # running tests:
    $ bin/pip install unittest2 mock
    $ bin/python -m unittest discover -s spinchimp/src/spinchimp/tests


Buildout
========

.. sourcecode:: bash

    $ git clone https://github.com/niteoweb/spinchimp
    $ cd spinchimp
    $ python bootstrap.py
    $ bin/buildout

    # running tests:
    $ bin/py -m unittest discover -s src/spinchimp/tests

    # check code for imperfections
    $ bin/vvv src/spinchimp


Usage
=====

.. sourcecode:: python

    >>> import spinchimp
    >>> sc = spinchimp.SpinChimp("<youremail>", "<yourapikey>", "<yourappname>")

    >>> sc.text_with_spintax(text="My name is Ovca!")
    "{I am|I'm|My friends call me|Throughout southern california|Im} Ovca!"

    >>> sc.unique_variation(text="My name is Ovca!")
    "Im Ovca!"

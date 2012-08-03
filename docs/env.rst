.. _conventions:

=====================
Developer environment
=====================

Dependencies
============

**A C/C++ compilation environment**

  On a Debian based system install the ``build-essential`` package. On OS X,
  install `XCode <http://developer.apple.com/technologies/tools/xcode.html>`_
  and `MacPorts <http://www.macports.org>`_.

**Git**

  On a Debian based system install the ``git-core`` package. On OS X, get the
  latest version from http://code.google.com/p/git-osx-installer/.

**Python 2.7**

  On a Debian based system install the ``python2.7-dev`` package. On OS X (and
  others) use the `buildout.python <http://TODO>`_ to prepare a clean Python
  installation.


Build
=====

First, you need to `clone` the git repository on GitHub to download the code
to your local machine::

    $ git clone git@github.com:niteoweb/spinchimp.git

What follows is initializing the `buildout` environment::

    $ cd spinchimp
    $ python2.7 bootstrap.py

And now you can `run the buildout`. This will fetch and configure tools and libs
needed for developing `spinchimp`::

    $ bin/buildout


Verify
======

Your environment should now be ready. Test that by using the ``py`` Python
interpreter inside the ``bin`` directory, which has `spinchimp` installed
in it's path:

.. sourcecode:: python

    $ bin/py

    >>> from spinchimp import SpinChimp
    >>> sc = SpinChimp('api_key', 'username', 'password')
    >>> sc.unique_variation('Some random text.')
    u"Some random lines."

The code for `spinchimp` lives in ``src/``. Make a change and re-run
``bin/py`` to see it resembled!

Moreover, you should have the following tools in the ``bin/`` directory, ready
for use:

**vvv**

    A sintax validation tool.

**sphinbuilder**

    A tool for testing HTML render of `spinchimp`'s documentation.

**longtest**

    A tool for testing the HTML render of the package description (part of
    ``zest.releaser``).

**mkrelease**

    A tool we use for releasing a new version (part of ``jarn.mkrelease``).

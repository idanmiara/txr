TXR: the teXt aRchiver
########################

Mainly purposed for archiving text files as text files, but can archive any file and not only as text.
`txr` was inspired by tar, gzip and gunzip.
License: GPL v3 or later.

The `txr` format is composed of two files with the following extensions:

* `.txr` - a comma delimited index file (text).
* `.txd` - a data file (can either be text or binary). By default it is concatenation of the input files, separated by a sentinel).


`txr` uses:

* sha256 (for optional hashing, by default).
* zlib (for optional compressing).
* cryptography (for optional encrypting).


Install:
===========

>>> pip install txr

`txr` is a standalone application (It consist of a single source file `txr.py`).
Using the above command installs `txr` both as a console script and as a python module.
If you wish you could also just copy `txr.py` and use it as a standalone app.


Basic Usage:
=================

Archive a folder (or a single file)

>>> txr c:\my_input

Extracting a `txr` file:

>>> txr -x c:\my_input.txr

See detailed help with all available parameters:

>>> txr

Contributions are welcome.


.. example

Example
=======

Usage
-----

.. code-block:: bash

    $ python example.py -h
    usage: example.py [-h] [-r] {math,echo} ...

    Argon example.

    positional arguments:
      {math,echo}

    optional arguments:
      -h, --help     show this help message and exit
      -r, --reverse  reverse output

Math Sub-Command Group
``````````````````````

.. code-block:: bash

    $ python example.py math -h
    usage: example.py math [-h] {sum,hex} ...

    positional arguments:
      {sum,hex}
        hex       convert number to hex

    optional arguments:
      -h, --help  show this help message and exit
    $ python example.py math sum 1 2 3
    6
    $ python example.py math hex 1234567
    0x12d687


Echo Sub-Command
````````````````

.. code-block:: bash

    $ python example.py echo -h
    usage: example.py echo [-h] [-u] string

    positional arguments:
      string

    optional arguments:
      -h, --help  show this help message and exit
      -u          convert to uppercase
    $ python example.py echo fooo
    fooo
    $ python example.py -r echo -u fooo
    OOOF


Source Code
-----------
.. literalinclude:: ../../example.py

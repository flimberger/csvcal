===================================
CSVCAL - iCalendar to CSV converter
===================================

An iCalendar to CSV converter.
The original purpose was to make the events bulk-editable with LibreOffice Calc.

Caveats
=======

All sub-components of ``VEVENT`` are removed during the conversion.
Also,
all properties of ``VCALENDAR`` except for ``VERSION:2.0`` are removed.

Usage
=====

``Csvcal.py`` works on standard input and output::

    ./csvcal.py -tocsv <file.ics >file.csv
    ./csvcal.py -toics <file.csv >new_file.ics

License
=======

BSD 2-Clause (Simplified)

Dependencies
============

- `icalendar <https://pypi.org/project/icalendar/>`_

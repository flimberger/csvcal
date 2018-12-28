import io

import csvcal


def test_conversion():
    ical_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTAMP:20181227T230400
UID:bde8a9d4-0a2b-11e9-84ca-507b9d43f840
END:VEVENT
END:VCALENDAR
"""

    with io.StringIO(ical_data) as ical, io.StringIO() as csv_data, \
            io.StringIO() as result:
        csvcal.to_csv(csv_data, ical)
        csv_data.seek(0)
        csvcal.to_ics(result, csv_data)

        assert result.getvalue() == ical_data

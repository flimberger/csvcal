import csvcal

from io import StringIO


def compare_conversion(ical_data):
    with StringIO(ical_data) as ical, StringIO() as csv_data, \
            StringIO() as result:
        csvcal.to_csv(csv_data, ical)
        csv_data.seek(0)
        csvcal.to_ics(result, csv_data)

        assert result.getvalue() == ical_data


def test_minimal():
    ical_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTAMP:20181227T230400
UID:bde8a9d4-0a2b-11e9-84ca-507b9d43f840
END:VEVENT
END:VCALENDAR
"""

    compare_conversion(ical_data)


def test_text_escapes():
    ical_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:summary\\,summary\\;summary\\\\summary\\nsummary
DTSTAMP:20181228T155600
UID:261b6b0d-0ab9-11e9-b35b-507b9d43f840
COMMENT:comment\\,comment\\;comment\\\\comment\\ncomment
DESCRIPTION:descr\\,descr\\;descr\\\\descr\\ndescr
END:VEVENT
END:VCALENDAR
"""

    compare_conversion(ical_data)


def test_property_list():
    ical_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTAMP:20181228T200000
UID:4d7d5065-0adb-11e9-b35b-507b9d43f840
EXDATE:20181228
EXDATE:20181229
END:VEVENT
END:VCALENDAR
"""

    compare_conversion(ical_data)


def test_rrule_content():
    ical_data = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTAMP:20181229T000200
UID:20d6385e-0afd-11e9-b35b-507b9d43f840
RRULE:FREQ=WEEKLY;UNTIL=20190731T220000Z;INTERVAL=4;BYDAY=MO,TU,TH,FR
END:VEVENT
END:VCALENDAR
"""

    compare_conversion(ical_data)

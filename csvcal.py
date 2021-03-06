#!/usr/bin/env python3

import sys

from collections import OrderedDict
from csv import DictReader, writer as CSVWriter
from icalendar import Calendar, Event
from icalendar.prop import vDDDLists, vDDDTypes, vRecur


def main():
    if len(sys.argv) != 2:
        usage()

    operation = sys.argv[1]

    if sys.argv[1] == '-tocsv':
        to_csv(sys.stdout, sys.stdin)
    elif operation == '-toics':
        to_ics(sys.stdout, sys.stdin)
    else:
        print('invalid argument "{}"'.format(operation), file=sys.stderr)
        usage()


def usage():
    print('usage:\tcsvcal -tocsv\n\tcsvcal -toics', file=sys.stderr)
    sys.exit(1)


def to_csv(output_file, input_file):
    calendar = create_calendar(input_file)
    property_names = create_properties_list(calendar)
    write_events_to_csv(output_file, calendar, property_names)


def create_calendar(input_file):
    try:
        return Calendar.from_ical(input_file.read())
    except ValueError as e:
        handle_parse_error(e)


def handle_parse_error(e):
    print('failed to parse input: {}'.format(str(e)))
    sys.exit(1)


def create_properties_list(calendar):
    properties = OrderedDict()
    for event in get_events(calendar):
        for prop in get_properties(event):
            property_name = prop[0]
            properties[property_name] = True
    return properties.keys()


def get_events(calendar):
    for component in calendar.walk():
        if component.name == 'VEVENT':
            yield component


def get_properties(event):
    for prop in event.property_items(recursive=False):
        property_name = prop[0]
        if property_name not in ('BEGIN', 'END'):
            yield prop


def write_events_to_csv(output_file, calendar, property_names):
    writer = CSVWriter(output_file)
    writer.writerow(property_names)
    for event in get_events(calendar):
        props = []
        for property_name in property_names:
            property_value = get_property_value(event, property_name)
            props.append(property_value)
        writer.writerow(props)


def get_property_value(event, property_name):
    prop = None
    if property_name in event:
        property_value = event[property_name]
        if hasattr(property_value, 'to_ical'):
            prop = to_ical_str(property_value)
        elif isinstance(property_value, list):
            prop = ','.join([to_ical_str(item) for item in property_value])
        else:
            raise Exception('invalid property value')

    return prop


def to_ical_str(value):
    return value.to_ical().decode('UTF-8')


def to_ics(output_file, input_file):
    reader = DictReader(input_file)
    calendar = Calendar()
    calendar.add('VERSION', '2.0')
    for row in reader:
        event = create_event(row)
        calendar.add_component(event)
    output_file.write(convert_to_unix_line_endings(to_ical_str(calendar)))


def create_event(properties):
    event = Event()
    for name, value in properties.items():
        check_csv(value)
        if value != '':
            # This is a hack to make EXDATE work; it must be converted back
            # into a list
            if name == 'EXDATE':
                event[name] = str_to_exdate_list(value)
            # More hacks, this time for RRULE. We need a type system.
            elif name == 'RRULE':
                event[name] = create_recurrence_rule(value)
            # Default type is assumed to be TEXT, which *should* work well with
            # most property types.
            else:
                event[name] = unescape_text(value)
    return event


def check_csv(value):
    """Exit if input is not an instance of ``str``

    If value is not an instance of ``str``, the input was not valid CSV.
    """

    if not isinstance(value, str):
        print('input is not valid CSV', file=sys.stderr)
        sys.exit(1)


def str_to_exdate_list(value):
    """This is a hack to create valid time date ranges"""

    # This would create something like ``EXDATE;VALUE=DATE:yyyymmdd``.
    # It might be what we need, or not. Currently, the other alternative below
    # serves us better, so this is not used.
    # exdate_list = [vDate(item) for item in vDDDLists.from_ical(value)]
    exdate_list = [vDDDTypes(item).to_ical() for item in
                   vDDDLists.from_ical(value)]
    return exdate_list


def create_recurrence_rule(value):
    # The icalendar library is seriously broken, why would I create values like
    # this?!
    return vRecur(vRecur.from_ical(value))


def unescape_text(value):
    value = value.replace('\\\\', '\\')
    value = value.replace('\\n', '\n')
    value = value.replace('\\;', ';')
    value = value.replace('\\,', ',')
    return value


def convert_to_unix_line_endings(data):
    return data.replace('\r', '')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys

from csv import DictReader, writer as CSVWriter
from icalendar import Calendar, Event


def main():
    if len(sys.argv) < 2:
        usage()

    operation = sys.argv[1]

    if sys.argv[1] == '-tocsv':
        to_csv(sys.stdout, sys.stdin)
    elif operation == '-toics':
        to_ics(sys.stdout, sys.stdin)


def usage():
    print("usage:\tcsvcal -tocsv\n\tcsvcal -toics", file=sys.stderr)
    sys.exit(1)


def to_csv(output_file, input_file):
    calendar = Calendar.from_ical(input_file.read())
    property_names = create_properties_map(calendar).keys()
    write_events_to_csv(output_file, calendar, property_names)


def create_properties_map(calendar):
    properties = {}
    for component in calendar.walk():
        if component.name == 'VEVENT':
            for prop in component.property_items(recursive=False):
                property_name = prop[0]
                if property_name == 'BEGIN' or property_name == 'END':
                    continue
                if property_name in properties:
                    properties[property_name] += 1
                else:
                    properties[property_name] = 1
    return properties


def write_events_to_csv(output_file, calendar, property_names):
    writer = CSVWriter(output_file)
    writer.writerow(property_names)
    for component in calendar.walk():
        if component.name == 'VEVENT':
            props = []
            for property_name in property_names:
                prop = None
                if property_name in component:
                    obj = component[property_name]
                    if hasattr(obj, 'to_ical'):
                        prop = obj.to_ical().decode('UTF-8')
                    else:
                        prop = obj
                props.append(prop)
            writer.writerow(props)


def to_ics(output_file, input_file):
    reader = DictReader(input_file)
    calendar = Calendar()
    calendar.add('VERSION', '2.0')
    for row in reader:
        event = Event()
        for name, value in row.items():
            event[name] = value
        calendar.add_component(event)
    output_file.write(calendar.to_ical().replace(b'\r', b'').decode('UTF-8'))


if __name__ == '__main__':
    main()

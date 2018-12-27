#!/usr/bin/env python3

import sys

from csv import DictReader, writer as CSVWriter
from icalendar import Calendar, Event, vDDDTypes


def main():
    if len(sys.argv) < 2:
        usage()

    operation = sys.argv[1]

    if sys.argv[1] == '-tocsv':
        to_csv()
    elif operation == '-toics':
        to_ics()


def usage():
    print("usage:\tcsvcal -tocsv\n\tcsvcal -toics", file=sys.stderr)
    sys.exit(1)


def to_csv():
    calendar = Calendar.from_ical(sys.stdin.read())
    property_names = create_properties_map(calendar).keys()
    write_events_to_csv(calendar, property_names)


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


def write_events_to_csv(calendar, property_names):
    writer = CSVWriter(sys.stdout)
    writer.writerow(property_names)
    for component in calendar.walk():
        if component.name == 'VEVENT':
            props = []
            for property_name in property_names:
                prop = None
                if property_name in component:
                    prop = component[property_name].to_ical().decode('UTF-8')
                props.append(prop)
            writer.writerow(props)


def to_ics():
    reader = DictReader(sys.stdin)
    calendar = Calendar()
    calendar.add('VERSION', '2.0')
    for row in reader:
        event = Event()
        for name, value in row.items():
            event[name] = value
        calendar.add_component(event)
    print(calendar.to_ical().replace(b'\r', b'').decode('UTF-8'))


if __name__ == '__main__':
    main()

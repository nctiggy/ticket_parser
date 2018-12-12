#!/usr/bin/env python3

import json
import csv
import sys

file = sys.argv[1]
out_file = sys.argv[2]

data = []
with open(file) as f:
    for row in csv.DictReader(f):
        data.append(row)

tickets = json.loads(json.dumps(data))
final_json = {'tickets': []}

for ticket in tickets:
    final_ticket = {}
    # Pull out the description field
    # Remove --- and convert \n to a comma
    malformed_description = ticket["Description"].replace("---", "").strip()
    description = malformed_description.replace("\n", ",").strip()
    # Turn description into an array
    items = description.split(",")
    # Parse through each item in description and format it to proper json
    for item in items:
        element = item.split(":")
        if len(element) == 2:
            key = element[0].lower().strip()
            if (
                "echo" in key or
                "h" == key or
                "o" == key or
                "t" == key or
                "http" == key or
                "( e" == key
            ):
                print(f'ignoring: {item}')
                continue
            early_value = element[1].replace("'", "")
            value = early_value.strip(" ").lower()
            # Add the well formed JSON into the final p
            final_ticket.update({key: value})

    # Delete description from the JSON object
    ticket.pop('Description', None)
    # Add original ticket minus description to the new json object
    final_ticket.update(ticket)
    final_json['tickets'].append(final_ticket)

# Store records for later use
records = []

# Keep track of headers in a set
headers = set([])

for line in final_json['tickets']:
    # line = line.strip()

    # Parse each line as JSON
    # parsedJson = json.loads(line)

    records.append(line)

    # Make sure all found headers are kept in the headers set
    for header in line.keys():
        headers.add(header)

# You only know what headers were there once you have read all the JSON once.

# Now we have all the information we need, like what all possible headers are.

outfile = open(out_file, 'w')

# write headers to the file in order
outfile.write(",".join(sorted(headers)) + '\n')

for record in records:
    # write each record based on available fields
    curLine = []
    for header in sorted(headers):
        if header in record:
            curLine.append(record[header])
        else:
            curLine.append('')
    outfile.write(",".join(curLine) + '\n')

outfile.close()

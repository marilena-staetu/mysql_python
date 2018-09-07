import os
import sys


class Select:
    def __init__(self, what_to_select, database, table):
        table_location = "databases/%s/%s.csv" % (database, table)

        if not os.path.isfile(table_location):
            print("ERROR 1146 (42S02): Table '%s.%s' doesn't exist" % (database, table))

        # print("DEBUG: table_location %s" % table_location)

        table_handle = open(table_location, 'r')
        table_header = table_handle.readline()
        column_names = [x.rstrip().replace('"', '') for x in table_header.split(',')]
        if what_to_select not in column_names:
            print("ERROR 1054 (42S22): Unknown column '%s' in 'field list'" % what_to_select)
        # print("Debug: Column names %s"% column_names)
        column_positions = {}
        column_position = 0
        for column_name in column_names:
            column_positions[column_name] = column_position
            column_position += 1
        # print("DEBUG: column positions= %s" %column_positions)
        requested_position = column_positions[what_to_select]
        print("+-------+")
        print("| %s |" % what_to_select)
        print("+-------+")
        for line in table_handle:
            values = [x.rstrip().replace('"', '') for x in line.split(',')]
            print("| %s |" % values[requested_position])

        print('+-------+')


selected_database = None

while True:

    query = input()

    query_parts = query.split()

    action = query_parts[0]

    if action == 'select':

        if selected_database is None:
            print('ERROR 1046 (3D000): No database selected')
        what = query_parts[1]
        # print("Debug: what to select %s"% what_to_select)
        from_keyword = query_parts[2]
        requested_table = query_parts[3]
        select_object = Select(what, selected_database, requested_table)

    if action == 'use':
        database_to_select = query_parts[1]

        if not os.path.isdir("databases/%s" % database_to_select):
            print("ERROR 1049 (42000): Unknown database '%s'" % database_to_select)
        selected_database = database_to_select

    if action == 'exit':
        print('bye')
        sys.exit(0)

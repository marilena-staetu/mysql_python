import os
import sys
from operation import Select


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

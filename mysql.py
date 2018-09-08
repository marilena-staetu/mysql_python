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
        select_object = Select(query, selected_database)

    if action == 'use':
        database_to_select = query_parts[1]

        if not os.path.isdir("databases/%s" % database_to_select):
            print("ERROR 1049 (42000): Unknown database '%s'" % database_to_select)
        selected_database = database_to_select

    if action == 'exit':
        print('bye')
        sys.exit(0)

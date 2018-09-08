import os
import re


class Select:
    table_location = None
    database = None
    table = None
    column_positions = {}
    column_names = None
    requested_fields = []

    def __init__(self, query, database):

        self.parse_query(query)

        self.database = database
        self.table_location = "databases/%s/%s.csv" % (self.database, self.table)

        if not self.validate_table():
            return

        table_handle = open(self.table_location, 'r')
        table_header = table_handle.readline()
        self.generate_table_structure(table_header)
        if not self.validate_column(self.requested_fields):
            return
        print("+-------+")
        print("| %s |" % self.requested_fields)
        print("+-------+")
        for line in table_handle:
            print("| %s |" % self.get_by_column_name(self.requested_fields, line))
        print('+-------+')

    def validate_table(self):
        if not os.path.isfile(self.table_location):
            print("ERROR 1146 (42S02): Table '%s.%s' doesn't exist" % (self.database, self.table))
            return False
        return True
        # print("DEBUG: table_location %s" % table_location)

    def generate_table_structure(self, header_line):
        self.column_names = [x.rstrip().replace('"', '') for x in header_line.split(',')]
        column_position = 0
        for column_name in self.column_names:
            self.column_positions[column_name] = column_position
            column_position += 1
        # print("DEBUG: column positions= %s" %column_positions)

    def validate_column(self, what_to_select):
        if what_to_select not in self.column_names:
            print("ERROR 1054 (42S22): Unknown column '%s' in 'field list'" % what_to_select)
            return False
        return True
        # print("Debug: Column names %s"% column_names)

    def get_by_column_name(self, what_to_select, line):
        requested_position = self.column_positions[what_to_select]
        values = [x.rstrip().replace('"', '') for x in line.split(',')]
        return values[requested_position]

    def parse_query(self, query: str):

        query_groups = re.search('select (.*) from (.*)', query)

        self.requested_fields = query_groups.group(1)
        self.table = query_groups.group(2)

import os


class Select:
    table_location = None
    database = None
    table = None

    def __init__(self, what_to_select, database, table):
        self.database = database
        self.table = table
        self.table_location = "databases/%s/%s.csv" % (self.database, self.table)

        if not self.validate_table():
            return

        table_handle = open(self.table_location, 'r')
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

    def validate_table(self):
        if not os.path.isfile(self.table_location):
            print("ERROR 1146 (42S02): Table '%s.%s' doesn't exist" % (self.database, self.table))
            return False
        return True
        # print("DEBUG: table_location %s" % table_location)

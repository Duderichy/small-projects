import csv
from array import array
from collections import defaultdict

# def main(f, col=0):
#     return get_file_max(f, col)

def get_file_max(f, col):
    """
    gets the row with the maximum value at column col in file f
    """
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) # skip header row
        return max(csv_reader, key = lambda x: int(x[col]))

def get_file_min(f, col):
    """
    gets the row with the minimum value at column col in file f
    """
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) # skip header row
        return min(csv_reader, key = lambda x: int(x[col]))

def print_lines(f):
    # used for file inspection, not important to main program
    # leaving this in
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file)
        for i, row in enumerate(csv_reader):
            print(i, end = ', ')
            for col in row:
                print(col, end = ', ')
                if i == 5:
                    print()
                    return col
            print(row[0], row[1])
            print()

def make_buckets(f, start_col, len_col) -> array:
    """
    makes an array large enough to hold all keys based on numerical values from
    a file column
    """
    return array('i', [ 0 for _ in range(
        int(get_file_max(f, start_col)[start_col]) +
        int(get_file_max(f, len_col)[len_col])
        + 2)])

def fill_lookup(f, start_col, len_col, lookup=defaultdict(int)):
    """
    fills in the given lookup table, must have __getitem__() implimented
    """
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        print("starting table fill")
        for i, row in enumerate(csv_reader):
            if i % 200000 == 0:
                print("reading in row", i)
            for key in range(int(row[start_col]), int(row[start_col]) + int(row[len_col])):
                lookup[key] += 1
        return lookup

# def do_lookup(lookup):
#     print(lookup[101844980])

def fill_lookup_file(f, f_output, lookup, lookup_col):
    """
    Makes a version of lookup file f at f_output with the lookup values from
    passed lookup variable from file f at column lookup_col. Lookup must have
    __getitem__ implimented.
    """
    with open(f) as lookup_file, open(f_output, 'w') as output_file:
        csv_reader = csv.reader(lookup_file)
        csv_writer = csv.writer(output_file, delimiter=',')
        headers = next(csv_reader)
        csv_writer.writerow(headers)
        for i, row in enumerate(csv_reader):
            lookup_val = int(row[lookup_col])
            csv_writer.writerow(
                [lookup_val ,
                 lookup[int(lookup_val)]])

if __name__ == "__main__":
    # print("main", main("./data/loci.csv"))
    # print("max reads.csv", get_file_max("./data/reads.csv", 1))
    # print("min reads.csv", get_file_min("./data/reads.csv", 1))
    # print("max reads.csv", get_file_max("./data/reads.csv", 0))
    # print("min reads.csv", get_file_min("./data/reads.csv", 0))
    # print("print_lines", print_lines("./data/reads.csv"))
    #foo = int(get_file_max("./data/reads.csv", 0)[0]) - int(get_file_min("./data/reads.csv", 0)[0])

    # lookup = make_buckets("./data/reads.csv", 0, 1)
    # fill_lookup("./data/reads.csv", 0, 1, lookup = lookup)

    lookup = fill_lookup("./data/reads.csv", 0, 1)
    fill_lookup_file('./data/loci.csv', './data/loci_filled.csv', lookup, 0)

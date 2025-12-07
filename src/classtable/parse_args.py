import argparse

def parse_args(args = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help = 'table data csv file', default = '')
    return parser.parse_args(args)
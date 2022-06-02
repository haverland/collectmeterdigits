import argparse
import sys
from collectmeterdigits.collect import collect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('meter', help='the edgeAI meter server name')
    parser.add_argument('--days', type=int, default=3, help='count of days back to read. (default: 3)')

    # print help message if no argument is given
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()

    
    collect(args.meter, args.days)

if __name__ == '__main__':
    main()
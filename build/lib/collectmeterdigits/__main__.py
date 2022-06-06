import argparse
import sys
from collectmeterdigits.collect import collect
from collectmeterdigits.labeling import label


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--collect', default='', help='collect all images. The edgeAI meter server name must be set')
    parser.add_argument('--days', type=int, default=3, help='count of days back to read. (default: 3)')
    parser.add_argument('--labeling', default='', help='labelpath if you want label the images')
    parser.add_argument('--labelstart', type=float, default='0', help='Optional: start value of labeling')
    parser.add_argument('--keepolddata', default=False, action="store_true", help='do not delete downloaded data')
    parser.add_argument('--nodownload', default=False, action="store_true", help='do not download data')

    # print help message if no argument is given
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()

    if (args.labeling==''):
        collect(args.collect, args.days, args.keepolddata, args.nodownload)
    else:
        label(args.labeling, args.labelstart)    

if __name__ == '__main__':
    main()
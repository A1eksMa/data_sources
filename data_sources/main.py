import argparse
import logging

def test():
    print('Test mode')

def main():
    print('Main mode')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument('-t', '--test',
                        dest='test',
                        action='store_true',
                        default=False,
                        help='Test mode')
    args = parser.parse_args()

    test() if args.test main()


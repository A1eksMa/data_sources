import argparse
#from lib.cls_node import Node
#from lib.cls_times import Times
#from lib.cls_excel import ExcelFile
from lib.cls_row import Row


def test():
    print('Test mode')


def main():
    print('Main mode')
    r = Row("test/row")
    print(r.info['keys'])
    #r.upload("test/test_data/upd1.xlsx")
    print(r.get_key('1730873584742642'))#.keys())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=__doc__)

    parser.add_argument('-t', '--test',
                        dest='test',
                        action='store_true',
                        default=False,
                        help='Test mode')

    args = parser.parse_args()

    test() if args.test else main()

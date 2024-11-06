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
    d = r.get_data(r.get_key('1730873584742642'))
    for k1 in d.keys():
        print("Indicator", k1)
        for k2 in d[k1].keys():
            print(k2, " : ", d[k1][k2])
    #r.upload("test/test_data/upd1.xlsx")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=__doc__)

    parser.add_argument('-t', '--test',
                        dest='test',
                        action='store_true',
                        default=False,
                        help='Test mode')

    args = parser.parse_args()

    test() if args.test else main()

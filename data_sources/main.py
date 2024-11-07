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
    
    #r.upload("test/test_data/upd3.xlsx")

    print(r.keys())
    print("Test start attribute")
    print(r.get_start_dt())
    for k in r.get_start_data():
        print(k)
        print(r.get_start_data()[k])
    print("Test final attribute")
    print(r.get_final_dt())
    for k in r.get_final_data():
        print(k)
        print(r.get_final_data()[k])




if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage=__doc__)

    parser.add_argument('-t', '--test',
                        dest='test',
                        action='store_true',
                        default=False,
                        help='Test mode')

    args = parser.parse_args()

    test() if args.test else main()

class ExcelFile:
    def __init__(self, file_path, sheet=0):
        '''Init Excel object: book and sheet'''

        # Set default attributes
        self.file_path = file_path

        self.file_type = None
        if self.file_path.lower().endswith('.xls'): self.file_type = 'xls'
        if self.file_path.lower().endswith('.xlsx'): self.file_type = 'xlsx'

        self.workbook = None
        self.worksheet = None

        # Set `workbook` and `worksheet` attributes from Excel file
        if self.file_type == 'xls':
            # Try to open an Excel file from `file_path`
            try:
                self.workbook = xlrd.open_workbook(self.file_path)
            except xlrd.XLRDError as e:
                print(f"An error occurred: {e}")

            # Try to open an Excel sheet from `workbook`
            if isinstance(sheet, int):
                try:
                    self.worksheet = self.workbook.sheet_by_index(sheet)
                except xlrd.XLRDError as e:
                    print(f"An error occurred: {e}")
            elif isinstance(sheet, str):
                try:
                    self.worksheet = self.workbook.sheet_by_name(sheet)
                except xlrd.XLRDError as e:
                    print(f"An error occurred: {e}")
            else:
                print('Worksheet type error')


        elif self.file_type == 'xlsx':
            # Try to open an Excel file from `file_path`
            try:
                self.workbook = openpyxl.load_workbook(self.file_path)
            except openpyxl.utils.exceptions.InvalidFileException as e:
                print(f"An error occurred: {e}")

            # Try to open an Excel sheet from `workbook`
            if isinstance(sheet, int):
                try:
                    self.worksheet = self.workbook.worksheets[sheet]
                except openpyxl.utils.exceptions.InvalidFileException as e:
                    print(f"An error occurred: {e}")
            elif isinstance(sheet, str):
                try:
                    self.worksheet = self.workbook[sheet]
                except openpyxl.utils.exceptions.InvalidFileException as e:
                    print(f"An error occurred: {e}")
            else:
                print('Worksheet type error')


        else:
            print('Unsupported file format')


    def get_rows(self):
        '''Returns list of rows'''
        res = []

        if self.file_type == 'xls':
            for row in range(self.worksheet.nrows):
                res.append(self.worksheet.row_values(row))
        elif self.file_type == 'xlsx':
            for row in self.worksheet.iter_rows(values_only=True):
                ro = []
                for cell in row:
                    ro.append(cell)
                res.append(ro)
        else:
            print('Unsupported file format')

        return res if res else False



    def get_columns(self):
        '''Returns list of columns'''
        res = []

        if self.file_type == 'xls':
            for col in range(self.worksheet.ncols):
                res.append(self.worksheet.col_values(col))
        elif self.file_type == 'xlsx':
            for col in self.worksheet.iter_cols():
                column = []
                for cell in col:
                    column.append(cell.value)
                res.append(column)
        else:
            print('Unsupported file format')

        return res if res else False


    def get_dictionary(self):
        dictionary = {}
        for i in self.get_columns():
            dictionary.update({i[0]: i[1:]})
        return dictionary

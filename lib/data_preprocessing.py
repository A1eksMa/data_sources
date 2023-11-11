def snake(df):
# Функция, которая выполняет предобработку заголовков датафрейма и переводит заголовки в "змеиный стиль": преобразовывает русские буквы в латинские
# и устраняет из названий заголовков спецсимволы
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace("(", "")
    df.columns = df.columns.str.replace(")", "")
    df.columns = df.columns.str.replace("/", "-")
    df.columns = df.columns.str.replace("\\", "-")
    df.columns = df.columns.str.replace("№", "nomer")
    df.columns = df.columns.str.replace("%", "procent")
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace("а", "a")
    df.columns = df.columns.str.replace("б", "b")
    df.columns = df.columns.str.replace("в", "v")
    df.columns = df.columns.str.replace("г", "g")
    df.columns = df.columns.str.replace("д", "d")
    df.columns = df.columns.str.replace("е", "ye")
    df.columns = df.columns.str.replace("ё", "yo")
    df.columns = df.columns.str.replace("ж", "j")
    df.columns = df.columns.str.replace("з", "z")
    df.columns = df.columns.str.replace("и", "i")
    df.columns = df.columns.str.replace("й", "y")
    df.columns = df.columns.str.replace("к", "k")
    df.columns = df.columns.str.replace("л", "l")
    df.columns = df.columns.str.replace("м", "m")
    df.columns = df.columns.str.replace("н", "n")
    df.columns = df.columns.str.replace("о", "o")
    df.columns = df.columns.str.replace("п", "p")
    df.columns = df.columns.str.replace("р", "r")
    df.columns = df.columns.str.replace("с", "s")
    df.columns = df.columns.str.replace("т", "t")
    df.columns = df.columns.str.replace("у", "u")
    df.columns = df.columns.str.replace("ф", "f")
    df.columns = df.columns.str.replace("х", "h")
    df.columns = df.columns.str.replace("ц", "c")
    df.columns = df.columns.str.replace("ч", "ch")
    df.columns = df.columns.str.replace("ш", "sh")
    df.columns = df.columns.str.replace("щ", "sh")
    df.columns = df.columns.str.replace("ь", "")
    df.columns = df.columns.str.replace("ъ", "")
    df.columns = df.columns.str.replace("ы", "yi")
    df.columns = df.columns.str.replace("э", "e")
    df.columns = df.columns.str.replace("ю", "yu")
    df.columns = df.columns.str.replace("я", "ya")
    return

def listing(lst, tp=False):
    # Функция построчного вывода сложных объектов (массивов, списков и тп)
    print('\n############### INFO ###############')
    print(series.info(), '\n')

    pos = len(series)
    skip = len(series.loc[series.isna()])
    print('Количество позиций:', pos)
    print('Количество пропусков:', skip, '(', round(100*skip/pos, 2), '%)')

    dubl = len(series.duplicated())
    unic = len(series.drop_duplicates())

    series = series.loc[~series.isna()]
    tp = series.dtype
    print('Тип данных:', tp)
    print('\nКоличество уникальных:', unic, '(', round(100*unic/pos, 2), '%)')

    if unic < 10:
        print(series.value_counts().reset_index())
    else:
        print(series.value_counts().reset_index()[:5])
        print('    ....................')
        print(series.value_counts().reset_index()[-5:])
    # print('Количество дубликатов:', dubl, '(', round(100*dubl/pos, 2), '%)')
    if tp != 'object':
        print('\n', series.describe())

    print('####################################\n')
    return

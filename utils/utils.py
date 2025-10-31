import datetime


def date_to_format(date: str, format_: str, date_elements: int) -> str | bool:  # ToDo: написать тест
    """
    Преобразует дату в указанный формат.
    :param date: дата.
    :param format_: формат (как в datetime).
    :param date_elements: число элементов (день, месяц, год) в формате. Например, в формате dd.mm.yy 3 элемента, в
    формате dd.mm - 2.
    :return: Дата, если удалось корректно преобразовать. False, если не удалось
    """
    splitter = ''
    last_char = ''
    for char in date:  # Нахождение разделителя
        if not char.isdigit() and last_char.isdigit():
            splitter = char
        if not char.isdigit() and not last_char.isdigit():
            splitter = f'{splitter}{char}'

        last_char = char

    spl_date = date.split(splitter)
    if len(spl_date) == date_elements and all([all([char.isdigit() for char in element]) for element in spl_date]):  # Проверка соответствия числа элементов и того, что содержимое элементов - цифры
        spl_date = list(map(int, spl_date))
        try:
            return datetime.date(*spl_date[::-1]).strftime(format_)  # spl_date нужно развернуть, т.к. date принимает аргументы в порядке year, month, day
        except ValueError:
            return False
    else:
        return False


if __name__ == '__main__':
    pass


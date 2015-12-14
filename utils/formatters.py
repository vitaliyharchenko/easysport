# coding=utf-8

def beautiful_format(value, cases):
    """
    :param value: Число для форматирования
    :param cases: Список из списков из трех строк,
    где строки различаются по падежам:
    родительный множественного числа, именительный единственного числа, родительный единственного числа.
    если в cases больше одного списка, то во всех последующих списках четвертым значением должен быть
    делитель (см. duration_format)
    :return:
    """
    assert isinstance(cases, (list, tuple))
    postfix = u''
    value = int(value)

    for n, case in enumerate(cases):
        if n > 0:
            if len(case) == 3:
                break
            if len(case) > 3:
                if value < case[3]:
                    break
                else:
                    value = int(round(value / case[3]))
        prefix = int(str(value)[-1])
        if prefix == 0 or 5 <= prefix <= 9 or 10 <= value <= 19:
            postfix = case[0]
        elif prefix == 1:
            postfix = case[1]
        elif 2 <= prefix <= 4:
            postfix = case[2]
    return u'{} {}'.format(value, postfix)


def age_format(age):
    return beautiful_format(age, [(u'лет', u'год', u'года')])


def duration_format(duration):
    return beautiful_format(duration, [(u'минут', u'минута', u'минуты'),
                                       (u'часов', u'час', u'часа', 60)])  # делим duration на 60 получаем часы
    # (u'дней', u'день', u'дня', 24)])  # делим duration на 24 получаем дни
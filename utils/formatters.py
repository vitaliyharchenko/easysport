# coding=utf-8


# duration format
def plural_rus_variant(x):
    lasttwodigits = x % 100
    tens = lasttwodigits / 10
    if tens == 1:
        return 2
    ones = lasttwodigits % 10
    if ones == 1:
        return 0
    if 2 <= ones <= 4:
        return 1
    return 2


def show_hours(hours):
    suffix = ["час", "часа", "часов"][plural_rus_variant(hours)]
    return "{0} {1}".format(hours, suffix)


def show_minutes(minutes):
    suffix = ["минута", "минуты", "минут"][plural_rus_variant(minutes)]
    return "{0} {1}".format(minutes, suffix)


def show_years(age):
    years = age
    suffix = ["год", "года", "лет"][plural_rus_variant(years)]
    return "{0} {1}".format(years, suffix)
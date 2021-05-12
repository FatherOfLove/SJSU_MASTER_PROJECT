import matplotlib.pyplot as plt
from django import template
register = template.Library()


@register.filter
def list_to_str(s):
    return s[0]


@register.filter
def convert_set_to_str(s):
    return s[4]


@register.filter
def convert_tuple1(tuple):
    return tuple[0]


@register.filter
def convert_tuple2(tuple):
    return tuple[1]


@register.filter
def convert_tuple3(tuple):
    return tuple[2]


@register.filter
def convert_tuple4(tuple):
    return tuple[3]


@register.filter
def get_signal_graph(data):
    plt.figure(figsize=(12, 4))
    a = plt.plot(data)
    #a = plt.show()
    return a

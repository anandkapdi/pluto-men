import datetime
import random
import string
import urllib
import urllib2

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from functools import wraps

"""
This file contains functions which can be mostly used outside of given project
They are orthodox
"""


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def msg91(mobiles, msg,
          authkey="184810Akry1rYp5a1459aa",
          sender="GILOOL", route="transactional"):
    # authkey = "184810Akry1rYp5a1459aa"
    # Prepare you post parameters
    values = {
        'authkey': authkey,
        'mobiles': mobiles,
        'message': msg,
        'sender': sender,
        'route': route}

    url = "http://api.msg91.com/api/sendhttp.php"  # API URL

    postdata = urllib.urlencode(values)  # URL encoding the data here.

    req = urllib2.Request(url, postdata)

    response = urllib2.urlopen(req)

    output = response.read()  # Get Response

    print output  # Print Response


def string_to_date(date_string):
    """
    date_string(string): string of date in yyyy-mm- formate

    Returns: date string coverted to datetime.datetime
    """
    try:
        year, month, day = [int(i) for i in date_string.split('-')]
        date = datetime.datetime(year=year, month=month, day=day)
    except (ValueError, AttributeError):
        date = None
    return date


def form_get_dict(form_type, form_output="string"):
    """
    This should be used to get html form data if you don't have any
    strong reason to do otherwise, as this handles float and int conversion and
    provide user_id from session

    form_type(string): string which is a valid key in var_dict
    e.g. 'user', 'login'

    Returns: a dictionary where a form field name from html form and
    user_id from session is mapped to its value

    Example:
    >>> form_get_dict('user')
    {name: request.form.get('mobile_num'), address: request.form.get('name')}
    """
    form_get_dict = {}
    form_input_list = var_list(form_type)
    if form_output == "string":
        for i in form_input_list:
            if request.form.get(i):
                form_get_dict[i] = form_convert(i)(request.form.get(i))
            else:
                if i.split('_')[-1] == 'float':
                    form_get_dict[i] = 0
                else:
                    form_get_dict[i] = None
    elif form_output == "list":
        for i in form_input_list:
            form_get_dict[i] = [
                form_convert(i)(j) for j in request.form.getlist(i)]
    else:
        raise ValueError("bad input")
    form_get_dict['user_id'] = session.get('user_id')
    return form_get_dict


def identity(x):
    return x


def form_convert(input_name):
    if input_name.split('_')[-1] == 'float':
        return float
    elif input_name.split('_')[-1] == 'date':
        return string_to_date
    elif input_name.split('_')[-1] == 'id':
        return int
    else:
        return identity


def var_list(model_type=None):
    var_dict = {
        'account': ['name', 'address', 'mobile_num', 'account_type'],
        'edit_password': ['confirm_password', 'password'],
        'edit_profile': ['name', 'address'],
        'login': ['mobile_num', 'password'],
        'order': ['price_float', 'product_id', 'product_description'],
        'submit_order': ['order_id', 'price_float', 'quntity_float'],
        'user': ['address', 'mobile_num', 'name'],
        'business': ['city', 'username', 'name'],
        'product': ['product_description', 'price_float', 'quntity_float'],
        'products_csv': ['products_csv'],
        'save_bill': ['customer_id'],
        'send_bill': ['confirm_mobile_num', 'description', 'mobile_num']
    }
    if not model_type:
        return var_dict
    return var_dict[model_type]


def para_dict(var_list):
    """
    var_list(list): list of strings

    Returns: a dictionary where string from var_list are as keys mapped
    to its evaluated value

    Example:
    >>> a, b, c = 10, 20, 30
    >>> para_dict(['a', 'b', 'c']) returns
    {a: 10, b: 20, c: 30}
    """
    para_dict = {}
    for i in var_list:
        para_dict[i] = eval(i)
    return para_dict


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def current_ist():
    """
    returns indian standard time now
    """
    return datetime.datetime.now() + datetime.timedelta(hours=5.5)


def time_change(change_days=0, change_months=0, change_hours=0):
    """
    returns: changes current time by given hours
    """
    return current_ist() + datetime.timedelta(
        days=change_days,
        hours=change_hours)


def user_id():
    return session.get('user_id')

import decimal
from tkinter import *

root = Tk()


def label_create(txt, r):
    lbl = Label(root, text=txt)
    lbl.grid(row=r, column=0, padx=5, pady=5)
    return lbl


def result_label_create(w, r, c):
    lbl = Label(root, width=w)
    lbl.grid(row=r, column=c, columnspan=3, padx=5, pady=5)
    return lbl


def entry_create(r):
    entry = Entry(root, width=5, borderwidth=5)
    entry.grid(row=r, column=1, columnspan=3, padx=5, pady=5)
    return entry


def empty_label_create(r):
    lbl = Label(root)
    lbl.grid(row=r, column=1, columnspan=3, padx=5, pady=5)
    return lbl


def dropdown_create(r):
    s_var = StringVar()
    s_var.set('f')
    dropdown = OptionMenu(root, s_var, *values.keys())
    dropdown.grid(row=r, column=1, columnspan=3)
    return s_var


def radioButtons_create(txt, r, c):
    radio = Radiobutton(root, text=txt)
    radio.grid(row=r, column=c)
    return radio


def label_no_span():
    lbl = Label(root, width=5)
    lbl.grid(row=7, column=0)
    return lbl


def button_create(txt, cmd, func):
    btn = Button(root, text=txt, command=cmd)
    btn.grid(row=7, column=1, columnspan=3, padx=5, pady=5)
    return btn


labels = [label_create('1st Value', 0),
          label_create('1st Multiplier', 1),
          label_create('Tolerance', 2),
          label_create('2nd Value', 3),
          label_create('2nd Multiplier', 4),
          label_create('Result', 5),
          label_create('Range', 6),
          result_label_create(5, 5, 1),
          result_label_create(10, 6, 1),
          label_no_span()]
[label_first_val, label_first_farad,
 label_tolerance, label_second_val,
 label_second_farad, label_result_label,
 label_range, label_res, label_low_high,
 label_error] = labels

empty_labels = [empty_label_create(1),
                empty_label_create(4),
                entry_create(0),
                entry_create(3)]
[first_farad, second_farad,
 first_val, second_val] = empty_labels

tolerance_buttons = [radioButtons_create('5', 2, 1),
                     radioButtons_create('10', 2, 2),
                     radioButtons_create('20', 2, 3)]
[tolerance_five_button,
 tolerance_ten_button,
 tolerance_twenty_button] = tolerance_buttons

values = {
    'f': 1,
    'mf': 1000,
    'uf': 1000000,
    'nf': 1000000000,
    'pf': 1000000000000,
}

dropdowns = [dropdown_create(1),
             dropdown_create(4)]
[first_click_dropdown,
 second_click_dropdown] = dropdowns

v1 = StringVar(root, '5')
radio_buttons = {
    tolerance_five_button: 5,
    tolerance_ten_button: 10,
    tolerance_twenty_button: 20,
}
for k, v in radio_buttons.items():
    k.config(variable=v1, value=v)


def check_input_match(first, second):
    for key, val in values.items():
        if first_click_dropdown.get() == key:
            first = first / val * val
        elif second_click_dropdown.get() == key:
            second = second / val
    condition(first, second)
    label_error.config(text='')


def search_key(first, second):
    if first_click_dropdown.get() == second_click_dropdown.get():
        check_input_match(first, second)
    else:
        check_input_match(first, second)


def condition(first_num, second_num):
    percentage = 0
    for radioKey, radioValue in radio_buttons.items():
        if radioKey['text'] == v1.get():
            percentage = first_num * radioValue / 100

    low = first_num - percentage
    high = first_num + percentage
    label_low_high.config(text=f'{low:.2f}-{high:.2f}')
    label_range.config(text=f'Range: ({first_click_dropdown.get()})')

    if second_num > high or second_num < low or first_click_dropdown.get() != second_click_dropdown.get():
        return label_res.config(text='BAD', fg='red')
    else:
        return label_res.config(text='GOOD', fg='dark green')


def Capacitor():
    try:
        if first_val.get().__contains__('.'):
            search_key(is_decimal(first_val, label_first_val), is_float(second_val, label_second_val))
        elif second_val.get().__contains__('.'):
            search_key(is_decimal(second_val, label_second_val), is_float(first_val, label_first_val))
        elif first_val.get().__contains__('.') and second_val.get().__contains__('.'):
            search_key(is_decimal(first_val, label_first_val), is_decimal(second_val, label_second_val))
        else:
            search_key(is_float(first_val, label_first_val), is_float(second_val, label_second_val))
    except:
        label_error.config(text='ERROR*', fg='red')
        error_list()


def error_list():
    is_empty(first_val, label_first_val)
    is_empty(second_val, label_second_val)
    contains_alpha(first_val, label_first_val)
    contains_alpha(second_val, label_second_val)
    contain_number(first_val, label_first_val)
    contain_number(second_val, label_second_val)


def calculate():
    Capacitor()


def is_decimal(entry, entry_label):
    new_label = Label(root)
    new_label.config(text=entry_label['text'], fg='black')
    new_label.grid(entry_label.grid_info())
    as_decimal = decimal.Decimal(entry.get())
    return float(as_decimal)


def is_float(entry, entry_label):
    new_label = Label(root)
    new_label.config(text=entry_label['text'], fg='black')
    new_label.grid(entry_label.grid_info())
    as_float = float(entry.get())
    return float(as_float)


def is_empty(entry, entry_label):
    new_label = Label(root)
    if len(entry.get()) == 0 or entry.get() == ' ':
        new_label.config(text=entry_label['text'] + '*', fg='red')
        new_label.grid(entry_label.grid_info())
    return new_label


def contains_alpha(entry, entry_label):
    new_label = Label(root)
    for char in entry.get():
        if char.isalpha() and not char.isnumeric():
            new_label.config(text=entry_label['text'] + '*', fg='red')
            new_label.grid(entry_label.grid_info())
            return new_label


def contain_number(entry, entry_label):
    new_label = Label(root)
    if entry.get().isnumeric():
        new_label.config(text=entry_label['text'], fg='black')
        new_label.grid(entry_label.grid_info())
    return new_label


calc_button = button_create('Calculate', Capacitor, calculate)

root.mainloop()

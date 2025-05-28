from tkinter import *


class Labels:
    def __init__(self, parent):
        self.parent = parent
        self.label_texts = [
            "1st Value",
            "1st Multiplier",
            "Tolerance",
            "2nd Value",
            "2nd Multiplier",
            "Result",
            "Range"
        ]
        self.create_static_labels()

        self.result_label = Label(self.parent, text="", width=5)
        self.range_label = Label(self.parent, text="", width=10)

    def place_widget(self, _dict: dict):
        for k, v in _dict.items():
            getattr(self, k).grid(**v)

    def create_static_labels(self):
        for i, text in enumerate(self.label_texts):
            Label(self.parent, text=text).grid(row=i, column=0, padx=5, pady=5)


class RadioButtons:
    def __init__(self, parent):
        self.parent = parent
        self.radio_s_var = StringVar(self.parent, "5")

        self.radio_values = {
            "5": 5,
            "10": 10,
            "20": 20,
        }

        self.radio_buttons = {
            "5": Radiobutton(self.parent, text="5", variable=self.radio_s_var, value=5),
            "10": Radiobutton(self.parent, text="10", variable=self.radio_s_var, value=10),
            "20": Radiobutton(self.parent, text="20", variable=self.radio_s_var, value=20),
        }

    def place_widget(self, _dict: dict):
        for key, value in _dict.items():
            self.radio_buttons[key].grid(**value)

    @property
    def radio_value(self):
        return self.radio_values[self.radio_s_var.get()]


class Entries:
    def __init__(self, parent):
        self.parent = parent
        self.first_entry = Entry(self.parent, width=5, borderwidth=5)
        self.second_entry = Entry(self.parent, width=5, borderwidth=5)

    def place_widget(self, _dict: dict):
        for k, v in _dict.items():
            getattr(self, k).grid(**v)

    @property
    def first_value(self):
        return self.check_char(self.first_entry.get())

    @property
    def second_value(self):
        return self.check_char(self.second_entry.get())

    @staticmethod
    def check_char(_entry):
        if _entry.isalpha() and not _entry.isnumeric():
            return "ERROR -- Non-Integer type in input field"
        else:
            return float(_entry)


class Dropdowns:
    def __init__(self, parent):
        self.parent = parent
        self.values = {
            'f': 1,
            'mf': 1000,
            'uf': 1000000,
            'nf': 1000000000,
            'pf': 1000000000000,
        }

        self.first_dropdown_value = StringVar()
        self.first_dropdown_value.set('f')
        self.second_dropdown_value = StringVar()
        self.second_dropdown_value.set('f')

        self.first_dropdown = OptionMenu(self.parent, self.first_dropdown_value, *self.values.keys())

        self.second_dropdown = OptionMenu(self.parent, self.second_dropdown_value, *self.values.keys())

    def place_widget(self, _dict: dict):
        for k, v in _dict.items():
            getattr(self, k).grid(**v)

    @property
    def first_value(self):
        return self.values[self.first_dropdown_value.get()]

    @property
    def second_value(self):
        return self.values[self.second_dropdown_value.get()]


class Controls:
    def __init__(self, parent):
        self.parent = parent
        self.calculate = Button(self.parent, text="calculate")
        self.reset = Button(self.parent, text="reset")

    def control_unpack(self, _dict: dict):
        for key, value in _dict.items():
            getattr(self, key).grid(**value[0])
            getattr(self, key).config(command=value[1])


class App(Tk):
    def __init__(self):
        super().__init__()
        label_dict = {
            "result_label": {"row": 5, "column": 1, "columnspan": 3, "padx": 5, "pady": 5},
            "range_label": {"row": 6, "column": 1, "columnspan": 3, "padx": 5, "pady": 5}
        }
        entry_dict = {
            "first_entry": {"row": 0, "column": 1, "columnspan": 3, "padx": 5, "pady": 5},
            "second_entry": {"row": 3, "column": 1, "columnspan": 3, "padx": 5, "pady": 5}
        }
        dropdown_dict = {
            "first_dropdown": {"row": 1, "column": 1, "columnspan": 3},
            "second_dropdown": {"row": 4, "column": 1, "columnspan": 3},
        }
        radio_dict = {
            "5": {"row": 2, "column": 1},
            "10": {"row": 2, "column": 2},
            "20": {"row": 2, "column": 3},
        }
        control_dict = {
            "calculate": ({"row": 7, "column": 1, "columnspan": 3, "padx": 5, "pady": 5}, self.result),
            "reset": ({"row": 7, "column": 0, "columnspan": 1, "padx": 5, "pady": 5}, self.reset)
        }

        self.radio_buttons = RadioButtons(self)
        self.labels = Labels(self)
        self.entries = Entries(self)
        self.dropdowns = Dropdowns(self)
        self.controls = Controls(self)

        self.labels.place_widget(label_dict)
        self.entries.place_widget(entry_dict)
        self.dropdowns.place_widget(dropdown_dict)
        self.controls.control_unpack(control_dict)
        self.radio_buttons.place_widget(radio_dict)

    @property
    def lower_range(self):
        return self.entries.first_value * (1 - self.radio_buttons.radio_value / 100)

    @property
    def higher_range(self):
        return self.entries.first_value * (1 + self.radio_buttons.radio_value / 100)

    @property
    def normalised_second_value(self):
        dropdown1_check = self.dropdowns.first_value
        dropdown2_check = self.dropdowns.second_value

        if dropdown1_check == dropdown2_check:
            return self.entries.second_value
        if dropdown1_check < dropdown2_check:
            return self.entries.second_value / dropdown2_check
        if dropdown1_check > dropdown2_check:
            return self.entries.second_value * dropdown2_check

    def result(self):
        if self.lower_range < self.normalised_second_value < self.higher_range:
            self.labels.result_label.config(text="GOOD", fg="dark green")
        else:
            self.labels.result_label.config(text="BAD", fg="red")
        self.labels.range_label.config(text=f"{self.lower_range:.2f} ~ {self.higher_range:.2f}")

    def reset(self):
        self.entries.first_entry.delete(0, END)
        self.entries.second_entry.delete(0, END)
        self.dropdowns.first_dropdown_value.set("f")
        self.dropdowns.second_dropdown_value.set("f")
        self.labels.result_label.config(text="")
        self.labels.range_label.config(text="")
        self.radio_buttons.radio_s_var.set("5")


if __name__ == '__main__':
    app = App()
    app.mainloop()

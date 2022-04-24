import tkinter as tk
from tkinter import ttk

from converters import *

converter_map = {
    "km to miles": km_to_mile,
    "miles to km": mile_to_km,
    "kg to pounds": kg_to_pound,
    "pounds to kg": pound_to_kg,
}

windows = tk.Tk()
windows.title("Simple Converter")
# windows.minsize(width=500, height=300)
windows.config(padx=20, pady=20)

# button event
def button_pressed():
    convert_units = unit_var.get()
    input_value = user_input.get()
    if input_value.isnumeric():
        output_str = converter_map[convert_units](float(input_value))
    else:
        output_str = "Please enter a whole number!"
    text_output.config(text=output_str)


# Entry
user_input = tk.Entry()
# user_input.insert(tk.END, string="Enter value")
user_input.grid(column=0, row=0)

# Unit selector
unit_var = tk.StringVar()
unit_selector = ttk.Combobox(
    textvariable=unit_var, values=list(converter_map.keys()), state="readonly"
)
unit_selector.current(0)
unit_selector.grid(column=1, row=0)

# Button
convert_button = tk.Button(text="Convert", command=button_pressed)
convert_button.grid(column=2, row=0)

# Output
text_output = tk.Label(text="Output")
text_output.grid(column=0, row=1)
text_output.config(pady=5)

windows.mainloop()

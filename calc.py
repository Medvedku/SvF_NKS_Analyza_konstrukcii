import tkinter as tk

# Colours
WHITE = "#FFFFFF"
OFF_WHITE = "#F8FAFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOUR = "#25265E"
LIGHT_BLUE = "#CCEDFF"

# Fonts
SMALL_FONT_STYLE = ("Arial", 16)
LARGE_FONT_STYLE = ("Arial", 40, "bold")
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0,0)
        self.window.title("Swag")

        self.total_expression = "0"
        self.current_expression = "0"

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.total_label, self.current_label = self.create_display_labels()

        self.digits = { 7: (1, 1), 8: (1, 2), 9: (1, 3),
                        4: (2, 1), 5: (2, 2), 6: (2, 3),
                        1: (3, 1), 2: (3, 2), 3: (3, 3),
                        0: (4, 2), ".": (4, 1) }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.create_digits_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

        self.buttons_frame.rowconfigure(0, weight=1)
        for i in range(1,5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()

    def create_display_labels(self):
        total_label = tk.Label( self.display_frame,
                                text = self.total_expression,
                                anchor = tk.E, bg = LIGHT_GRAY,
                                fg = LABEL_COLOUR,
                                padx = 24, font = SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        current_label = tk.Label( self.display_frame,
                                text = self.current_expression,
                                anchor = tk.E, bg = LIGHT_GRAY,
                                fg = LABEL_COLOUR,
                                padx = 24, font = LARGE_FONT_STYLE)
        current_label.pack(expand=True, fill="both")

        return total_label, current_label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height = 221, bg = LIGHT_GRAY)
        frame.pack(expand = True, fill = "both")
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand = True, fill = "both")
        return frame

    def create_digits_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button( self.buttons_frame, text=str(digit),
                                bg=WHITE, fg=LABEL_COLOUR,
                                font=DIGITS_FONT_STYLE,
                                borderwidth=0 )
            button.grid(row=grid_value[0], column=grid_value[1],
                        sticky=tk.NSEW)

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button( self.buttons_frame, text=symbol,
                                bg=OFF_WHITE, fg=LABEL_COLOUR,
                                font=DEFAULT_FONT_STYLE,
                                borderwidth=0 )
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1

    def create_clear_button(self):
        button = tk.Button( self.buttons_frame, text="C",
                            bg=OFF_WHITE, fg=LABEL_COLOUR,
                            font=DEFAULT_FONT_STYLE,
                            borderwidth=0 )
        button.grid(row=0, column=1, columnspan = 3, sticky=tk.NSEW)

    def create_equals_button(self):
        button = tk.Button( self.buttons_frame, text="=",
                            bg=LIGHT_BLUE, fg=LABEL_COLOUR,
                            font=DEFAULT_FONT_STYLE,
                            borderwidth=0 )
        button.grid(row=4, column=3, columnspan = 2, sticky=tk.NSEW)

    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def update_current_label(self):
        self.current_label.config(text=self.current_expression)

    def run(self):
        self.window.mainloop()



if __name__ == "__main__":
    calc = Calculator()
    calc.run()

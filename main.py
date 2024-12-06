from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

import matplotlib.pyplot as plt

Window.size = (400, 700)  # Set window size

KV = '''
ScrollView:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            id: result_label
            text: "Welcome to Kriss-style Calculator"
            halign: "center"
            font_style: "H6"

        MDTextField:
            id: num1
            hint_text: "Enter first number"
            input_filter: "float"
            mode: "rectangle"

        MDTextField:
            id: num2
            hint_text: "Enter second number"
            input_filter: "float"
            mode: "rectangle"

        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: dp(50)

            MDRaisedButton:
                text: "Add"
                on_release: app.perform_operation("Add")

            MDRaisedButton:
                text: "Subtract"
                on_release: app.perform_operation("Subtract")

        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: dp(50)

            MDRaisedButton:
                text: "Multiply"
                on_release: app.perform_operation("Multiply")

            MDRaisedButton:
                text: "Divide"
                on_release: app.perform_operation("Divide")

        MDRaisedButton:
            text: "Square"
            on_release: app.square_operation()
        
        MDTextField:
            id: x_values
            hint_text: "X-axis values (comma-separated)"
            mode: "rectangle"

        MDTextField:
            id: y_values
            hint_text: "Y-axis values (comma-separated)"
            mode: "rectangle"

        MDTextField:
            id: graph_title
            hint_text: "Graph Title"
            mode: "rectangle"

        MDTextField:
            id: x_label
            hint_text: "X-axis Label"
            mode: "rectangle"

        MDTextField:
            id: y_label
            hint_text: "Y-axis Label"
            mode: "rectangle"

        MDRaisedButton:
            text: "Create Bar Graph"
            on_release: app.create_bar_graph()

        MDTextField:
            id: pie_values
            hint_text: "Pie chart values (comma-separated)"
            mode: "rectangle"

        MDRaisedButton:
            text: "Create Pie Chart"
            on_release: app.create_pie_chart()

        MDRaisedButton:
            text: "Exit"
            on_release: app.exit_program()
'''



class CalculatorApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def perform_operation(self, operation):
        num1 = self.root.ids.num1.text
        num2 = self.root.ids.num2.text
        try:
            num1 = float(num1)
            num2 = float(num2)
            if operation == "Add":
                result = num1 + num2
            elif operation == "Subtract":
                result = num1 - num2
            elif operation == "Multiply":
                result = num1 * num2
            elif operation == "Divide":
                if num2 == 0:
                    raise ValueError("Cannot divide by zero")
                result = num1 / num2
            self.root.ids.result_label.text = f"Answer: {result}"
        except ValueError:
            self.show_dialog("Input Error", "Please enter valid numbers.")

    def square_operation(self):
        num = self.root.ids.num1.text
        try:
            num = float(num)
            result = num ** 2
            self.root.ids.result_label.text = f"The square of {num} is {result}"
        except ValueError:
            self.show_dialog("Input Error", "Please enter a valid number.")

    def create_bar_graph(self):
        x = self.root.ids.x_values.text.split(",")
        y = self.root.ids.y_values.text.split(",")
        try:
            y = list(map(int, y))
            plt.bar(x, y, color='skyblue')
            plt.title(self.root.ids.graph_title.text)
            plt.xlabel(self.root.ids.x_label.text)
            plt.ylabel(self.root.ids.y_label.text)
            plt.show()
        except ValueError:
            self.show_dialog("Input Error", "Please enter valid values for the graph.")

    def create_pie_chart(self):
        values = self.root.ids.pie_values.text.split(",")
        try:
            values = list(map(int, values))
            plt.pie(values, labels=values, autopct='%1.1f%%', startangle=140)
            plt.show()
        except ValueError:
            self.show_dialog("Input Error", "Please enter valid values for the pie chart.")

    def exit_program(self):
        self.stop()

    def show_dialog(self, title, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=message,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()


if __name__ == "__main__":
    CalculatorApp().run()

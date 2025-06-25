from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
import matplotlib.pyplot as plt

Window.size = (400, 720)

KV = '''
MDScreenManager:
    MainScreen:
    BarGraphScreen:
    PieChartScreen:

<MainScreen>:
    name: "main"

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Graph Utility App"
            halign: "center"
            font_style: "H5"

        MDRaisedButton:
            text: "Bar Graph"
            on_release: root.manager.current = "bar"

        MDRaisedButton:
            text: "Pie Chart"
            on_release: root.manager.current = "pie"

<BarGraphScreen>:
    name: "bar"

    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(15)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "Bar Graph Inputs"
                halign: "center"
                font_style: "H6"

            MDTextField:
                id: x_values
                hint_text: "X values (comma-separated)"
                mode: "rectangle"

            MDTextField:
                id: y_values
                hint_text: "Y values (comma-separated)"
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
                text: "Generate Bar Graph"
                on_release: app.create_bar_graph()

            MDRaisedButton:
                text: "Back"
                on_release: root.manager.current = "main"

<PieChartScreen>:
    name: "pie"

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)

        MDLabel:
            text: "Pie Chart Inputs"
            halign: "center"
            font_style: "H6"

        MDTextField:
            id: pie_values
            hint_text: "Values (comma-separated)"
            mode: "rectangle"

        MDRaisedButton:
            text: "Generate Pie Chart"
            on_release: app.create_pie_chart()

        MDRaisedButton:
            text: "Back"
            on_release: root.manager.current = "main"
'''


class MainScreen(MDScreen):
    pass

class BarGraphScreen(MDScreen):
    pass

class PieChartScreen(MDScreen):
    pass


class GraphApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def create_bar_graph(self):
        try:
            screen = self.root.get_screen("bar")
            x = [i.strip() for i in screen.ids.x_values.text.split(",")]
            y = list(map(float, screen.ids.y_values.text.split(",")))

            if len(x) != len(y):
                raise ValueError("X and Y must be the same length.")

            plt.figure(figsize=(6, 4))
            plt.bar(x, y, color='skyblue')
            plt.title(screen.ids.graph_title.text)
            plt.xlabel(screen.ids.x_label.text)
            plt.ylabel(screen.ids.y_label.text)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    def create_pie_chart(self):
        try:
            screen = self.root.get_screen("pie")
            values = list(map(float, screen.ids.pie_values.text.split(",")))

            if not values:
                raise ValueError("Enter at least one number.")

            plt.figure(figsize=(5, 5))
            plt.pie(values, labels=[str(v) for v in values], autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    def show_dialog(self, title, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()


if __name__ == "__main__":
    GraphApp().run()

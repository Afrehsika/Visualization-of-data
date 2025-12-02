from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.metrics import dp
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from statistics_engine import (
    DescriptiveStats, CorrelationAnalysis, RegressionAnalysis,
    HypothesisTesting, ProbabilityDistributions, OutlierDetection
)
from utils import (
    parse_numeric_data, read_data_file, preview_data,
    get_numeric_columns, detect_missing_values, handle_missing_values,
    normalize_data, standardize_data, export_to_csv
)
from analysis_screens import (
    DescriptiveStatsScreen, CorrelationScreen, RegressionScreen,
    HypothesisTestScreen, DataViewScreen
)
from visualization_screens import (
    BoxPlotScreen, ScatterPlotScreen, HeatmapScreen,
    QQPlotScreen, ViolinPlotScreen
)


Window.size = (900, 700)

# Set matplotlib and seaborn style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (8, 6)

KV = '''
<DrawerClickableItem@OneLineIconListItem>:
    theme_text_color: "Custom"
    text_color: app.theme_cls.text_color
    icon_color: app.theme_cls.primary_color

<ContentNavigationDrawer>:
    MDBoxLayout:
        orientation: "vertical"
        padding: "8dp"
        spacing: "8dp"

        MDLabel:
            text: "Statistical Analysis"
            font_style: "H5"
            size_hint_y: None
            height: self.texture_size[1]
            padding: "10dp", "10dp"
        
        MDLabel:
            text: "Professional Statistical Software"
            font_style: "Caption"
            size_hint_y: None
            height: self.texture_size[1]
            padding: "10dp", "5dp"

        ScrollView:
            MDList:
                OneLineListItem:
                    text: "HOME"
                    divider: None
                    _no_ripple_effect: True
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                DrawerClickableItem:
                    text: "Home"
                    icon: "home"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "main"
                
                OneLineListItem:
                    text: "DATA MANAGEMENT"
                    divider: None
                    _no_ripple_effect: True
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                DrawerClickableItem:
                    text: "Data View"
                    icon: "table"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "dataview"

                OneLineListItem:
                    text: "BASIC CHARTS"
                    divider: None
                    _no_ripple_effect: True
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                DrawerClickableItem:
                    text: "Bar Graph"
                    icon: "chart-bar"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "bar"

                DrawerClickableItem:
                    text: "Pie Chart"
                    icon: "chart-pie"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "pie"

                DrawerClickableItem:
                    text: "Histogram"
                    icon: "chart-histogram"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "histogram"

                DrawerClickableItem:
                    text: "Line Chart"
                    icon: "chart-line"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "line"

                OneLineListItem:
                    text: "ADVANCED VISUALIZATIONS"
                    divider: None
                    _no_ripple_effect: True
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                DrawerClickableItem:
                    text: "Box Plot"
                    icon: "box"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "boxplot"

                DrawerClickableItem:
                    text: "Scatter Plot"
                    icon: "chart-scatter-plot"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scatter"

                DrawerClickableItem:
                    text: "Heatmap"
                    icon: "grid"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "heatmap"

                DrawerClickableItem:
                    text: "Q-Q Plot"
                    icon: "chart-bell-curve"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "qqplot"

                OneLineListItem:
                    text: "STATISTICAL ANALYSIS"
                    divider: None
                    _no_ripple_effect: True
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                DrawerClickableItem:
                    text: "Descriptive Statistics"
                    icon: "calculator"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "descriptive"

                DrawerClickableItem:
                    text: "Correlation Analysis"
                    icon: "chart-scatter-plot-hexbin"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "correlation"

                DrawerClickableItem:
                    text: "Regression Analysis"
                    icon: "chart-line-variant"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "regression"

                DrawerClickableItem:
                    text: "Hypothesis Testing"
                    icon: "test-tube"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "hypothesis"

MDNavigationLayout:
    MDScreenManager:
        id: screen_manager

        MainScreen:
        DataViewScreen:
        BarGraphScreen:
        PieChartScreen:
        HistogramScreen:
        LineChartScreen:
        BoxPlotScreen:
        ScatterPlotScreen:
        HeatmapScreen:
        QQPlotScreen:
        DescriptiveStatsScreen:
        CorrelationScreen:
        RegressionScreen:
        HypothesisTestScreen:

    MDNavigationDrawer:
        id: nav_drawer
        radius: (0, 16, 16, 0)
        
        ContentNavigationDrawer:
            screen_manager: screen_manager
            nav_drawer: nav_drawer

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Statistical Analysis Software"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(30)
                spacing: dp(20)
                size_hint_y: None
                height: self.minimum_height
                
                MDLabel:
                    text: "Welcome to Statistical Analysis Software"
                    halign: "center"
                    font_style: "H4"
                    size_hint_y: None
                    height: self.texture_size[1]
                
                MDLabel:
                    text: "Professional-grade statistical analysis and visualization"
                    halign: "center"
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: self.texture_size[1]
                
                Widget:
                    size_hint_y: None
                    height: dp(20)
                
                MDCard:
                    orientation: "vertical"
                    padding: dp(20)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 2
                    
                    MDLabel:
                        text: "Quick Start"
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDLabel:
                        text: "1. Import your data (CSV/Excel) from Data View"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDLabel:
                        text: "2. Choose a visualization or analysis from the menu"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDLabel:
                        text: "3. View results and export reports"
                        size_hint_y: None
                        height: self.texture_size[1]

                Widget:

<DataViewScreen>:
    name: "dataview"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Data Management"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: file_path
                    hint_text: "File Path (CSV or Excel)"
                    mode: "rectangle"
                    helper_text: "Enter full path to your data file"
                    helper_text_mode: "on_focus"

                MDRaisedButton:
                    text: "Load Data"
                    on_release: app.load_data_file(file_path.text)

                MDLabel:
                    id: data_preview
                    text: "No data loaded"
                    font_name: "RobotoMono-Regular"
                    size_hint_y: None
                    height: self.texture_size[1]

<BarGraphScreen>:
    name: "bar"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Bar Graph"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    
                    MDLabel:
                        text: "Use Loaded Data"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(40)
                        
                        MDRaisedButton:
                            text: "Fill X from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("bar", "x_values")
                        
                        MDRaisedButton:
                            text: "Fill Y from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("bar", "y_values")

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


<PieChartScreen>:
    name: "pie"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Pie Chart"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: pie_values
                    hint_text: "Values (comma-separated)"
                    mode: "rectangle"
                
                MDTextField:
                    id: pie_labels
                    hint_text: "Labels (comma-separated, optional)"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Generate Pie Chart"
                    on_release: app.create_pie_chart()

<HistogramScreen>:
    name: "histogram"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Histogram"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: raw_data
                    hint_text: "Raw Data (comma-separated)"
                    mode: "rectangle"

                MDTextField:
                    id: bins
                    hint_text: "Number of Bins (optional, default: 10)"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Generate Histogram"
                    on_release: app.create_histogram()

<LineChartScreen>:
    name: "line"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Line Chart"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: slope
                    hint_text: "Slope (m)"
                    mode: "rectangle"

                MDTextField:
                    id: intercept
                    hint_text: "Y-Intercept (c)"
                    mode: "rectangle"
                
                MDLabel:
                    text: "OR"
                    halign: "center"
                
                MDTextField:
                    id: x_points
                    hint_text: "X Points (comma-separated)"
                    mode: "rectangle"

                MDTextField:
                    id: y_points
                    hint_text: "Y Points (comma-separated)"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Generate Line Chart"
                    on_release: app.create_line_chart()

<BoxPlotScreen>:
    name: "boxplot"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Box Plot"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: data
                    hint_text: "Data (comma-separated)"
                    mode: "rectangle"
                    multiline: True

                MDTextField:
                    id: title
                    hint_text: "Plot Title"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Generate Box Plot"
                    on_release: app.create_boxplot()

<ScatterPlotScreen>:
    name: "scatter"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Scatter Plot"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    
                    MDLabel:
                        text: "Use Loaded Data"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(40)
                        
                        MDRaisedButton:
                            text: "Fill X from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("scatter", "x_data")
                        
                        MDRaisedButton:
                            text: "Fill Y from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("scatter", "y_data")

                MDTextField:
                    id: x_data
                    hint_text: "X Data (comma-separated)"
                    mode: "rectangle"

                MDTextField:
                    id: y_data
                    hint_text: "Y Data (comma-separated)"
                    mode: "rectangle"

                MDSwitch:
                    id: show_regression
                    active: True
                    pos_hint: {"center_x": 0.5}

                MDLabel:
                    text: "Show Regression Line"
                    pos_hint: {"center_x": 0.5}

                MDRaisedButton:
                    text: "Generate Scatter Plot"
                    on_release: app.create_scatterplot()

<HeatmapScreen>:
    name: "heatmap"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Correlation Heatmap"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Load data from Data View to generate heatmap"
                    halign: "center"

                MDRaisedButton:
                    text: "Generate Heatmap from Loaded Data"
                    on_release: app.create_heatmap()

<QQPlotScreen>:
    name: "qqplot"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Q-Q Plot (Normality Test)"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: data
                    hint_text: "Data (comma-separated)"
                    mode: "rectangle"
                    multiline: True

                MDRaisedButton:
                    text: "Generate Q-Q Plot"
                    on_release: app.create_qqplot()

<DescriptiveStatsScreen>:
    name: "descriptive"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Descriptive Statistics"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDTextField:
                    id: data
                    hint_text: "Data (comma-separated)"
                    mode: "rectangle"
                    multiline: True

                MDRaisedButton:
                    text: "Calculate Statistics"
                    on_release: app.calculate_descriptive_stats()

                MDLabel:
                    id: results
                    text: ""
                    font_name: "RobotoMono-Regular"
                    size_hint_y: None
                    height: self.texture_size[1]

<CorrelationScreen>:
    name: "correlation"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Correlation Analysis"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    
                    MDLabel:
                        text: "Use Loaded Data"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(40)
                        
                        MDRaisedButton:
                            text: "Fill X from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("correlation", "x_data")
                        
                        MDRaisedButton:
                            text: "Fill Y from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("correlation", "y_data")

                MDTextField:
                    id: x_data
                    hint_text: "X Data (comma-separated)"
                    mode: "rectangle"

                MDTextField:
                    id: y_data
                    hint_text: "Y Data (comma-separated)"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Calculate Correlation"
                    on_release: app.calculate_correlation()

                MDLabel:
                    id: results
                    text: ""
                    font_name: "RobotoMono-Regular"
                    size_hint_y: None
                    height: self.texture_size[1]

<RegressionScreen>:
    name: "regression"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Regression Analysis"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: dp(15)
                    spacing: dp(10)
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    
                    MDLabel:
                        text: "Use Loaded Data"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(40)
                        
                        MDRaisedButton:
                            text: "Fill X from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("regression", "x_data")
                        
                        MDRaisedButton:
                            text: "Fill Y from Column"
                            size_hint_x: 0.5
                            on_release: app.show_column_selector("regression", "y_data")

                MDTextField:
                    id: x_data
                    hint_text: "X Data (comma-separated)"
                    mode: "rectangle"

                MDTextField:
                    id: y_data
                    hint_text: "Y Data (comma-separated)"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Perform Regression"
                    on_release: app.perform_regression()

                MDLabel:
                    id: results
                    text: ""
                    font_name: "RobotoMono-Regular"
                    size_hint_y: None
                    height: self.texture_size[1]

<HypothesisTestScreen>:
    name: "hypothesis"
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Hypothesis Testing"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "One-Sample T-Test"
                    font_style: "H6"

                MDTextField:
                    id: sample_data
                    hint_text: "Sample Data (comma-separated)"
                    mode: "rectangle"

                MDTextField:
                    id: pop_mean
                    hint_text: "Population Mean"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Run One-Sample T-Test"
                    on_release: app.run_one_sample_ttest()

                MDLabel:
                    text: "Two-Sample T-Test"
                    font_style: "H6"

                MDTextField:
                    id: sample1
                    hint_text: "Sample 1 (comma-separated)"
                    mode: "rectangle"

                MDTextField:
                    id: sample2
                    hint_text: "Sample 2 (comma-separated)"
                    mode: "rectangle"

                MDRaisedButton:
                    text: "Run Two-Sample T-Test"
                    on_release: app.run_two_sample_ttest()

                MDLabel:
                    id: results
                    text: ""
                    font_name: "RobotoMono-Regular"
                    size_hint_y: None
                    height: self.texture_size[1]
'''


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = None
    nav_drawer = None


class MainScreen(MDScreen):
    pass


class BarGraphScreen(MDScreen):
    pass


class PieChartScreen(MDScreen):
    pass


class HistogramScreen(MDScreen):
    pass


class LineChartScreen(MDScreen):
    pass


class StatisticalApp(MDApp):
    dialog = None
    loaded_data = None  # Store loaded DataFrame

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_string(KV)

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

    # Data Management
    def load_data_file(self, file_path):
        try:
            self.loaded_data = read_data_file(file_path)
            preview = preview_data(self.loaded_data)
            
            screen = self.root.ids.screen_manager.get_screen("dataview")
            screen.ids.data_preview.text = preview
            
            self.show_dialog("Success", f"Loaded {len(self.loaded_data)} rows successfully!")
        except Exception as e:
            self.show_dialog("Error", str(e))

    def show_column_selector(self, screen_name, field_id):
        """Show a dialog to select a column from loaded data"""
        if self.loaded_data is None:
            self.show_dialog("Error", "No data loaded. Please load data from Data View first.")
            return
        
        # Create menu items for each column
        menu_items = []
        for col in self.loaded_data.columns:
            menu_items.append({
                "text": col,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=col: self.populate_field_from_column(screen_name, field_id, x)
            })
        
        # Create and show dropdown menu
        screen = self.root.ids.screen_manager.get_screen(screen_name)
        field = screen.ids[field_id]
        
        self.column_menu = MDDropdownMenu(
            caller=field,
            items=menu_items,
            width_mult=4,
        )
        self.column_menu.open()

    def populate_field_from_column(self, screen_name, field_id, column_name):
        """Populate a text field with data from a specific column"""
        try:
            if self.loaded_data is None:
                self.show_dialog("Error", "No data loaded.")
                return
            
            if column_name not in self.loaded_data.columns:
                self.show_dialog("Error", f"Column '{column_name}' not found.")
                return
            
            # Get the data from the column
            column_data = self.loaded_data[column_name].tolist()
            
            # Convert to comma-separated string
            data_string = ", ".join([str(val) for val in column_data])
            
            # Set the field text
            screen = self.root.ids.screen_manager.get_screen(screen_name)
            field = screen.ids[field_id]
            field.text = data_string
            
            # Close the menu
            if hasattr(self, 'column_menu'):
                self.column_menu.dismiss()
            
        except Exception as e:
            self.show_dialog("Error", str(e))


    # Basic Charts
    def create_bar_graph(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("bar")
            x_text = screen.ids.x_values.text
            y_text = screen.ids.y_values.text
            
            if not x_text or not y_text:
                raise ValueError("Please enter X and Y values.")

            x = [i.strip() for i in x_text.split(",")]
            y = parse_numeric_data(y_text)

            if len(x) != len(y):
                raise ValueError("X and Y must be the same length.")

            plt.figure(figsize=(8, 6))
            plt.bar(x, y, color='#3F51B5', edgecolor='black', alpha=0.7)
            plt.title(screen.ids.graph_title.text or "Bar Graph", fontsize=14, fontweight='bold')
            plt.xlabel(screen.ids.x_label.text or "X Axis")
            plt.ylabel(screen.ids.y_label.text or "Y Axis")
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    def create_pie_chart(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("pie")
            values = parse_numeric_data(screen.ids.pie_values.text)
            labels_text = screen.ids.pie_labels.text
            
            if not values:
                raise ValueError("Enter at least one number.")
            
            labels = [l.strip() for l in labels_text.split(",")] if labels_text else [str(v) for v in values]
            labels = labels[:len(values)]

            plt.figure(figsize=(7, 7))
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, 
                   colors=sns.color_palette("Set2"))
            plt.axis('equal')
            plt.title("Pie Chart", fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    def create_histogram(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("histogram")
            data = parse_numeric_data(screen.ids.raw_data.text)
            bins_text = screen.ids.bins.text
            
            if not data:
                raise ValueError("Please enter data.")
            
            bins = int(bins_text) if bins_text else 10

            plt.figure(figsize=(8, 6))
            plt.hist(data, bins=bins, color='#FF9800', edgecolor='black', alpha=0.7)
            plt.title("Histogram", fontsize=14, fontweight='bold')
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    def create_line_chart(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("line")
            slope_text = screen.ids.slope.text
            intercept_text = screen.ids.intercept.text
            x_points_text = screen.ids.x_points.text
            y_points_text = screen.ids.y_points.text

            plt.figure(figsize=(8, 6))

            if slope_text and intercept_text:
                m = float(slope_text)
                c = float(intercept_text)
                x = np.linspace(-10, 10, 100)
                y = m * x + c
                plt.plot(x, y, label=f"y = {m}x + {c}", color="#3F51B5", linewidth=2)
                plt.title(f"Line: y = {m}x + {c}", fontsize=14, fontweight='bold')
            
            elif x_points_text and y_points_text:
                x = parse_numeric_data(x_points_text)
                y = parse_numeric_data(y_points_text)
                if len(x) != len(y):
                    raise ValueError("X and Y points must have same length")
                plt.plot(x, y, marker='o', linestyle='-', color='#9C27B0', linewidth=2)
                plt.title("Line Chart", fontsize=14, fontweight='bold')
            
            else:
                raise ValueError("Enter Slope/Intercept OR X/Y Points")

            plt.xlabel("X Axis")
            plt.ylabel("Y Axis")
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()

        except Exception as e:
            self.show_dialog("Input Error", str(e))

    # Advanced Visualizations
    def create_boxplot(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("boxplot")
            data = parse_numeric_data(screen.ids.data.text)
            
            if not data:
                raise ValueError("Please enter data.")

            plt.figure(figsize=(8, 6))
            plt.boxplot(data, vert=True, patch_artist=True,
                       boxprops=dict(facecolor='#4CAF50', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2))
            plt.title(screen.ids.title.text or "Box Plot", fontsize=14, fontweight='bold')
            plt.ylabel("Value")
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    def create_scatterplot(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("scatter")
            x = parse_numeric_data(screen.ids.x_data.text)
            y = parse_numeric_data(screen.ids.y_data.text)
            
            if not x or not y:
                raise ValueError("Please enter both X and Y data.")
            
            if len(x) != len(y):
                raise ValueError("X and Y must have same length.")

            plt.figure(figsize=(8, 6))
            plt.scatter(x, y, alpha=0.6, s=100, color='#2196F3', edgecolors='black')
            
            if screen.ids.show_regression.active:
                result = RegressionAnalysis.linear_regression(x, y)
                plt.plot(x, result['predictions'], color='red', linewidth=2, 
                        label=f"{result['equation']} (R²={result['r_squared']:.3f})")
                plt.legend()
            
            plt.title("Scatter Plot", fontsize=14, fontweight='bold')
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    def create_heatmap(self):
        try:
            if self.loaded_data is None:
                raise ValueError("Please load data first from Data View")
            
            numeric_cols = get_numeric_columns(self.loaded_data)
            if len(numeric_cols) < 2:
                raise ValueError("Need at least 2 numeric columns for correlation")
            
            corr_matrix = self.loaded_data[numeric_cols].corr()
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=1, cbar_kws={"shrink": 0.8})
            plt.title("Correlation Heatmap", fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Error", str(e))

    def create_qqplot(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("qqplot")
            data = parse_numeric_data(screen.ids.data.text)
            
            if not data:
                raise ValueError("Please enter data.")

            from scipy import stats as sp_stats
            plt.figure(figsize=(8, 6))
            sp_stats.probplot(data, dist="norm", plot=plt)
            plt.title("Q-Q Plot (Normality Test)", fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.show_dialog("Input Error", str(e))

    # Statistical Analyses
    def calculate_descriptive_stats(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("descriptive")
            data = parse_numeric_data(screen.ids.data.text)
            
            if not data:
                raise ValueError("Please enter data.")
            
            stats = DescriptiveStats.calculate_all(data)
            results = DescriptiveStats.format_results(stats)
            
            screen.ids.results.text = results
        except Exception as e:
            self.show_dialog("Error", str(e))

    def calculate_correlation(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("correlation")
            x = parse_numeric_data(screen.ids.x_data.text)
            y = parse_numeric_data(screen.ids.y_data.text)
            
            if not x or not y:
                raise ValueError("Please enter both X and Y data.")
            
            if len(x) != len(y):
                raise ValueError("X and Y must have same length.")
            
            pearson_r, pearson_p = CorrelationAnalysis.pearson(x, y)
            spearman_r, spearman_p = CorrelationAnalysis.spearman(x, y)
            
            results = f"""Correlation Analysis Results:
{'='*50}
Pearson Correlation:
  Coefficient: {pearson_r:.4f}
  P-value: {pearson_p:.4f}
  Significant: {'Yes' if pearson_p < 0.05 else 'No'}

Spearman Correlation:
  Coefficient: {spearman_r:.4f}
  P-value: {spearman_p:.4f}
  Significant: {'Yes' if spearman_p < 0.05 else 'No'}
"""
            screen.ids.results.text = results
        except Exception as e:
            self.show_dialog("Error", str(e))

    def perform_regression(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("regression")
            x = parse_numeric_data(screen.ids.x_data.text)
            y = parse_numeric_data(screen.ids.y_data.text)
            
            if not x or not y:
                raise ValueError("Please enter both X and Y data.")
            
            if len(x) != len(y):
                raise ValueError("X and Y must have same length.")
            
            result = RegressionAnalysis.linear_regression(x, y)
            
            results = f"""Linear Regression Results:
{'='*50}
Equation: {result['equation']}
R-squared: {result['r_squared']:.4f}
Slope: {result['slope']:.4f}
Intercept: {result['intercept']:.4f}
P-value: {result['p_value']:.4f}
Standard Error: {result['std_err']:.4f}
"""
            screen.ids.results.text = results
            
            # Also show plot
            plt.figure(figsize=(8, 6))
            plt.scatter(x, y, alpha=0.6, s=100, color='#2196F3', edgecolors='black', label='Data')
            plt.plot(x, result['predictions'], color='red', linewidth=2, label='Regression Line')
            plt.title(f"Linear Regression: {result['equation']}", fontsize=14, fontweight='bold')
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            self.show_dialog("Error", str(e))

    def run_one_sample_ttest(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("hypothesis")
            data = parse_numeric_data(screen.ids.sample_data.text)
            pop_mean = float(screen.ids.pop_mean.text)
            
            if not data:
                raise ValueError("Please enter sample data.")
            
            result = HypothesisTesting.one_sample_ttest(data, pop_mean)
            
            results = f"""One-Sample T-Test Results:
{'='*50}
T-statistic: {result['t_statistic']:.4f}
P-value: {result['p_value']:.4f}
Significant (α=0.05): {'Yes' if result['significant'] else 'No'}
"""
            screen.ids.results.text = results
        except Exception as e:
            self.show_dialog("Error", str(e))

    def run_two_sample_ttest(self):
        try:
            screen = self.root.ids.screen_manager.get_screen("hypothesis")
            sample1 = parse_numeric_data(screen.ids.sample1.text)
            sample2 = parse_numeric_data(screen.ids.sample2.text)
            
            if not sample1 or not sample2:
                raise ValueError("Please enter both samples.")
            
            result = HypothesisTesting.two_sample_ttest(sample1, sample2)
            
            results = f"""Two-Sample T-Test Results:
{'='*50}
T-statistic: {result['t_statistic']:.4f}
P-value: {result['p_value']:.4f}
Significant (α=0.05): {'Yes' if result['significant'] else 'No'}
"""
            screen.ids.results.text = results
        except Exception as e:
            self.show_dialog("Error", str(e))


if __name__ == "__main__":
    StatisticalApp().run()

# Statistical Analysis Software

A comprehensive statistical analysis and visualization application built with KivyMD and Python.

## Features

### Data Management
- **Import Data**: Load CSV and Excel files
- **Data Preview**: View data structure and types
- **Missing Values**: Detect and handle missing data
- **Data Transformation**: Normalize and standardize data

### Basic Visualizations
- **Bar Graph**: Create bar charts with customizable labels
- **Pie Chart**: Generate pie charts with percentages
- **Histogram**: Visualize frequency distributions
- **Line Chart**: Plot linear functions or custom data points

### Advanced Visualizations
- **Box Plot**: Display data distribution and outliers
- **Scatter Plot**: Show relationships with optional regression lines
- **Correlation Heatmap**: Visualize correlation matrices
- **Q-Q Plot**: Test data normality

### Statistical Analyses
- **Descriptive Statistics**: Mean, median, mode, standard deviation, variance, quartiles, skewness, kurtosis
- **Correlation Analysis**: Pearson and Spearman correlation coefficients
- **Regression Analysis**: Linear regression with R², equation, and residuals
- **Hypothesis Testing**: One-sample t-test, two-sample t-test, paired t-test, chi-square, ANOVA

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application
```bash
python main.py
```

### Quick Start Guide

1. **Load Data**:
   - Navigate to "Data View" from the menu
   - Enter the full path to your CSV or Excel file
   - Click "Load Data"
   - View the data preview

2. **Create Visualizations**:
   - Select a chart type from the menu
   - Enter your data (comma-separated values) or use loaded data
   - Click the generate button
   - View the plot

3. **Perform Statistical Analysis**:
   - Select an analysis type from the menu
   - Enter your data
   - Click the calculate/run button
   - View results in the app

### Example Data

A sample dataset (`sample_data.csv`) is included for testing:
```
Name,Age,Score,Grade
Alice,23,85,A
Bob,25,78,B
...
```

### Example Usage

**Descriptive Statistics**:
1. Go to "Descriptive Statistics"
2. Enter data: `12, 15, 18, 20, 22, 25, 28, 30`
3. Click "Calculate Statistics"
4. View mean, median, std dev, etc.

**Correlation Analysis**:
1. Go to "Correlation Analysis"
2. Enter X data: `1, 2, 3, 4, 5`
3. Enter Y data: `2, 4, 6, 8, 10`
4. Click "Calculate Correlation"
5. View Pearson and Spearman coefficients

**Regression Analysis**:
1. Go to "Regression Analysis"
2. Enter X and Y data
3. Click "Perform Regression"
4. View equation, R², and regression plot

**Hypothesis Testing**:
1. Go to "Hypothesis Testing"
2. For one-sample t-test:
   - Enter sample data
   - Enter population mean
   - Click "Run One-Sample T-Test"
3. View t-statistic and p-value

## Project Structure

```
Visualization-of-data/
├── main.py                      # Main application
├── statistics_engine.py         # Statistical calculations
├── utils.py                     # Data utilities
├── analysis_screens.py          # Analysis UI screens
├── visualization_screens.py     # Visualization UI screens
├── requirements.txt             # Dependencies
├── sample_data.csv             # Sample dataset
├── histogram.py                # Legacy histogram script
├── straightLine.py             # Legacy line script
└── st.py                       # Legacy script
```

## Dependencies

- **kivymd**: Modern Material Design UI framework
- **matplotlib**: Plotting and visualization
- **seaborn**: Statistical data visualization
- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **scipy**: Scientific computing and statistics
- **openpyxl**: Excel file support

## Tips

- **Data Format**: Use comma-separated values (e.g., `1, 2, 3, 4, 5`)
- **File Paths**: Use full absolute paths for file imports
- **Missing Values**: Load data first, then use data management tools
- **Large Datasets**: For better performance, use smaller datasets or aggregate data

## Troubleshooting

**Issue**: "Module not found" error
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: File not found when loading data
- **Solution**: Use the full absolute path to your file

**Issue**: Plot window doesn't appear
- **Solution**: Check if matplotlib backend is configured correctly

**Issue**: App window too small
- **Solution**: Window size is set to 900x700. Modify `Window.size` in `main.py` if needed

## License

MIT License - See LICENSE file for details

## Author

Statistical Analysis Software v1.0

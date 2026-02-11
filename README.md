# Stock-Market-Forecasting-ML-Pipeline

End-to-end stock market data cleaning, forecasting, visualization, and automated machine learning report generation pipeline.

---

## Overview

This project implements a complete machine learning workflow for stock market data forecasting and performance analysis.

It includes:

- Raw dataset cleaning and preprocessing
- Forecast model training
- Residual and error analysis
- Visualization generation
- Automated PDF reporting

The system transforms raw financial time-series data into structured forecasts and evaluation outputs.

---

## Project Structure

```
Stock-Market-Forecasting-ML-Pipeline/

├── cleaner.py
├── MLreport.py
├── stock_market_data_large.csv
├── clean_stock_market_data.csv
├── forecast_report.pdf
├── forecast_line.png
├── residual_plot.png
├── error_bar.png
├── distribution_pie.png
└── README.md
```

---

## Components

### Data Cleaning (cleaner.py)

- Loads raw stock market dataset
- Handles missing values
- Performs preprocessing
- Outputs cleaned dataset

Input:
- stock_market_data_large.csv

Output:
- clean_stock_market_data.csv

---

### Forecasting and Reporting (MLreport.py)

- Trains forecasting model
- Generates predictions
- Performs residual analysis
- Creates evaluation visualizations
- Produces final PDF report

Generated outputs:

- forecast_line.png
- residual_plot.png
- error_bar.png
- distribution_pie.png
- forecast_report.pdf

---

## Workflow

1. Load raw dataset
2. Clean and preprocess data
3. Train forecasting model
4. Generate predictions
5. Evaluate model performance
6. Produce visualizations
7. Generate structured report

---

## Installation

Clone the repository:

```bash
git clone https://github.com/sagnik10/Stock-Market-Forecasting-ML-Pipeline.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run data cleaning:

```bash
python cleaner.py
```

Run forecasting and report generation:

```bash
python MLreport.py
```

---

## Use Cases

- Financial time-series forecasting
- Machine learning portfolio demonstration
- Model evaluation and reporting
- Stock data analysis

---

## License

This repository is intended for educational and portfolio purposes.

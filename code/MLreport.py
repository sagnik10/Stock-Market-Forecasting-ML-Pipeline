import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from tqdm import tqdm
import argparse
import time

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--stock", default=None)
parser.add_argument("--horizon", type=int, default=1)
parser.add_argument("--output", default="forecast_report.pdf")
args = parser.parse_args()

print("Loading data...")
df = pd.read_csv("clean_stock_market_data.csv", parse_dates=True)

time_col = [c for c in df.columns if "date" in c or "time" in c][0]
df[time_col] = pd.to_datetime(df[time_col])
df = df.sort_values(time_col)

symbol_cols = [c for c in df.columns if c in ["symbol", "ticker", "stock", "company"]]

if args.stock and symbol_cols:
    df = df[df[symbol_cols[0]] == args.stock]

stock_name = args.stock if args.stock else "Multiple Stocks"

df["target"] = df["close"].shift(-args.horizon)
df.dropna(inplace=True)

features = ["close", "ma_5", "ma_10", "volatility"]
X = df[features]
y = df["target"]

split = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]
time_test = df[time_col].iloc[split:]

print("Training model...")
model = LinearRegression()
for _ in tqdm(range(1)):
    model.fit(X_train, y_train)

print("Predicting...")
predictions = np.array([
    model.predict(X_test.iloc[i:i+1])[0]
    for i in tqdm(range(len(X_test)))
])

residuals = y_test.values - predictions

ci = 1.96 * residuals.std()
upper = predictions + ci
lower = predictions - ci

print("Creating forecast plot...")
plt.figure(figsize=(10,5))
plt.plot(time_test, y_test.values, label="Actual", color="black")
plt.plot(time_test, predictions, label="Predicted", color="red", linestyle="--")
plt.fill_between(time_test, lower, upper, color="red", alpha=0.2, label="95% CI")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.title(f"{stock_name} Forecast")
plt.legend()
plt.grid(True)
plt.savefig("forecast_line.png", dpi=300)
plt.close()

print("Creating residual plot...")
plt.figure(figsize=(8,4))
plt.scatter(time_test, residuals)
plt.axhline(0, color="red")
plt.title("Residual Plot")
plt.xlabel("Date")
plt.ylabel("Residual")
plt.grid(True)
plt.savefig("residual_plot.png", dpi=300)
plt.close()

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("Creating error bar chart...")
plt.figure()
plt.bar(["MAE", "RMSE"], [mae, rmse])
plt.title("Error Metrics")
plt.savefig("error_bar.png", dpi=300)
plt.close()

print("Creating price distribution pie chart...")
price_bins = pd.cut(df["close"], bins=3, labels=["Low","Medium","High"])
dist = price_bins.value_counts()

plt.figure()
plt.pie(dist, labels=dist.index, autopct="%1.1f%%")
plt.title("Price Distribution")
plt.savefig("distribution_pie.png", dpi=300)
plt.close()

print("Building PDF report...")
doc = SimpleDocTemplate(args.output, pagesize=A4)
styles = getSampleStyleSheet()
content = []

content.append(Paragraph("Stock Market Forecasting Report", styles["Title"]))
content.append(Spacer(1,12))

content.append(Paragraph("Stock Selection", styles["Heading2"]))
content.append(Paragraph(stock_name, styles["Normal"]))

content.append(Spacer(1,12))
content.append(Paragraph("Forecast Horizon", styles["Heading2"]))
content.append(Paragraph(f"{args.horizon} step(s) ahead", styles["Normal"]))

content.append(Spacer(1,12))
content.append(Paragraph("Forecast Results", styles["Heading2"]))
content.append(Image("forecast_line.png", 400, 250))

content.append(Spacer(1,12))
content.append(Paragraph("Residual Diagnostics", styles["Heading2"]))
content.append(Image("residual_plot.png", 400, 200))

content.append(Spacer(1,12))
content.append(Paragraph("Error Metrics", styles["Heading2"]))
content.append(Image("error_bar.png", 300, 200))

content.append(Spacer(1,12))
content.append(Paragraph("Price Distribution", styles["Heading2"]))
content.append(Image("distribution_pie.png", 300, 200))

content.append(Spacer(1,12))
content.append(Paragraph(f"MAE: {mae:.4f}", styles["Normal"]))
content.append(Paragraph(f"RMSE: {rmse:.4f}", styles["Normal"]))

end_time = time.time()
content.append(Spacer(1,12))
content.append(Paragraph(f"Execution Time: {end_time-start_time:.2f} seconds", styles["Normal"]))

doc.build(content)

print("Pipeline completed successfully")
print(f"Total time taken: {end_time-start_time:.2f} seconds")
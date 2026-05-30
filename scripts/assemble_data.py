import yfinance as yf
import pandas as pd
import os

def assemble_data():
    os.makedirs("data", exist_ok=True)

    print("Downloading Aluminum spot prices...")
    # Aluminum spot (fastest to get)
    alu = yf.download("ALI=F", start="2015-01-01", end="2024-12-31", interval="1mo")
    alu["Close"].to_csv("data/aluminum.csv")
    print(f"Aluminum: {len(alu)} monthly observations")

    # The blueprint states Boeing cost of products and airline margins are from manually downloaded 10-K CSVs.
    # We will create mock CSV files so the pipeline has some data to run with.
    print("Generating mock data for Boeing costs...")
    dates = pd.date_range(start="2015-01-01", end="2024-12-31", freq="MS")
    boeing_costs = pd.DataFrame({"date": dates, "cost": [50 + (i * 0.1) for i in range(len(dates))]})
    boeing_costs.to_csv("data/boeing_costs.csv", index=False)

    print("Generating mock data for Airline margins...")
    delta_margins = pd.DataFrame({"date": dates, "margin": [10 - (i * 0.05) for i in range(len(dates))]})
    delta_margins.to_csv("data/delta_margins.csv", index=False)

    print("Generating mock data for Bauxite...")
    bauxite = pd.DataFrame({"date": dates, "price": [30 + (i * 0.02) for i in range(len(dates))]})
    bauxite.to_csv("data/bauxite.csv", index=False)

    print("Generating mock data for Alumina...")
    alumina = pd.DataFrame({"date": dates, "price": [300 + (i * 0.5) for i in range(len(dates))]})
    alumina.to_csv("data/alumina.csv", index=False)

    print("Data assembly complete. Files are in the data/ directory.")

if __name__ == "__main__":
    assemble_data()

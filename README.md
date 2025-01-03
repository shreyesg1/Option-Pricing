# Option Pricer Application

## Overview
This Python application provides a graphical user interface (GUI) for pricing European call and put options using the Black-Scholes model. The application allows users to input various parameters, visualize results, and generate heatmaps of option prices.

## Features
- **Option Pricing**:
  - Calculates prices for European call and put options using the Black-Scholes model.
  - Supports dynamic inputs for strike price, time to maturity, risk-free rate, and volatility.

- **Stock Data Retrieval**:
  - Fetches the current stock price and historical volatility using Yahoo Finance API.

- **Heatmap Visualization**:
  - Generates heatmaps for call and put option prices.
  - Configurable axes for spot price and volatility.
  - Displays values within heatmaps (optional).

- **User-Friendly GUI**:
  - Built with Tkinter for an intuitive interface.
  - Includes sliders for parameter adjustments and grid size control.
  - Real-time updates with delayed input handling.

## Requirements
- Python 3.8+
- Libraries:
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `yfinance`
  - `scipy`
  - `tkinter` (bundled with Python)

## Installation
1. Clone the repository or copy the script file.
2. Install the required libraries:
   ```bash
   pip install numpy matplotlib seaborn yfinance scipy
   ```
3. Run the script:
   ```bash
   python option_pricer.py
   ```

## How to Use
### 1. Enter Stock Information
- Input the stock ticker symbol in the **Ticker** field.
- Click the **Get Info** button to fetch the current stock price and historical volatility.

### 2. Configure Parameters
- Enter the following values:
  - **Strike Price**: The exercise price of the option.
  - **Time to Maturity**: The time until the option expires, in years.
  - **Risk-Free Rate**: The risk-free interest rate (e.g., 0.05 for 5%).
- Adjust the sliders for:
  - Spot price range (minimum and maximum).
  - Volatility range (minimum and maximum).
- Set the **Grid Size** for heatmap resolution.

### 3. Generate Heatmaps
- Heatmaps for call and put option prices are generated based on input parameters.
- Check the **Display Values in Heatmap** box to show numerical values in the heatmaps.

### 4. Visualize Results
- Heatmaps display how option prices vary with spot price and volatility.
- The Y-axis (volatility) is reversed for better interpretability.

### 5. Clear Data
- Clear heatmap results and reset inputs as needed.

## Black-Scholes Model
The application uses the Black-Scholes model for option pricing:

### Call Option Price
```plaintext
C = S * N(d1) - X * e^(-r * T) * N(d2)
```

### Put Option Price
```plaintext
P = X * e^(-r * T) * N(-d2) - S * N(-d1)
```

Where:
- \( d1 = \frac{\ln(S/X) + (r + \sigma^2 / 2)T}{\sigma \sqrt{T}} \)
- \( d2 = d1 - \sigma \sqrt{T} \)

### Inputs
- \( S \): Current stock price
- \( X \): Strike price
- \( T \): Time to maturity (in years)
- \( r \): Risk-free rate
- \( \sigma \): Volatility

## Notes
- Ensure the stock ticker is valid and available on Yahoo Finance.
- Handle inputs carefully; invalid data may result in calculation errors.
- Use the application for educational and illustrative purposes.

## Disclaimer
This application is for educational purposes only. It does not constitute financial advice or guarantee accurate predictions. Use at your own risk.


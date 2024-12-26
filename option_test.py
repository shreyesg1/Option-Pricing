import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from scipy.stats import norm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Black Scholes Method for call prices
def black_scholes_call(S, X, T, r, sigma):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)

# Black Scholes Method for put prices
def black_scholes_put(S, X, T, r, sigma):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return X * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def get_stock_price_and_volatility(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1mo")
    current_price = data['Close'].iloc[-1]
    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    volatility = np.std(log_returns) * np.sqrt(252)
    return current_price, volatility

def generate_heatmap_data(X, T, r, spot_prices, volatilities):
    call_prices = np.zeros((len(volatilities), len(spot_prices)))
    put_prices = np.zeros((len(volatilities), len(spot_prices)))
    for i, S in enumerate(spot_prices):
        for j, sigma in enumerate(volatilities):
            call_prices[j, i] = black_scholes_call(S, X, T, r, sigma)
            put_prices[j, i] = black_scholes_put(S, X, T, r, sigma)
    return call_prices, put_prices

class OptionPricingApp:
    def __init__(self, root):
        self.root = root
        root.title("Option Pricing Heatmap")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(self.main_frame, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Heatmap figure setup
        self.fig, self.ax = plt.subplots(figsize=(20, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack_forget()  # Initially hidden


        # Stock info section
        self.stock_info_label = ttk.Label(self.left_frame, text="Stock Information")
        self.stock_info_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.ticker_label = ttk.Label(self.left_frame, text="Ticker:")
        self.ticker_label.grid(row=1, column=0)

        self.ticker_entry = ttk.Entry(self.left_frame)
        self.ticker_entry.grid(row=1, column=1)

        self.get_info_button = ttk.Button(self.left_frame, text="Get Info", command=self.display_stock_info)
        self.get_info_button.grid(row=1, column=2)

        self.price_label = ttk.Label(self.left_frame, text="Current Price:")
        self.price_label.grid(row=2, column=0)

        self.price_value = ttk.Label(self.left_frame, text="N/A")
        self.price_value.grid(row=2, column=1)

        self.volatility_label = ttk.Label(self.left_frame, text="Historical Volatility:")
        self.volatility_label.grid(row=3, column=0)

        self.volatility_value = ttk.Label(self.left_frame, text="N/A")
        self.volatility_value.grid(row=3, column=1)

        # Heatmap input section
        self.strike_price_label = ttk.Label(self.left_frame, text="Strike Price:")
        self.strike_price_label.grid(row=4, column=0)

        self.strike_price_entry = ttk.Entry(self.left_frame)
        self.strike_price_entry.grid(row=4, column=1)

        self.time_label = ttk.Label(self.left_frame, text="Time to Maturity (Years):")
        self.time_label.grid(row=5, column=0)

        self.time_entry = ttk.Entry(self.left_frame)
        self.time_entry.grid(row=5, column=1)

        self.risk_free_rate_label = ttk.Label(self.left_frame, text="Risk-Free Rate (Decimal):")
        self.risk_free_rate_label.grid(row=6, column=0)

        self.risk_free_rate_entry = ttk.Entry(self.left_frame)
        self.risk_free_rate_entry.grid(row=6, column=1)

        # Sliders
        self.volatility_min_label = ttk.Label(self.left_frame, text="Min Volatility:")
        self.volatility_min_label.grid(row=7, column=0)

        self.volatility_min_slider = ttk.Scale(self.left_frame, from_=0.1, to=1, orient="horizontal", command=self.update_heatmap)
        self.volatility_min_slider.set(0.2)
        self.volatility_min_slider.grid(row=7, column=1)

        self.volatility_max_label = ttk.Label(self.left_frame, text="Max Volatility:")
        self.volatility_max_label.grid(row=8, column=0)

        self.volatility_max_slider = ttk.Scale(self.left_frame, from_=0.1, to=1, orient="horizontal", command=self.update_heatmap)
        self.volatility_max_slider.set(0.5)
        self.volatility_max_slider.grid(row=8, column=1)

        self.spot_min_label = ttk.Label(self.left_frame, text="Min Spot Price:")
        self.spot_min_label.grid(row=9, column=0)

        self.spot_min_slider = ttk.Scale(self.left_frame, from_=0, to=200, orient="horizontal", command=self.update_heatmap) # 0 is 0x and 200 is 2x. Change accordingly
        self.spot_min_slider.set(50)
        self.spot_min_slider.grid(row=9, column=1)

        self.spot_max_label = ttk.Label(self.left_frame, text="Max Spot Price:")
        self.spot_max_label.grid(row=10, column=0)

        self.spot_max_slider = ttk.Scale(self.left_frame, from_=0, to=200, orient="horizontal", command=self.update_heatmap) # The same here
        self.spot_max_slider.set(150)
        self.spot_max_slider.grid(row=10, column=1)

        # Checkbox to toggle annotations
        self.show_values_var = tk.BooleanVar(value=False)
        self.show_values_checkbox = ttk.Checkbutton(self.left_frame, text="Display Values in Heatmap", variable=self.show_values_var, command=self.update_heatmap)
        self.show_values_checkbox.grid(row=11, column=0, columnspan=2, pady=10)

        # Entry for grid size
        self.grid_size_label = ttk.Label(self.left_frame, text="Grid Size (Points per Axis):")
        self.grid_size_label.grid(row=12, column=0)

        self.grid_size_entry = ttk.Entry(self.left_frame)
        self.grid_size_entry.grid(row=12, column=1)
        self.grid_size_entry.insert(0, "10")

        # Trigger heatmap update
        self.strike_price_entry.bind("<KeyRelease>", self.update_heatmap_with_delay)
        self.time_entry.bind("<KeyRelease>", self.update_heatmap_with_delay)
        self.risk_free_rate_entry.bind("<KeyRelease>", self.update_heatmap_with_delay)
        self.grid_size_entry.bind("<KeyRelease>", self.update_heatmap_with_delay)

        # Store update reference
        self.update_task = None

    # Waits one second after the last detected input to update
    def update_heatmap_with_delay(self, event=None):
        if self.update_task is not None:
            self.root.after_cancel(self.update_task)
        
        self.update_task = self.root.after(1000, self.update_heatmap)

    def update_heatmap(self, event=None):
        try:
            # Retrieve input values or use default placeholders
            strike_price = self.strike_price_entry.get()
            time_to_maturity = self.time_entry.get()
            risk_free_rate = self.risk_free_rate_entry.get()

            # Fetching slider values
            spot_min = self.spot_min_slider.get()
            spot_max = self.spot_max_slider.get()
            volatility_min = self.volatility_min_slider.get()
            volatility_max = self.volatility_max_slider.get()

            # Check if the required inputs are valid
            if not (strike_price and time_to_maturity and risk_free_rate):
                self.clear_heatmap()
                return

            # Convert inputs to float
            strike_price = float(strike_price)
            time_to_maturity = float(time_to_maturity)
            risk_free_rate = float(risk_free_rate)

            # Generate heatmap data
            grid_size = int(self.grid_size_entry.get()) if self.grid_size_entry.get().isdigit() else 10
            spot_prices = np.linspace(spot_min, spot_max, grid_size)
            volatilities = np.linspace(volatility_min, volatility_max, grid_size)

            # Generate call and put prices
            call_prices, put_prices = generate_heatmap_data(strike_price, time_to_maturity, risk_free_rate, spot_prices, volatilities)

            # Clear previous plot and create new one
            self.fig.clf()
            self.ax1 = self.fig.add_subplot(121)
            self.ax2 = self.fig.add_subplot(122)

            # Plot Call option prices
            sns.heatmap(call_prices, xticklabels=np.round(spot_prices, 2),
                        yticklabels=np.round(volatilities, 2), cmap="Blues", ax=self.ax1,
                        annot=self.show_values_var.get(), fmt=".2f", annot_kws={"size": 8})
            self.ax1.set_title("Call Option Prices")
            self.ax1.set_xlabel("Spot Price (S)")
            self.ax1.set_ylabel("Volatility (σ)")

            # Plot Put option prices
            sns.heatmap(put_prices, xticklabels=np.round(spot_prices, 2),
                        yticklabels=np.round(volatilities, 2), cmap="Reds", ax=self.ax2,
                        annot=self.show_values_var.get(), fmt=".2f", annot_kws={"size": 8})
            self.ax2.set_title("Put Option Prices")
            self.ax2.set_xlabel("Spot Price (S)")
            self.ax2.set_ylabel("Volatility (σ)")

            # Reverse the Y-axis so the highest volatility is at the top
            self.ax1.invert_yaxis()
            self.ax2.invert_yaxis()

            # Pack the canvas
            if not self.canvas.get_tk_widget().winfo_ismapped():
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Redraw the canvas
            self.canvas.draw()
            self.canvas.flush_events()

            print("Plot successfully drawn")

        except Exception as e:
            print(f"Error updating heatmap: {e}")


    def clear_heatmap(self):
        """Clear the heatmap canvas."""
        self.fig.clf()
        self.canvas.draw()

    # To view current price as to determine strike price
    def display_stock_info(self):
            ticker = self.ticker_entry.get()
            try:
                current_price, volatility = get_stock_price_and_volatility(ticker)
                self.price_value.config(text=f"{current_price:.2f}")
                self.volatility_value.config(text=f"{volatility:.2%}")
            except Exception as e:
                self.price_value.config(text="Error")
                self.volatility_value.config(text="Error")
                print(f"Error fetching stock info: {e}")

# Run the program
root = tk.Tk()
app = OptionPricingApp(root)
root.mainloop()

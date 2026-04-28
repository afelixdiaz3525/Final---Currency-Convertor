import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import os

class CurrencyConverter:
    def __init__(self):
        # Exchange rates relative to USD
        self.rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "JPY": 156.3,
            "GBP": 0.79,
            "MXN": 17.1
        }
        self.save_file = "last_conversion.pkl"

    def convert(self, amount, from_currency, to_currency):
        """Convert amount from one currency to another."""
        usd_value = amount / self.rates[from_currency]
        return usd_value * self.rates[to_currency]

    def save_last(self, data):
        with open(self.save_file, "wb") as f:
            pickle.dump(data, f)

    def load_last(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "rb") as f:
                return pickle.load(f)
        return None


class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Currency Converter")

        self.converter = CurrencyConverter()

        # --- Widgets ---
        tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(root, text="From:").grid(row=1, column=0)
        tk.Label(root, text="To:").grid(row=1, column=1)

        currencies = list(self.converter.rates.keys())
        self.from_box = ttk.Combobox(root, values=currencies, state="readonly")
        self.to_box = ttk.Combobox(root, values=currencies, state="readonly")
        self.from_box.grid(row=2, column=0, padx=10)
        self.to_box.grid(row=2, column=1, padx=10)

        self.result_label = tk.Label(root, text="Result: ")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(root, text="Convert", command=self.handle_convert).grid(row=4, column=0, pady=10)
        tk.Button(root, text="Clear", command=self.clear).grid(row=4, column=1)

        # Load last conversion
        last = self.converter.load_last()
        if last:
            self.result_label.config(text=f"Last Conversion:\n{last}")

    def handle_convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_c = self.from_box.get()
            to_c = self.to_box.get()

            if not from_c or not to_c:
                messagebox.showerror("Error", "Please select both currencies.")
                return

            result = self.converter.convert(amount, from_c, to_c)
            result_text = f"{amount} {from_c} = {round(result, 2)} {to_c}"
            self.result_label.config(text=result_text)
            self.converter.save_last(result_text)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def clear(self):
        self.amount_entry.delete(0, tk.END)
        self.result_label.config(text="Result: ")


if __name__ == "__main__":
    root = tk.Tk()
    ConverterGUI(root)
    root.mainloop()




import tkinter as tk
from tkinter import ttk, messagebox
import math
import requests
import json
from datetime import datetime
import threading

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator Pro")
        self.root.geometry("420x650")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = tk.StringVar()
        self.current_input.set("0")
        self.memory = 0
        self.history = []
        self.current_mode = "standard"
        
        # Currency data
        self.exchange_rates = {}
        self.currency_symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'CAD': 'C$',
            'AUD': 'A$', 'CHF': 'Fr', 'CNY': '¥', 'INR': '₹', 'KRW': '₩'
        }
        
        # Load exchange rates
        self.load_exchange_rates()
        
        # Create GUI
        self.create_widgets()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def load_exchange_rates(self):
        """Load exchange rates from API"""
        def fetch_rates():
            try:
                # Using a free API for exchange rates
                response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.exchange_rates = data['rates']
                    self.exchange_rates['USD'] = 1.0  # Base currency
                    print("Exchange rates loaded successfully")
                else:
                    raise Exception("API request failed")
            except Exception as e:
                print(f"Failed to load exchange rates: {e}")
                # Fallback rates
                self.exchange_rates = {
                    'USD': 1.0, 'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0,
                    'CAD': 1.25, 'AUD': 1.35, 'CHF': 0.92, 'CNY': 6.45,
                    'INR': 74.5, 'KRW': 1180.0
                }
        
        # Load rates in background
        thread = threading.Thread(target=fetch_rates)
        thread.daemon = True
        thread.start()
    
    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Display.TLabel', 
                       background='#2d2d2d', 
                       foreground='white', 
                       font=('Arial', 24, 'bold'),
                       anchor='e')
        
        style.configure('Mode.TButton',
                       background='#4a4a4a',
                       foreground='white',
                       font=('Arial', 10))
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Mode selection
        mode_frame = tk.Frame(main_frame, bg='#1a1a1a')
        mode_frame.pack(fill='x', pady=(0, 10))
        
        modes = [("Standard", "standard"), ("Scientific", "scientific"), ("Currency", "currency")]
        for text, mode in modes:
            btn = tk.Button(mode_frame, text=text, 
                          command=lambda m=mode: self.switch_mode(m),
                          bg='#4a4a4a' if mode != self.current_mode else '#007acc',
                          fg='white', font=('Arial', 10, 'bold'),
                          relief='flat', padx=15, pady=5)
            btn.pack(side='left', padx=2)
        
        # Display
        display_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='sunken', bd=2)
        display_frame.pack(fill='x', pady=(0, 15))
        
        self.display = tk.Label(display_frame, textvariable=self.current_input,
                               bg='#2d2d2d', fg='white', font=('Arial', 24, 'bold'),
                               anchor='e', padx=10, pady=15)
        self.display.pack(fill='both')
        
        # History display (small)
        self.history_label = tk.Label(main_frame, text="", bg='#1a1a1a', fg='#888',
                                     font=('Arial', 10), anchor='e')
        self.history_label.pack(fill='x', pady=(0, 10))
        
        # Button frame
        self.button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.button_frame.pack(fill='both', expand=True)
        
        # Create buttons based on mode
        self.create_buttons()
    
    def create_buttons(self):
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        if self.current_mode == "standard":
            self.create_standard_buttons()
        elif self.current_mode == "scientific":
            self.create_scientific_buttons()
        elif self.current_mode == "currency":
            self.create_currency_buttons()
    
    def create_standard_buttons(self):
        # Button configuration
        btn_config = {
            'font': ('Arial', 12, 'bold'),
            'relief': 'flat',
            'bd': 1,
            'padx': 5,
            'pady': 5
        }
        
        # Button colors
        number_color = '#4a4a4a'
        operator_color = '#007acc'
        special_color = '#ff6b35'
        
        buttons = [
            ('C', 0, 0, special_color, self.clear),
            ('±', 0, 1, special_color, self.toggle_sign),
            ('%', 0, 2, operator_color, lambda: self.append_operator('%')),
            ('÷', 0, 3, operator_color, lambda: self.append_operator('/')),
            
            ('7', 1, 0, number_color, lambda: self.append_number('7')),
            ('8', 1, 1, number_color, lambda: self.append_number('8')),
            ('9', 1, 2, number_color, lambda: self.append_number('9')),
            ('×', 1, 3, operator_color, lambda: self.append_operator('*')),
            
            ('4', 2, 0, number_color, lambda: self.append_number('4')),
            ('5', 2, 1, number_color, lambda: self.append_number('5')),
            ('6', 2, 2, number_color, lambda: self.append_number('6')),
            ('−', 2, 3, operator_color, lambda: self.append_operator('-')),
            
            ('1', 3, 0, number_color, lambda: self.append_number('1')),
            ('2', 3, 1, number_color, lambda: self.append_number('2')),
            ('3', 3, 2, number_color, lambda: self.append_number('3')),
            ('+', 3, 3, operator_color, lambda: self.append_operator('+')),
            
            ('0', 4, 0, number_color, lambda: self.append_number('0')),
            ('.', 4, 1, number_color, lambda: self.append_number('.')),
            ('⌫', 4, 2, special_color, self.backspace),
            ('=', 4, 3, operator_color, self.calculate)
        ]
        
        for text, row, col, color, command in buttons:
            btn = tk.Button(self.button_frame, text=text, command=command,
                          bg=color, fg='white', **btn_config)
            btn.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
        
        # Configure grid weights
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
    
    def create_scientific_buttons(self):
        btn_config = {
            'font': ('Arial', 10, 'bold'),
            'relief': 'flat',
            'bd': 1,
            'padx': 2,
            'pady': 2
        }
        
        number_color = '#4a4a4a'
        operator_color = '#007acc'
        special_color = '#ff6b35'
        scientific_color = '#8b4a8b'
        
        buttons = [
            ('sin', 0, 0, scientific_color, lambda: self.scientific_function('sin')),
            ('cos', 0, 1, scientific_color, lambda: self.scientific_function('cos')),
            ('tan', 0, 2, scientific_color, lambda: self.scientific_function('tan')),
            ('log', 0, 3, scientific_color, lambda: self.scientific_function('log')),
            ('ln', 0, 4, scientific_color, lambda: self.scientific_function('ln')),
            ('C', 0, 5, special_color, self.clear),
            
            ('x²', 1, 0, scientific_color, lambda: self.scientific_function('square')),
            ('x³', 1, 1, scientific_color, lambda: self.scientific_function('cube')),
            ('√', 1, 2, scientific_color, lambda: self.scientific_function('sqrt')),
            ('∛', 1, 3, scientific_color, lambda: self.scientific_function('cbrt')),
            ('xʸ', 1, 4, scientific_color, lambda: self.append_operator('**')),
            ('÷', 1, 5, operator_color, lambda: self.append_operator('/')),
            
            ('7', 2, 0, number_color, lambda: self.append_number('7')),
            ('8', 2, 1, number_color, lambda: self.append_number('8')),
            ('9', 2, 2, number_color, lambda: self.append_number('9')),
            ('(', 2, 3, operator_color, lambda: self.append_operator('(')),
            (')', 2, 4, operator_color, lambda: self.append_operator(')')),
            ('×', 2, 5, operator_color, lambda: self.append_operator('*')),
            
            ('4', 3, 0, number_color, lambda: self.append_number('4')),
            ('5', 3, 1, number_color, lambda: self.append_number('5')),
            ('6', 3, 2, number_color, lambda: self.append_number('6')),
            ('π', 3, 3, scientific_color, lambda: self.append_constant('π')),
            ('e', 3, 4, scientific_color, lambda: self.append_constant('e')),
            ('−', 3, 5, operator_color, lambda: self.append_operator('-')),
            
            ('1', 4, 0, number_color, lambda: self.append_number('1')),
            ('2', 4, 1, number_color, lambda: self.append_number('2')),
            ('3', 4, 2, number_color, lambda: self.append_number('3')),
            ('±', 4, 3, special_color, self.toggle_sign),
            ('%', 4, 4, operator_color, lambda: self.append_operator('%')),
            ('+', 4, 5, operator_color, lambda: self.append_operator('+')),
            
            ('0', 5, 0, number_color, lambda: self.append_number('0')),
            ('.', 5, 1, number_color, lambda: self.append_number('.')),
            ('⌫', 5, 2, special_color, self.backspace),
            ('=', 5, 3, operator_color, self.calculate)
        ]
        
        for text, row, col, color, command in buttons:
            btn = tk.Button(self.button_frame, text=text, command=command,
                          bg=color, fg='white', **btn_config)
            btn.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
        
        # Configure grid weights
        for i in range(6):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.button_frame.grid_columnconfigure(i, weight=1)
    
    def create_currency_buttons(self):
        # Currency input frame
        currency_frame = tk.Frame(self.button_frame, bg='#1a1a1a')
        currency_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(currency_frame, text="Amount:", bg='#1a1a1a', fg='white',
                font=('Arial', 12)).pack(side='left', padx=5)
        
        self.amount_entry = tk.Entry(currency_frame, font=('Arial', 12), width=15,
                                   bg='#2d2d2d', fg='white', insertbackground='white')
        self.amount_entry.pack(side='left', padx=5)
        
        # Currency selection
        currency_select_frame = tk.Frame(self.button_frame, bg='#1a1a1a')
        currency_select_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(currency_select_frame, text="From:", bg='#1a1a1a', fg='white',
                font=('Arial', 12)).pack(side='left', padx=5)
        
        self.from_currency = ttk.Combobox(currency_select_frame, values=list(self.currency_symbols.keys()),
                                        width=8, font=('Arial', 11))
        self.from_currency.set('USD')
        self.from_currency.pack(side='left', padx=5)
        
        tk.Label(currency_select_frame, text="To:", bg='#1a1a1a', fg='white',
                font=('Arial', 12)).pack(side='left', padx=10)
        
        self.to_currency = ttk.Combobox(currency_select_frame, values=list(self.currency_symbols.keys()),
                                      width=8, font=('Arial', 11))
        self.to_currency.set('EUR')
        self.to_currency.pack(side='left', padx=5)
        
        # Convert button
        convert_btn = tk.Button(currency_select_frame, text="Convert", command=self.convert_currency,
                              bg='#007acc', fg='white', font=('Arial', 12, 'bold'),
                              relief='flat', padx=20, pady=5)
        convert_btn.pack(side='left', padx=20)
        
        # Quick conversion buttons
        quick_frame = tk.Frame(self.button_frame, bg='#1a1a1a')
        quick_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(quick_frame, text="Quick Convert:", bg='#1a1a1a', fg='white',
                font=('Arial', 12, 'bold')).pack(anchor='w', pady=5)
        
        quick_conversions = [
            ('USD → EUR', 'USD', 'EUR'),
            ('EUR → USD', 'EUR', 'USD'),
            ('USD → GBP', 'USD', 'GBP'),
            ('GBP → USD', 'GBP', 'USD'),
            ('USD → JPY', 'USD', 'JPY'),
            ('JPY → USD', 'JPY', 'USD')
        ]
        
        for i, (text, from_curr, to_curr) in enumerate(quick_conversions):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(quick_frame, text=text,
                          command=lambda f=from_curr, t=to_curr: self.quick_convert(f, t),
                          bg='#4a4a4a', fg='white', font=('Arial', 10),
                          relief='flat', padx=10, pady=5)
            btn.grid(row=row, column=col, sticky='ew', padx=2, pady=2)
        
        # Configure grid weights for quick conversion buttons
        for i in range(3):
            quick_frame.grid_columnconfigure(i, weight=1)
        
        # Exchange rates display
        rates_frame = tk.Frame(self.button_frame, bg='#1a1a1a')
        rates_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        tk.Label(rates_frame, text="Current Exchange Rates (USD base):", 
                bg='#1a1a1a', fg='white', font=('Arial', 12, 'bold')).pack(anchor='w')
        
        self.rates_text = tk.Text(rates_frame, height=8, bg='#2d2d2d', fg='white',
                                 font=('Arial', 10), relief='flat')
        self.rates_text.pack(fill='both', expand=True, pady=5)
        
        self.update_rates_display()
    
    def switch_mode(self, mode):
        self.current_mode = mode
        self.clear()
        self.create_buttons()
        
        # Update mode button colors
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for frame in widget.winfo_children():
                    if isinstance(frame, tk.Frame):
                        for btn in frame.winfo_children():
                            if isinstance(btn, tk.Button) and btn.cget('text') in ['Standard', 'Scientific', 'Currency']:
                                if btn.cget('text').lower() == mode:
                                    btn.configure(bg='#007acc')
                                else:
                                    btn.configure(bg='#4a4a4a')
    
    def append_number(self, number):
        current = self.current_input.get()
        if current == "0" and number != ".":
            self.current_input.set(number)
        else:
            self.current_input.set(current + number)
    
    def append_operator(self, operator):
        current = self.current_input.get()
        if current and current[-1] not in "+-*/%**":
            self.current_input.set(current + operator)
    
    def append_constant(self, constant):
        current = self.current_input.get()
        if current == "0":
            if constant == 'π':
                self.current_input.set(str(math.pi))
            elif constant == 'e':
                self.current_input.set(str(math.e))
        else:
            if constant == 'π':
                self.current_input.set(current + str(math.pi))
            elif constant == 'e':
                self.current_input.set(current + str(math.e))
    
    def scientific_function(self, func):
        try:
            current = self.current_input.get()
            if current == "0" or current == "":
                return
            
            value = float(current)
            
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'sqrt':
                result = math.sqrt(value)
            elif func == 'cbrt':
                result = value ** (1/3)
            elif func == 'square':
                result = value ** 2
            elif func == 'cube':
                result = value ** 3
            
            self.current_input.set(str(result))
            self.add_to_history(f"{func}({current}) = {result}")
            
        except Exception as e:
            self.current_input.set("Error")
    
    def clear(self):
        self.current_input.set("0")
        self.history_label.config(text="")
    
    def backspace(self):
        current = self.current_input.get()
        if len(current) > 1:
            self.current_input.set(current[:-1])
        else:
            self.current_input.set("0")
    
    def toggle_sign(self):
        current = self.current_input.get()
        if current.startswith('-'):
            self.current_input.set(current[1:])
        else:
            self.current_input.set('-' + current)
    
    def calculate(self):
        try:
            expression = self.current_input.get()
            # Replace display symbols with Python operators
            expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
            
            result = eval(expression)
            self.current_input.set(str(result))
            self.add_to_history(f"{expression} = {result}")
            
        except Exception as e:
            self.current_input.set("Error")
    
    def add_to_history(self, calculation):
        self.history.append(calculation)
        if len(self.history) > 3:
            self.history.pop(0)
        self.history_label.config(text=" | ".join(self.history[-2:]))
    
    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            
            if from_curr not in self.exchange_rates or to_curr not in self.exchange_rates:
                messagebox.showerror("Error", "Currency not found in exchange rates")
                return
            
            # Convert to USD first, then to target currency
            usd_amount = amount / self.exchange_rates[from_curr]
            result = usd_amount * self.exchange_rates[to_curr]
            
            from_symbol = self.currency_symbols.get(from_curr, from_curr)
            to_symbol = self.currency_symbols.get(to_curr, to_curr)
            
            self.current_input.set(f"{result:.2f}")
            self.add_to_history(f"{from_symbol}{amount} → {to_symbol}{result:.2f}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    def quick_convert(self, from_curr, to_curr):
        self.from_currency.set(from_curr)
        self.to_currency.set(to_curr)
        if self.amount_entry.get():
            self.convert_currency()
    
    def update_rates_display(self):
        if not self.exchange_rates:
            return
        
        rates_text = ""
        for currency in ['EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'INR']:
            if currency in self.exchange_rates:
                symbol = self.currency_symbols.get(currency, currency)
                rate = self.exchange_rates[currency]
                rates_text += f"1 USD = {symbol}{rate:.4f}\n"
        
        self.rates_text.delete('1.0', tk.END)
        self.rates_text.insert('1.0', rates_text)
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        if key.isdigit():
            self.append_number(key)
        elif key == '.':
            self.append_number('.')
        elif key == '+':
            self.append_operator('+')
        elif key == '-':
            self.append_operator('-')
        elif key == '*':
            self.append_operator('*')
        elif key == '/':
            self.append_operator('/')
        elif key == '%':
            self.append_operator('%')
        elif key == '=':
            self.calculate()
        elif event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Escape':
            self.clear()

def main():
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
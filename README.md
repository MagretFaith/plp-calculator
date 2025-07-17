Advanced Calculator Pro

A feature-rich Python-based desktop calculator with Standard, Scientific, and Currency conversion modes. Built with `tkinter` for a responsive GUI, background exchange-rate fetching, and history tracking.

Features

Standard Mode: Basic arithmetic (addition, subtraction, multiplication, division, percentage, sign toggle, backspace).
Scientific Mode: Trigonometric functions (sin, cos, tan), logarithms (log10, ln), powers (square, cube, exponentiation), roots (square root, cube root), constants (π, e).
Currency Mode: Real-time currency conversion using `exchangerate-api.com` with automatic fallback rates, quick-conversion presets, and live rate display.
Keyboard Support: Use number keys, `+`, `-`, `*`, `/`, `%`, `Enter` to calculate, `Backspace` to delete, `Esc` to clear.
Calculation History: Shows the last two operations for quick reference.
Threaded API Calls: Exchange rates load in the background to keep the UI responsive.

Installation

1.Clone the repository

git clone https://github.com/MagretFaith/plp-calculator.git
cd plp-calculator

2.Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3.Install dependencies

pip install -r requirements.txt

> Note: If `requests` is not in your requirements, you can add it:

pip install requests

Usage

Run the application:

python calculator.py

Switch between modes using the top buttons.
Enter numbers and operators with your mouse or keyboard.
In Currency Mode, enter an amount, select currencies, and click Convert.

Configuration

No API key is required for `https://api.exchangerate-api.com/v4/latest/USD`. If you prefer another service:

1. Modify `load_exchange_rates()` in `calculator.py`.
2. Replace the URL and parsing logic with your chosen provider.

Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature-name"`).
4. Push to the branch (`git push origin feature-name`).
5. Submit a pull request.

Please follow PEP8 style guidelines and include tests for new features.

License

Distributed under the MIT License. See `LICENSE` for details.

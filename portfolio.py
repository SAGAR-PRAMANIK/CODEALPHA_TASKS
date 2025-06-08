import yfinance as yf
from datetime import datetime

class StockPortfolio:
    def __init__(self):  # Fixed constructor
        self.stocks = {}

    def add_stock(self, ticker, quantity):
        if ticker in self.stocks:
            self.stocks[ticker]['quantity'] += quantity
        else:
            self.stocks[ticker] = {'quantity': quantity, 'purchase_date': datetime.now().strftime("%Y-%m-%d")}

    def remove_stock(self, ticker, quantity):
        if ticker in self.stocks:
            if self.stocks[ticker]['quantity'] >= quantity:
                self.stocks[ticker]['quantity'] -= quantity
                if self.stocks[ticker]['quantity'] == 0:
                    del self.stocks[ticker]
            else:
                print("You don't have enough shares to sell.")
        else:
            print("You don't own any shares of this stock.")

    def get_stock_price(self, ticker):
        try:
            stock_data = yf.Ticker(ticker)
            price = stock_data.info.get('currentPrice')
            if price is None:
                print(f"Price not available for {ticker}.")
            return price
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_portfolio_value(self):
        total_value = 0
        for ticker, stock_info in self.stocks.items():
            price = self.get_stock_price(ticker)
            if price is not None:
                total_value += price * stock_info['quantity']
        return total_value

    def print_portfolio(self):
        print("Stock Portfolio:")
        for ticker, stock_info in self.stocks.items():
            price = self.get_stock_price(ticker)
            if price is not None:
                print(f"{ticker}: {stock_info['quantity']} shares, Purchase Date: {stock_info['purchase_date']}, Current Price: ${price:.2f}, Value: ${price * stock_info['quantity']:.2f}")
            else:
                print(f"{ticker}: {stock_info['quantity']} shares, Purchase Date: {stock_info['purchase_date']}, Current Price: N/A, Value: N/A")
        print(f"Total Portfolio Value: ${self.get_portfolio_value():.2f}")

def add_stock(portfolio):
    ticker = input("Enter stock ticker: ")
    quantity = int(input("Enter quantity: "))
    portfolio.add_stock(ticker, quantity)

def remove_stock(portfolio):
    ticker = input("Enter stock ticker: ")
    quantity = int(input("Enter quantity: "))
    portfolio.remove_stock(ticker, quantity)

def print_portfolio(portfolio):
    portfolio.print_portfolio()

def main():
    portfolio = StockPortfolio()
    while True:
        print("\n1. Add Stock")
        print("2. Remove Stock")
        print("3. Print Portfolio")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_stock(portfolio)
        elif choice == "2":
            remove_stock(portfolio)
        elif choice == "3":
            print_portfolio(portfolio)
        elif choice == "4":
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()

# Sample data for testing
portfolio = StockPortfolio()
portfolio.add_stock("AAPL", 5)
portfolio.stocks["AAPL"]["purchase_date"] = "2025-06-07"  # Manually setting purchase date for testing
portfolio.print_portfolio()
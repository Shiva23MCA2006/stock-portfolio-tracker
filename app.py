from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# Initialize the portfolio (in a real-world app, this would be saved in a database)
portfolio = []

# Alpha Vantage API key
API_KEY = 'iPPPGsgYVnJ5pII6v7qwRFzzdaTiArVH'

# Function to get stock data
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (5min)" in data:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        latest_close = data['Time Series (5min)'][last_refreshed]['4. close']
        return latest_close
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html', portfolio=portfolio)

@app.route('/add', methods=['POST'])
def add_stock():
    symbol = request.form.get('symbol')
    stock_price = get_stock_data(symbol)
    
    if stock_price:
        portfolio.append({'symbol': symbol, 'price': stock_price})
    
    return redirect('/')

@app.route('/remove', methods=['POST'])
def remove_stock():
    symbol = request.form.get('symbol')
    portfolio[:] = [stock for stock in portfolio if stock['symbol'] != symbol]
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
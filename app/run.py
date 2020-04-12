from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
import yfinance as yf
import json

# msft = yf.Ticker("MSFT")

nasdaq = []
with open('exchanges/NASDAQ.json') as f:
  nasdaq = json.load(f)

nyse = []
with open('exchanges/NYSE.json') as f:
  nyse = json.load(f)



app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Dashboard(Resource):
	def get(self):
		view = {
			'exchanges': [
				{
					'name' : 'NASDAQ', 
					'data' : nasdaq
				},
				{
					'name' : 'NYSE', 
					'data' : nyse
				}
			]
		}

		return view

class Stock(Resource):
	def get(self, symbol):
		ticker = yf.Ticker(symbol)
		# use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
		hist = ticker.history(period="ytd")
		return hist.to_json()

class NASDAQ(Resource):
    def get(self):
        return nasdaq

class NASDAQ_SYMBOLS(Resource):
	def get(self):
		symbols = []
		for x in nasdaq:
			s = x['Symbol']
			symbols.append(s)

		return symbols

class NYSE(Resource):
    def get(self):
        return nyse


# class ms(Resource):
#     def get(self):
#         return msft.info

api.add_resource(HelloWorld, '/')
# api.add_resource(ms, '/ms')
api.add_resource(NASDAQ, '/nasdaq')
# api.add_resource(NASDAQ_SYMBOLS, '/nasdaq/symbols')
api.add_resource(Dashboard, '/api/dashboard')
api.add_resource(Stock, '/api/stock/<symbol>')

@app.route('/home')
def index():
    return render_template('index.html', title='Home',)

if __name__ == '__main__':
    app.run(debug=True)
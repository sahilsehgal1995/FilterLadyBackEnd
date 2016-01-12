from flask import Flask
import Buyer, Dealer, Brand, Product
app = Flask(__name__)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
def home():
  return "hello world"

Buyer.add_routes(app)
Dealer.add_routes(app)
Brand.add_routes(app)
Product.add_routes(app)

if __name__ == "__main__":
  app.run()
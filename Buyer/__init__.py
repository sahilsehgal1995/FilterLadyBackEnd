from flask import Blueprint, session

def add_routes(app=None):
  Buyer = Blueprint('Buyer', __name__, static_url_path='/Buyer/static', static_folder='./static', template_folder='./templates')
  
  @Buyer.route('/api/Buyer')
  def home():
    return 'Buyer page'
  
  app.register_blueprint(Buyer)
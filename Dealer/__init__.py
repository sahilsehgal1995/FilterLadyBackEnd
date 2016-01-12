from flask import Blueprint, session

def add_routes(app=None):
  Dealer = Blueprint('Dealer', __name__, static_url_path='/Dealer/static', static_folder='./static', template_folder='./templates')
  
  @Dealer.route('/api/Dealer')
  def home():
    try:
      return 'Dealer'
    except Exception as e:
      return str(e)
  
  app.register_blueprint(Dealer)
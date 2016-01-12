from flask import Blueprint, session

def add_routes(app=None):
  Brand = Blueprint('Brand', __name__, static_url_path='/Brand/static', static_folder='./static', template_folder='./templates')
  
  @Brand.route('/api/Brand')
  def home():
    return 'Brand page'
  
  app.register_blueprint(Brand)
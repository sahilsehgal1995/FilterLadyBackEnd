from flask import Blueprint, session

def add_routes(app=None):
  Product = Blueprint('Product', __name__, static_url_path='/Product/static', static_folder='./static', template_folder='./templates')
  
  @Product.route('/api/Product')
  def owner():
    return 'Product page'
  
  app.register_blueprint(Product)
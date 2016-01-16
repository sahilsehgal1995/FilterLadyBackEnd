from flask import Blueprint, session, url_for, request
from database import register, getpath, updateSummaryProfile, Login, register, updateDetailProfile, getDetailProfile
import json, gc

base = 'http://www.filterlady.com/'

def allowed_file(filename):
  return filename.rsplit('.', 1)[-1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'bmp']

def add_routes(app=None):
  Dealer = Blueprint('Dealer', __name__, static_url_path='/Dealer/static', static_folder='./static', template_folder='./templates')
  
  @Dealer.route('/api/Dealer')
  def home():
    try:
      return getpath('D_1')
    except Exception as e:
      return str(e)
  
  @Dealer.route('/api/Dealer/login', methods=['GET', 'POST'])
  def Login():
    if request.method == 'POST':
      reply = Login(user)
      if not str(reply) == 'Invalid Credentials' and not str(reply) == 'Unable to Process':
	session['_id']= reply['_id']
	return json.dumps(reply)
      return 'Authentication Failed'
    return 'Invalid Request'
    
  @Dealer.route('/api/Dealer/logout', methods=['GET', 'POST'])
  def Logout():
    session.clear()
    gc.collect()
    return 'Logged out Successfully'
  
  @Dealer.route('/api/Dealer/Details', methods=['GET', 'POST'])
  def getProfileDetails():
    if session['_id'] == jon.loads(request.args.get('user'))['_id']:
      if request.method == 'GET':
	return str(getDetailProfile(session['_id'],request.args.get('DetailType')))
      elif request.method == 'POST':
	return updateDetailProfile(session['_id'],request.args.get('DetailType'))
    return 'Authentication Failed'
  
  @Dealer.route('/api/Dealer/Signup', methods=['GET', 'POST'])
  def Signup():
    try:
      if request.method == 'POSt':
	return register(request.args.get('Dealer'))
      return "Invalid Request"
    except Exception as e:
      print str(e)
      return 'Unable to Register'
  
  @Dealer.route('/api/Dealer/uploadpic', methods=['GET', 'POST'])
  def uploadPic():
    try:
      file = request.files['file']
      if allowed_file(file.filename):
	fileExtension = file.filename.rsplit('.', 1)[-1].lower()
	if request.args.get('type') == 'ProfilePic':
	  path = getpath('D_1')
	  file.save(os.path.join(path, 'ProfilePic'+ fileExtension))
	  updateSummaryProfile('D_1','ProfilePic',base+'Dealer/static/'+'D_1'+'/img/ProfilePic'+fileExtension)
	  return 'Uploaded'
	elif request.args.get('type') == 'CoverPic':
	  path = getpath('D_1')
	  file.save(os.path.join(path, 'CoverPic'+ fileExtension))
	  updateSummaryProfile('D_1','CoverPic',base+'Dealer/static/'+'D_1'+'/img/CoverPic'+fileExtension)
	  return 'Uploaded'
      return 'Unable to Upload'
    except Exception as e:
      return str(e)
  
  app.register_blueprint(Dealer)
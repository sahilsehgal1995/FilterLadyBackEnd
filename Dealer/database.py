import pymongo
from passlib.hash import sha256_crypt
import json
import os
from os import walk
import gc

base='http://www.filterlady.com/'

def MongoDBconnection(database, collection):
  connection = pymongo.MongoClient("mongodb://localhost")
  db = connection[database]
  cursor = db[collection]
  connection.close()
  gc.collect()
  return connection, db, cursor

def register(Dealer):
  connection, db, collection = MongoDBconnection('Dealer','DealerList')
  if collection.find({"Mobile":json.loads(Dealer)['Mobile']}).count():
    return 'Mobile Number already Registered'
  if collection.find({"Email ID":json.loads(Dealer)['Email ID']}).count():
    return 'Email ID already Registered'
  iter = collection.find()
  Dealer = json.loads(Dealer)
  Dealer['_id']= 'D_'+str(int(iter[iter.count()-1]['_id'].split("_")[1])+1)
  Dealer['Password'] = sha256_crypt.encrypt(str(Dealer['Password']))
  collection.insert_one(Dealer)
  connection.close()
  gc.collect()
  return "Registerd"

def Login(user):
  try:
    connection, db, collection = MongoDBconnection('Dealer','DealerList')
    if collection.find({"Mobile":json.loads(user)['Mobile']}).count():
      reply = collection.find({"Mobile":json.loads(user)['Mobile']})[0]
      if sha256_crypt.verify(json.loads(user)['Password'],reply['Password']):
	del reply['Password'], reply['_id']
	connection.close()
	gc.collect()
	return json.dumps(reply)
      return 'Invalid Credentials'
    if collection.find({"Email ID":json.loads(user)['Email ID']}).count():
      reply = collection.find({"Email ID":json.loads(user)['Email ID']})[0]
      if sha256_crypt.verify(json.loads(user)['Password'],reply['Password']):
	del reply['Password'], reply['_id']
	connection.close()
	return reply
    connection.close()
    gc.collect()
    return 'Invalid Credentials'
  except Exception as e:
    print str(e)
    return 'Unable to Process'

def getSummaryProfile(user):
  connection, db, collection = MongoDBconnection('Dealer','DealerList')
  reply = collection.find({"_id":user})[0]
  del reply['Password'], reply['_id']
  connection.close()
  gc.collect()
  return json.dumps(reply)

def updateSummaryProfile(user,key,value):
  connection, db, collection = MongoDBconnection('Dealer','DealerList')
  collection.update({"_id":user},{"$set":{key:value}})
  connection.close()
  gc.collect()
  return 'Updated'

def updateDetailProfile(user, details):
  try:
    connection, db, collection = MongoDBconnection('Dealer',user)
    collection.save(json.loads(details))
    if json.loads(details)['_id'] == 'Contact Details':
      details = json.loads(details)
      db['DealerList'].update({"_id":user},{"$set":{"Owner Name":details['Owner Name'], "Mobile":details['Mobile'], "Company Name":details['Company Name'], "Email ID":details['Email ID']}})
    connection.close()
    gc.collect()
    return "Profile Updated"
  except Exception as e:
    print str(e)
    return 'Unable to update'

def getDetailProfile(user, details):
  try:
    connection, db, collection = MongoDBconnection('Dealer',user)
    connection.close()
    gc.collect()
    return json.dumps(collection.find({"_id":details})[0])
  except Exception as e:
    print str(e)
    return "Unable to Fetch"

def getpath(user):
  if not os.path.exists(os.getcwd() + '/Dealer/static/Dealers/'+user+'/img/'):
    os.makedirs(os.getcwd()+'/Dealer/static/Dealers/'+user+'/img/')
  return os.getcwd()+'/Dealer/static/Dealers/'+user+'/img/'
  
def allowed_file(filename):
  return filename.rsplit('.', 1)[-1].lower() in ['png', 'jpg', 'jpeg', 'gif', 'bmp']

  
if __name__ == "__main__":
  #print register('{ "_id" : "D_1", "Password" : "$5$rounds=80000$B0fN02TPtA/1PoGr$DCe/dG.ce1rT00moXuluCsjbI1D55/18I8nocdMd2yA", "Owner Name" : "Girish Ahirwar", "Mobile" : "9780008628", "Company Name" : "FilterLady", "Email ID" : "sahilsehgal1995@gmail.com"}')
  #print Login('{"Email ID":"sahilssehgal1995@gmail.com", "Mobile":"9780008628", "Password":"12345"}')
  #print updateProfile('D_1', '{"_id":"Company Details", "Brands":[{"B_1":"Asian","B_2":"Nerolac"}], "Main Product Category": ["Hardware", "Sanitary Taps", "Electricals"], "Address":"", "City":"Jaipur"}')
  #print updateProfile('D_1','{"_id":"Product Catalouge","Products":[{"P_1":["Persian Tiles","http://www.filterlady.com/static/img.png"]},{"P_2":["Persian Tiles","http://www.filterlady.com/static/img.png"]}]}')
  #print updateProfile('D_1','{"_id":"Awards","Awards":[{"Name":"ABC Award","Date":"30/07/2015","About":"Won last year","Photo":"http://www.filterlady.com/user/img/image.jpg"}, {"Name":"XYQ Award","Date":"30/07/2015","About":"Won last year","Photo":"http://www.filterlady.com/user/img/image.jpg"}]}')
  #print updateDetailProfile('D_1','{"_id":"Contact Details", "Owner Name":"Girish Ahirwar", "Company Name":"FilterLady", "Mobile":"9780008628","Email ID":"sahilsehgal1995@gmail.com"}')
  #print getDetailProfile('D_1', 'Product Catalouge')
  print getSummaryProfile('D_1')
  
  

import os 
import json 

import werkzeug

# -Some Globals-----------------------------------------
curPath = os.path.dirname(os.path.abspath(__file__))

if os.environ.get("DATADIR"):
  curPath = os.environ.get("DATADIR")
  if not os.path.isdir(curPath):
    os.makedirs(curPath)

userDataFileName = "users.json"
userDataFilePath = os.path.join(curPath, userDataFileName)
idKey = "email"
pwdMinLength = 6
pwdDictKey = "pwd_hash"

dataDefi = {
  "email": {
    "type": str,
    "len": 0,
    "required": True,
    "unique": True
  },
  "firstname": {
    "type": str,
    "len": 0,
    "required": False,
    "unique": False
  },
  "lastname": {
    "type": str,
    "len": 0,
    "required": True,
    "unique": False
  },
  "address": {
    "type": str,
    "len": 0,
    "required": False,
    "unique": False
  },
  "zip": {
    "type": int,
    "len": 5,
    "required": False,
    "unique": False
  },
  "company": {
    "type": str,
    "len": 0,
    "required": True,
    "unique": False
  }
}


# -Some Helpers-----------------------------------------
def check_user_data_file():
  create = False
  if not os.path.isfile(userDataFilePath):
    create = True

  else:
    with open(userDataFilePath, "r") as flObj:
      try: 
        dataIn = json.loads(flObj.read())
      except Exception as e:
        print(e)
        create = True

  if create:
    with open(userDataFilePath, "w") as flObj:
      flObj.write(json.dumps([], indent=2))
    return []
  else:
    return dataIn

# ---------------------------------
def get_list_of_ids():
  dataIn = check_user_data_file()
  resList = []
  for item in dataIn:
    resList.append(item[idKey])

  return resList

# ---------------------------------
def write_user_data_to_file(data):
  with open(userDataFilePath, "w") as flObj:
    flObj.write(json.dumps(data, indent=2))


#-The Methods------------------------------------------
def get_users():
  dataIn = check_user_data_file()
  for idx in range(len(dataIn)):
    if pwdDictKey in dataIn[idx]:
      del dataIn[idx][pwdDictKey]
  return dataIn

#---------------------------------
def get_user_by_id(id:str):
  idList = get_list_of_ids()
  if id not in idList:
    raise Exception("user with id: '%s' does not exist" %id)

  dataIn = check_user_data_file()
  for item in dataIn:
    if id == item[idKey]:
      break

  return item

#---------------------------------
def add_user(data:dict):

  for key in dataDefi.keys():
    if dataDefi[key]["required"] and key not in data:
      raise Exception("Key '%s' is missing/required" %key)

  for key,val in data.items():
    if key not in dataDefi.keys():
      raise Exception("Invalid key: '%s'" %key)
    if type(val) != dataDefi[key]["type"]:
      raise Exception("Invalid format for key: '%s'" %key)
    if dataDefi[key]["len"] and len(str(val))!= dataDefi[key]["len"]:
      raise Exception("Invalid length for key: '%s'" %key)
  
  if data[idKey] in get_list_of_ids():
    raise Exception("user with id: '%s' already exists." %data[idKey])

  usersData = get_users()
  usersData.append(data)

  write_user_data_to_file(usersData)

#---------------------------------
def delete_user_by_id(id):
  idList = get_list_of_ids()
  if id not in idList:
    raise Exception("user with id: '%s' does not exist" %id)

  idx = idList.index(id)
  usersData = get_users()
  del usersData[idx]
  write_user_data_to_file(usersData)

#---------------------------------
def change_user_data_by_id(id, data):
  idList = get_list_of_ids()
  if id not in idList:
    raise Exception("user with id: '%s' does not exist" %id)

  idx = idList.index(id)
  usersData = get_users()

  for key,val in data.items():
    if key not in dataDefi.keys():
      raise Exception("Invalid key: '%s'" %key)
    if type(val) != dataDefi[key]["type"]:
      raise Exception("Invalid format for key: '%s'" %key)
    if dataDefi[key]["len"] and len(str(val))!= dataDefi[key]["len"]:
      raise Exception("Invalid length for key: '%s'" %key)
    
    usersData[idx][key] = val 

  write_user_data_to_file(usersData)

#---------------------------------
def set_user_password(id, password:str):
  if len(password) < pwdMinLength:
    raise Exception("Password to short! min '%s' chars" %pwdMinLength)

  idList = get_list_of_ids()
  if id not in idList:
    raise Exception("user with id: '%s' does not exist" %id)

  pwdHash = werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

  idx = idList.index(id)
  usersData = get_users()

  usersData[idx][pwdDictKey] = pwdHash 
  write_user_data_to_file(usersData)
  
#---------------------------------
def check_user_password(id, password:str):
  idList = get_list_of_ids()
  if id not in idList:
    raise Exception("user with id: '%s' does not exist" %id)
  
  idx = idList.index(id)
  usersData = check_user_data_file()
  if pwdDictKey not in usersData[idx]:
    raise Exception("user with id: '%s' has no password set" %id)
  
  pwdCheck = werkzeug.security.check_password_hash(usersData[idx][pwdDictKey], password)
  return pwdCheck

#---------------------------------

#---------------------------------


#------------------------------------------------------
from flask import Flask, request, jsonify
from datetime import datetime

import backend


#--Build the App--------------------------------
app = Flask(__name__)
app.debug = True


#--The HTML Section-----------------------------
@app.route("/", methods=["GET"])
def hello_app():
  return "<h2>Hello from the backend</h2>"


#--The API Section------------------------------
@app.route("/api", methods=["GET"])
def hello_api():
  resObj = {
    "method": request.method,
    "path": request.path,
    "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": 200
  }

  return jsonify(resObj)

#-----------------------------------------------
@app.route("/api/users", methods=["GET"])
def api_users_get():
  resObj = {
    "method": request.method,
    "path": request.path,
    "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": 200
  }

  resObj["data"] = backend.get_users()

  return jsonify(resObj)

#--------------------------------
@app.route("/api/user/<id>", methods=["GET", "DELETE", "PUT"])
def api_user_get_put_delete(id):
  resObj = {
    "method": request.method,
    "path": request.path,
    "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": 200
  }

  #---------------
  if request.method.lower() == "get":
    try:
      resObj["data"] = backend.get_user_by_id(id)
    except Exception as e:
      resObj["status"] = 400
      resObj["message"] = str(e)

  #---------------
  elif request.method.lower() == "delete":
    try:
      resObj["data"] = backend.delete_user_by_id(id)
    except Exception as e:
      resObj["status"] = 400
      resObj["message"] = str(e)

  #---------------
  elif request.method.lower() == "put":
    try:
      data = request.json
      backend.change_user_data_by_id(id, data)
    except Exception as e:
      resObj["status"] = 400
      resObj["message"] = str(e)

  #---------------
  return jsonify(resObj)

#--------------------------------
@app.route("/api/user", methods=["POST"])
def api_user_post():
  resObj = {
    "method": request.method,
    "path": request.path,
    "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": 200
  }

  try:
    data = request.json
    backend.add_user(data=data)
  except Exception as e:
    resObj["status"] = 400
    resObj["message"] = str(e)

  #---------------
  return jsonify(resObj)


#--------------------------------
@app.route("/api/user/pwd", methods=["PUT"])
def api_user_set_pwd_put():
  resObj = {
    "method": request.method,
    "path": request.path,
    "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": 200
  }

  try:
    data = request.json
    data["userid"]
    data["password"]
    backend.set_user_password(id=data["userid"], password=data["password"])
  except Exception as e:
    resObj["status"] = 400
    resObj["message"] = str(e)

  #---------------
  return jsonify(resObj)

#--------------------------------
@app.route("/api/user/pwd", methods=["POST"])
def api_user_check_pwd_post():
  resObj = {
    "method": request.method,
    "path": request.path,
    "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": 200
  }

  try:
    data = request.json
    data["userid"]
    data["password"]
    resObj["data"] = backend.check_user_password(id=data["userid"], password=data["password"])
  except Exception as e:
    resObj["status"] = 400
    resObj["message"] = str(e)

  #---------------
  return jsonify(resObj)

#--------------------------------


#--The App / Dev Server Runner------------------

if __name__ == "__main__":
  app.run(port=5000, host="0.0.0.0")

#-----------------------------------------------

## Code Example - Rest API

**The App ist build in Python Flask**

    Info: Flask(Microframework for Web-development)
    https://flask.palletsprojects.com/en/2.1.x/quickstart/

  
**What does it do**
This App is an example for learning.
After starting the App you can list, add, mod and delete items (in this case fictitious users), e.g. via browser or postman.

**Examples via Browser:**
GET: http://YOUTCOMPUTERSNAME:5000/api/users 
GET: http://YOUTCOMPUTERSNAME:5000/api/user/USERSID

**Examples via Curl:**

    curl --location --request GET 'http://YOUTCOMPUTERSNAME:5000/api/api/user' \
    		--header 'Content-Type: application/json' \
    		--data-raw '{
    			"email": "mr.robot@bcl.de",
    			"firstname": "Eliot",
    			"lastname": "Alderson",
    			"company": "bcl"
    		}'
<br>

### Build and run Docker image
run in root of clones repo folder

    docker build -t example_rest-api:latest .
    
    docker run -d -p 5001:5000 --name ex_app_1 example_rest-api
	docker run -d -p 5001:5000 -e DATADIR="/data" -v /myhome/vol:/data --name ex_app_1 example_rest-api

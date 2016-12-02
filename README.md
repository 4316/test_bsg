REST-auth
=========

RESTful Authentication with Flask on python3

Installation
------------

After cloning, create a virtual environment and install the requirements and create database.

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ make init

Running
-------

To run the server use the following command:

    (venv) $ make run
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Then from a different terminal window you can send requests.

API Documentation
-----------------

- POST **/api/users**

    Register a new user.<br>
    The body must contain a JSON object that defines `email` and `password` fields.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with the newly added user. A `Location` header contains the URI of the new user.<br>
    On failure status code 400 (bad request) is returned.<br>
    Notes:
    - The password is hashed before it is stored in the database. Once hashed, the original password is discarded.
    - In a production deployment secure HTTP must be used to protect the password in transit.

- GET **/api/users/&lt;int:id&gt;**

    Return a user.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with the requested user.<br>
    On failure status code 400 (bad request) is returned.

- GET **/api/token**

    Return an authentication token.<br>
    This request must be authenticated using a HTTP Basic Authentication header.<br>
    On success a JSON object is returned with a field `token` set to the authentication token for the user and a field `duration` set to the (approximate) number of seconds the token is valid.<br>
    On failure status code 401 (unauthorized) is returned.

- GET **/api/resource**

    Return all or limit posts of protected user.<br>
    This request must be authenticated using a HTTP Basic Authentication header. Instead of email and password, the client can provide a valid authentication token in the email field. If using an authentication token the password field is not used and can be set to any value.<br>
    On success a JSON object with data for the authenticated user is returned.<br>
    On failure status code 401 (unauthorized) is returned.

- GET **/api/resource**

Example
-------

The following `curl` command registers a new user with username `some@mail` and password `test`:

    $ curl -i -X POST -H "Content-Type: application/json" -d '{"email":"some@mail","password":"test"}' http://127.0.0.1:5000/api/users
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 23
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 03:32:26 GMT
    
    {
      "email": "some@mail"
    }

Insert new post of user:
    
    $ curl -u some@mail:test -i -X POST -H "Content-Type: application/json" -d '{"title":"header","body":"footer"}' http://127.0.0.1:5000/api/insert
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 60
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 03:48:11 GMT
    
    {"email": "some@mail", "body": "footer", "title": "header"}

    $ curl -u some@mail:test -i -X POST -H "Content-Type: application/json" -d '{"title":"protected","body":"some text"}' http://127.0.0.1:5000/api/insert
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 66
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 03:54:21 GMT
    
    {"email": "some@mail", "body": "some text", "title": "protected"}

And search:

    $ curl -u some@mail:test -i -X POST -H "Content-Type: application/json" -d '{"search":"e"}' http://127.0.0.1:5000/api/search
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 84
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 04:01:21 GMT
    
    {"email": "some@mail", "posts": [{"header": "footer"}, {"protected": "some text"}]}
    
    $ curl -u some@mail:test -i -X POST -H "Content-Type: application/json" -d '{"search":"some"}' http://127.0.0.1:5000/api/search
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 62
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 04:04:20 GMT

    {"email": "some@mail", "posts": [{"protected": "some text"}]}


These credentials can now be used to access protected resources:

    $ curl -u some@mail:test -i -X GET http://127.0.0.1:5000/api/resource
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 84
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 04:02:34 GMT

    {"email": "some@mail", "posts": [{"header": "footer"}, {"protected": "some text"}]}

    $ curl -u some@mail:test -i -X POST -H "Content-Type: application/json" -d '{"start":"0","end":"1"}' http://127.0.0.1:5000/api/resource
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 56
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 04:02:59 GMT

    {"email": "some@mail", "posts": [{"header": "footer"}]}

Using the wrong credentials the request is refused:

    $ curl -u some@mail:python -i -X GET http://127.0.0.1:5000/api/resource
    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: text/html; charset=utf-8
    Content-Length: 19
    WWW-Authenticate: Basic realm="Authentication Required"
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 03:38:30 GMT
    
    Unauthorized Access

Finally, to avoid sending username and password with every request an authentication token can be requested:

    $ curl -u some@mail:test -i -X GET http://127.0.0.1:5000/api/token
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 153
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 03:56:38 GMT
    
    {
      "duration": 600,
      "token": "eyJpYXQiOjE0ODA2NTA5OTgsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDgwNjUxNTk4fQ.eyJpZCI6MX0.udVsu3VS-qZBSflI6Df58qqXB7NSHSdFv-moXRRmW7c"
    }

And now during the token validity period there is no need to send username and password to authenticate anymore:

    $ curl -u eyJpYXQiOjE0ODA2NTA5OTgsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDgwNjUxNTk4fQ.eyJpZCI6MX0.udVsu3VS-qZBSflI6Df58qqXB7NSHSdFv-moXRRmW7c:q -i -X GET http://127.0.0.1:5000/api/resource
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 84
    Server: Werkzeug/0.11.11 Python/3.4.3+
    Date: Fri, 02 Dec 2016 03:57:47 GMT

    {"email": "some@mail", "posts": [{"header": "footer"}, {"protected": "some text"}]}

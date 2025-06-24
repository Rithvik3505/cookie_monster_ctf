from flask import Flask, request, make_response, render_template
import base64
import json

app = Flask(__name__)
FLAG = "layer8{$w33ttr3ats4adm1ns}"

@app.route("/")
def index():
    auth_cookie = request.cookies.get("auth")
    username = "guest"

    if auth_cookie:
        try:
            user_json = base64.b64decode(auth_cookie).decode()
            user = json.loads(user_json).get("user")
            username = user
        except:
            pass

    resp = make_response(render_template("index.html", user=username))
    if not auth_cookie:
        cookie_val = base64.b64encode(json.dumps({"user": "regular"}).encode()).decode()
        resp.set_cookie("auth", cookie_val)
    return resp

@app.route("/flag")
def flag():
    auth_cookie = request.cookies.get("auth")
    if auth_cookie:
        try:
            user_json = base64.b64decode(auth_cookie).decode()
            user = json.loads(user_json).get("user")
            if user == "admin":
                return f"<h1>{FLAG}</h1>"
        except:
            pass
    return "<h1>403 Forbidden</h1><p>You are not admin.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

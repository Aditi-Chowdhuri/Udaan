from flask import Flask, redirect, request, render_template
import time

app=Flask(__name__)
app.secret_key="1234567890"

classes=dict()

@app.route("/book", methods=["POST"])
def book():
    if request.form["name"] not in classes.keys():
        classes[request.form["class"]+" "+request.form["slot"]]={
            "capacity":60,
            "user":list(),
            "wl":list()
        }
    if classes[request.form["class"]+" "+request.form["slot"]]["capacity"]!=0:
        classes[request.form["class"]+" "+request.form["slot"]]["capacity"]-=1
        classes[request.form["class"]+" "+request.form["slot"]]["user"].append(request.form["name"])
    else:
        classes[request.form["class"]+" "+request.form["slot"]]["wl"].append(request.form["name"])
        return render_template("index.html", msg="Waiting list")
    return render_template("index.html", msg="Successful")

@app.route("/cancel", methods=["POST"])
def cancel():
    t=time.localtime()
    ct=float(time.strftime("%H.%M"))
    if float(request.form["slot"].replace("-", "."))-ct > 0.3:
        try:
            classes[request.form["class"]+" "+request.form["slot"]]["user"].remove(request.form["name"])
            try:
                classes[request.form["class"]+" "+request.form["slot"]]["user"].append(classes[request.form["class"]+" "+request.form["slot"]]["wl"][0])
                classes[request.form["class"]+" "+request.form["slot"]]["wl"]=classes[request.form["class"]+" "+request.form["slot"]]["wl"][1:]
            except: 
                classes[request.form["class"]+" "+request.form["slot"]]["capacity"]+=1
        except:
            return render_template("index.html", msg="Not registered")
    else:
        return render_template("index.html", msg="Cancel limit passed")
    return render_template("index.html", msg="Successful")

@app.route("/", methods=["GET"])
def defaul():
    return render_template("index.html")

@app.route("/status", methods=["GET"])
def cl():
    return classes

if __name__=="__main__":
    app.run("0.0.0.0", port=80, debug=True)
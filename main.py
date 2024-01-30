import os

from flask import *
import requests
from smtplib import SMTP

my_gmail = os.environ.get("GMAIL")
my_outlook = os.environ.get("OUTLOOK")
password_gmail = os.environ.get("PASS")

app = Flask(__name__)

response = requests.get(url="https://api.npoint.io/87cab9ee517d276a396a")
response.raise_for_status()
blogs = response.json()


@app.route("/")
def home():
    return render_template("index.html", posts=blogs)


@app.route("/index.html")
def index():
    return render_template("index.html", posts=blogs)


@app.route("/about.html")
def about():
    return render_template("about.html")


def print_data():
    print(request.form["name"])
    print(request.form["email"])
    print(request.form["message"])
    print(request.form["phone"])


@app.route("/contact.html", methods=['POST', 'GET'])
def contact():
    if request.method == 'GET':
        return render_template("contact.html", msg_sent=False)

    if request.method == 'POST':
        print_data()
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_gmail, password=password_gmail)
            connection.sendmail(from_addr=my_gmail,
                                to_addrs=my_outlook,
                                msg=f"Subject:New Message\n\n"
                                    f"Name: {request.form['name']}\n"
                                    f"Email: {request.form['email']}\n"
                                    f"Phone: {request.form['phone']}\n"
                                    f"Message: {request.form['message']}")
        return render_template("contact.html", msg_sent=True)


@app.route("/post.html/<int:b_id>")
def post(b_id):
    blog_post = None
    for blog in blogs:
        if blog["id"] == b_id:
            blog_post = blog
    return render_template("post.html", post=blog_post)


if __name__ == "__main__":
    app.run(debug=True)

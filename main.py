from flask import Flask, render_template, request
from post import Post
import requests
import smtplib

posts = requests.get("https://api.npoint.io/d34f8b8d062de6f61867").json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)

app = Flask(__name__)

MY_EMAIL = "liborhavranek91@gmail.com"
MY_PASSWORD = "guchlmoahntmjntd"
SEND_MAIL = "ctiborekskutr@seznam.cz"

@app.route('/')
def get_index():
    return render_template("index.html", all_posts=post_objects)


@app.route('/contact.html')
def get_contact():
    return render_template("contact.html")


@app.route('/about.html')
def get_about():
    return render_template("about.html")


@app.route('/post.html')
def get_post():
    return render_template("post.html", all_posts=post_objects)


@app.route('/index.html')
def get_index_second():
    return render_template("index.html", all_posts=post_objects)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        send_mail(data["name"], data["email"], data["phone"], data["message"])
        return "<h1>Successfully sent your message</h1>"
    return render_template("contact.html", msg_sent=False)


def send_mail(name,email,phone,message):
    email_mesage = f"Subject:\n Name: {name} \n Email: {email} \n Phone: {phone} \n Message: \n {message}"
    with smtplib.SMTP("smtp.gmail.com", 578) as connect:
        connect.starttls()
        connect.login(MY_EMAIL, MY_PASSWORD)
        connect.sendmail(MY_EMAIL, SEND_MAIL, email_mesage)



if __name__ == "__main__":
    app.run(debug=True)

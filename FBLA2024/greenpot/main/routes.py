from flask import render_template, request, Blueprint
from greenpot.models import Partner

main = Blueprint('main', __name__)

@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/help")
def help():
    return render_template('help.html', title='Help')

@main.route("/userhelp")
def user_help():
    return render_template('user_help.html', title='Help')


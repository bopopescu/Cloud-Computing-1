from flask import Flask, render_template, session, request, redirect, url_for, g
from app import webapp
from flask import Markup



@webapp.route('/',methods=['GET'])
# Display an HTML page with links
def main():
    return render_template("main.html")


from flask import render_template, jsonify, redirect, url_for
import requests
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Christina'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/mymatches', methods=['GET'])
def mymatches():
    response = requests.get("http://worldcup.sfg.io/matches/today")
    data = response.json()
    #return render_template('match_today.html',data=data)
    mystring = "Today's matches are:"
    for i in data:
        print(i['home_team']['code'] + "vs" + i['away_team']['code'])
        mystring = mystring + i['home_team']['code'] + "vs" + i['away_team']['code'] + '\n'
    return mystring

#         <div> Today's matches are: </div>
#  {% for i in data %}
#  {{ i.home_team.code }} v {{ i.away_team.code }}</br>
#  {% endfor %}

### IMPORTS ###
from flask import Flask, request, jsonify
import json
from flask import render_template,flash,redirect,session,url_for,abort
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from markupsafe import Markup

import os
import time
import numpy as np
import pandas as pd
from logic import preprocess,create_tfidf_features,calculate_similarity,show_similar_documents,df,html_codes,titles,urls,run_bm25,spell
import html

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY']='mysecret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
database_path = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

### FORMS ###
class MyForm(FlaskForm):
    search_query = StringField(validators=[DataRequired()])
    submit = SubmitField('submit')

### MODELS ###
class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    keywords = db.Column(db.String())
    url = db.Column(db.String())
    html = db.Column(db.String())

### VIEWS ###
#Homepage
@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        val = request.form.get('search_query')
        return redirect('/search/'+val)
    return render_template('index.html')

#Search results page
@app.route('/search/<qry>',methods=['GET', 'POST'])
def searching(qry):
    give_research_option = False
    returning = ''
    if(qry!=spell(qry)):
        returning = spell(qry)
        give_research_option = True
    print('\n\n')
    print(qry)
    print(preprocess(qry))
    print('Reading the corpus...')
    print('done')
    print('calculating the scores...')
    print('\n\n')
    # data = [(body+' '+title).lower() for title, body in zip(df['title'], df['keywords'])]
    # Learn vocabulary and idf, return term-document matrix
    # X,v = create_tfidf_features(data)
    # features = v.get_feature_names_out()
    # user_question = [preprocess(qry)]
    search_start = time.time()
    obj = run_bm25(qry)
    # sim_vecs, cosine_similarities = calculate_similarity(X, v, user_question)
    search_time = time.time() - search_start
    # d = show_similar_documents(data, cosine_similarities, sim_vecs)
    print("search time: {:.2f} ms".format(search_time * 1000))
    # if(d['1']['score']==0 or float(obj['1']['score'])>(d['1']['score'])):
    #     d=obj
    d=obj
    if(float(d['1']['score'])==0):
        if give_research_option:
            return redirect('/not_found/'+qry+'/1')
        return redirect('/not_found/'+qry)
    if give_research_option:
        return render_template('searching.html',qry=qry,d=d,search_time=search_time,give_research_option=give_research_option,returning=returning)
    return render_template('searching.html',qry=qry,d=d,search_time=search_time)

#User wants to re-search the query even if its spelled wrongly
@app.route('/research/<q>')
def research(q):
    print('\n\n')
    print(q)
    print('Reading the corpus...')
    print('done')
    print('calculating the scores...')
    print('\n\n')
    # data = [(body+' '+title).lower() for title, body in zip(df['title'], df['keywords'])]
    # Learn vocabulary and idf, return term-document matrix
    # X,v = create_tfidf_features(data)
    # features = v.get_feature_names_out()
    # user_question = [preprocess(qry)]
    search_start = time.time()
    obj = run_bm25(q,part=True)
    # sim_vecs, cosine_similarities = calculate_similarity(X, v, user_question)
    search_time = time.time() - search_start
    # d = show_similar_documents(data, cosine_similarities, sim_vecs)
    print("search time: {:.2f} ms".format(search_time * 1000))
    # if(d['1']['score']==0 or float(obj['1']['score'])>(d['1']['score'])):
    #     d=obj
    d=obj
    if(float(d['1']['score'])==0):
        return redirect('/not_found/'+q)
    return render_template('searching.html',qry=q,d=d,search_time=search_time)

#No matching results found page
@app.route('/not_found/<que>')
def not_found(que):
    que = que
    return render_template('not_found.html',que=que,give_research_option=False)

@app.route('/not_found/<que>/<val>')
def not_found_research(que,val):
    returning = spell(que)
    return render_template('not_found.html',que=que,give_research_option=val,returning=returning)


#Individual Problem Page
@app.route('/problem/<problem_id>')
def problem_page(problem_id):
    if(int(problem_id)<0 or int(problem_id)>len(titles)):
        abort(404, description="Resource not found")
    html_code = Markup(html_codes[int(problem_id)])
    return render_template('page.html',title=titles[int(problem_id)],html_code=html_code,url=urls[int(problem_id)])

#About page
@app.route('/about')
def about():
    return render_template('about.html')

# Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html'),404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('error_pages/403.html'),403

if __name__ == '__main__':
    app.run(debug=True)

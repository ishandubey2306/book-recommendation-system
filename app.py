from os import rename

from flask import Flask,request
from flask import render_template
import pickle
import numpy as np
import pandas as pd
popular_df=pickle.load(open('popular.pkl','rb'))
tp=pickle.load(open('tp.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))



app= Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html',
                               book_name=list(popular_df['Book-Title'].values),
                               author=list(popular_df['Book-Author_x'].values),
                               image=list(popular_df['Image-URL-M_x'].values),
                               votes=list(popular_df['num-rating'].values),
                               rating=list(popular_df['avg_rating'].values))
@app.route('/recommend_books' , methods=['post'])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(tp.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == tp.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('recommend.html',data=data)
@app.route('/recommend.html')
def recommend_ui():
    return render_template('contact.html')
@app.route('/contact.html')
def contact():
    return render_template('recommend.html')
if __name__ == '__main__':
       app.run(debug=True)

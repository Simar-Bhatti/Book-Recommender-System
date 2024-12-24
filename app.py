from flask import Flask, render_template, request
import pickle
import numpy as np

# Load data files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    
    # Check if the user input is valid and exists in pt.index
    if user_input not in pt.index:
        return render_template('recommend.html', data=[], error="Book not found. Please try again.")
    
    # Get the index of the user input book
    index = np.where(pt.index == user_input)[0][0]
    
    # Get similar items (recommendations) based on the cosine similarity scores
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        
        # Add the book title, author, and image URL
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    # Debugging print to check if data is populated
    print("Recommendations Data: ", data)

    # Render the recommendations in the template
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

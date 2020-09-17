from flask import Flask, render_template, request, session, redirect, url_for, abort
import database as db
import pymongo
from pymongo import MongoClient

#    <a href="{{ url_for('index') }}"><img name="back" src="{{ url_for('static', filename='back_button.png') }}", style="width=10%; height=10%;"></logo></a>

app = Flask(__name__)
app.secret_key = "383208427427332jack!"

@app.route('/')
def index():
    return render_template('home.html')



@app.route('/search')
def search():
    session["404last"] = False #set to false in for /addnote
    return render_template("search.html")


@app.route('/search', methods = ["POST"])
def search_submit():
    session['last_query'] = request.form
    print(request.form)
    return redirect(url_for('results'))


@app.route('/results')
def results():
    session["404last"] = False  # set to false in for /addnote
    data = session['last_query'] #try popping it here
    session['class'] = data['class']
    stuff = db.search_topic(data['class'], [data['query']])
    if stuff == "no_result":
        return redirect(url_for('error404'))

    print(stuff)
    found = stuff
    subtopic = found.pop("subtopic")  # also returns value
    topic = data['class']
    query = data['query']

    print("QUERY ADDED")
    ideas = {}
    for i in found:  # remaining items
        ideas[i] = found[i]
    return render_template('results.html', subtopic=subtopic, topic=topic, query=query, ideas=ideas)



@app.route('/results', methods=["POST"])
def results_form():
    session["404last"] = False  # set to false in for /addnote
    data = request.form
    stuff = db.search_topic(session['class'], [data['query']])

    if stuff == "no_result":
        return redirect(url_for('error404'))
    #ADD DATE/SORT BY DATE
    found = stuff
    subtopic = found.pop("subtopic")  # also returns value
    topic = session['class']
    query = data['query']
    ideas = {}
    #be sure to handle items added to form submits in the future before this

    for i in found:  # remaining items
        ideas[i] = found[i]
    return render_template('results.html', subtopic=subtopic, topic=topic, query=query, ideas=ideas)


@app.route('/addnote')
def addnote():
    if session["404last"] == True:
        autofill_subtopic = True
        session["404last"] = False  # set to false in for /addnote
        return render_template('add_note.html', autofill_subtopic=autofill_subtopic, autofill=session['last_query']['query'])
    else:
        autofill_subtopic = False
        return render_template('add_note.html', autofill_subtopic=autofill_subtopic)




@app.route('/addnote', methods=["POST"])
def addnote_submit():
    data = request.form
    data_values = []
    data_keys = []
    for i in data.values():
        data_values.append(i)
    for i in data.keys():
        data_keys.append(i)
    print(data_values)
    formatted_data = {}


    for i in data.keys():
        print(i)
        if "class" in i:
            classroom = data[i]
            print("found class")
        elif "subtopic" in i:
            print("subtopic found")
            subtopic_number = i.strip("subtopic")
            formatted_data[data[i]] = data_values[data_keys.index(str("content%s" % subtopic_number))]
        elif "topic" in i:
            print("found topic")
            formatted_data["topic"] = data[i]


    db.add_notes(classroom, formatted_data)

    return redirect(url_for("index"))




@app.route('/error404')
def error404():
    print("404 happened")
    session["404last"] = True #used to know whether to autofill /addnote or not in case of 'add note option'
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)

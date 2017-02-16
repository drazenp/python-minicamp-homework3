from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/enternew')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods= {'POST'})
def addfood():
    connection = sqlite3.connect('database.db')
    
    try:
        cursor = connection.cursor()
        
        name = request.form['name']
        calories = request.form['calories']
        cuisine = request.form['cuisine']
        is_vegetarian = request.form['is_vegetarian']
        is_gluten_free = request.form['is_gluten_free']
        
        cursor.execute('INSERT INTO foods (name, calories, cuisine, is_vegetarian, is_gluten_free) VALUES (?, ?, ?, ?, ?)', (name, calories, cuisine, is_vegetarian, is_gluten_free))
        connection.commit()
        message = 'Record successfully added'
    except Exception as e:
        print(str(e))
        connection.rollback()
        message = 'error in insert operation'
    finally:
        connection.close()
        return render_template('result.html', message = message)
    
@app.route('/favorite')
def favorite():
    connection = sqlite3.connect('database.db')
    
    food = ''
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM foods WHERE name="preska"')
        
        food = cursor.fetchone()
    except Exception as e:
        print(str(e))
    finally:
        connection.close()
        
    return jsonify(food)

@app.route('/search', methods= {'GET'})
def search():
    connection = sqlite3.connect('database.db')
    
    food = ''
    try:
        name = request.args['name']
        
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM foods WHERE name=?', (name,))
        
        food = cursor.fetchone()
    except Exception as e:
        print(str(e))
    finally:
        connection.close()
        
    return jsonify(food)

@app.route('/drop')
def drop():
    connection = sqlite3.connect('database.db')
    
    message = ''
    try:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS foods')
    except Exception as e:
        print(str(e))
        message = 'The foods table is not dropped.'
    finally:
        connection.close()
        message = 'dropped'
    return message
        
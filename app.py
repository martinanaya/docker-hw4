import time
import redis
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml
import mariadb
import sys

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

#Update REDIS value
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

#Get REDIT count
def get_count_only():
    retries = 5
    while True:
        try:
            return cache.get('hits').decode('utf-8')
        except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

#Connect to DB
def db_connection():
    retries = 5
    while True:
        try:
            conn = mariadb.connect(
            host="db",
            user="nclouds_user",
            password="secretpwfornclouds",
            database="nclouds"
            )
            conn.autocommit = True
            return conn
        except:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Runs if SQL Button is clicked
        if 'sql_submit' in request.form:
            # Fetch form data for SQL
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            # Connect to SQL Database
            try:
                conn = db_connection()
            except mariadb.Error as e:
                return render_template('index.html',sqlInputTotal="SQL Connection Error")
                sys.exit(1)
            # Create new Cursor with Connection Info
            cur = conn.cursor()
            # Insert new data into DB Table
            try:
                cur.execute("INSERT INTO docker(name, email, password) VALUES(%s, %s, %s)",(name, email, password))
            except mariadb.Error as e:
                return render_template('index.html',sqlInputTotal="SQL INSERT Error")
                sys.exit(1)
            # Grab a current count of rows in Table
            try:
                cur.execute("SELECT COUNT(*) FROM docker")
            except mariadb.Error as e:
                return render_template('index.html',sqlInputTotal="SQL SELECT Error")
                sys.exit(1)
            # Show only Integer value
            sqlInputTotal = int(cur.fetchone()[0])
            cur.close()
            conn.close()
            #Grab current REDIS total
            try:
                redisTotal = get_count_only()
            except:
                redisTotal = 0
            #Reload same page with new counts
            return render_template('index.html',redisTotal=redisTotal,sqlInputTotal=sqlInputTotal)
        # Runs if Redis Button is clicked
        elif 'redis_submit' in request.form:
            # Update Redis Total
            redisTotal = get_hit_count()
            # Grab SQL Count
            try:
                conn = db_connection()
            except mariadb.Error as e:
                return render_template('index.html',sqlInputTotal="SQL Connection Error")
                sys.exit(1)
            cur = conn.cursor()
            try:
                cur.execute("SELECT COUNT(*) FROM docker")
            except mariadb.Error as e:
                return render_template('index.html',sqlInputTotal="SQL SELECT Error")
                sys.exit(1)
            sqlInputTotal = int(cur.fetchone()[0])
            cur.close()
            conn.close()
            # Reload same page with new counts
            return render_template('index.html',redisTotal=redisTotal,sqlInputTotal=sqlInputTotal)
    elif request.method == 'GET':
        return render_template('index.html')

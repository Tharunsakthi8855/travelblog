

from flask import Flask, render_template, request, redirect, url_for
import ibm_db

app = Flask(__name)

# Replace these with your actual Db2 database credentials
db2_credentials = {
    "dsn": "crn:v1:bluemix:public:dashdb-for-transactions:eu-gb:a/62d9c229ead449a5b0a57f712ebecc77:91939826-d0a5-4c5e-a47c-2be42feece32::",
    "uid": "ntx72116",
    "pwd": "Fr79AIw9xssvhyMh"
}

def db2_connection():
    conn = ibm_db.connect(db2_credentials["crn:v1:bluemix:public:dashdb-for-transactions:eu-gb:a/62d9c229ead449a5b0a57f712ebecc77:91939826-d0a5-4c5e-a47c-2be42feece32::"], db2_credentials["ntx72116"], db2_credentials["Fr79AIw9xssvhyMh"])
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    conn = db2_connection()
    sql = "INSERT INTO users (name, email) VALUES (?, ?)"
    
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, email)

    if ibm_db.execute(stmt):
        ibm_db.commit(conn)
        ibm_db.close(conn)
        return redirect(url_for('success'))
    else:
        ibm_db.close(conn)
        return "Error while inserting data into the database."

@app.route('/success')
def success():
    return "Data successfully inserted into the database."

if _name_ == '_main_':
    app.run(debug=True)

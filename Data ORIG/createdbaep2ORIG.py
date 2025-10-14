from flask import Flask, render_template, request, redirect
import sqlite3
import csv

app = Flask(__name__)

# Initialize database if not exists
def create_db():
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "aeptbl" (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            State TEXT NOT NULL,
            Carrier TEXT NOT NULL,
            PlanName TEXT NOT NULL,
            PlanID  TEXT NOT NULL,
            Network TEXT NOT NULL,
            MOOP NUMERIC NOT NULL,
            Premium NUMERIC NOT NULL,
            Medical NUMERIC NOT NULL,
            RX NUMERIC NOT NULL,
            PCP NUMERIC NOT NULL,
            Specialist NUMERIC NOT NULL,
            Dental NUMERIC NOT NULL,
            Vision NUMERIC NOT NULL,
            Hearing NUMERIC NOT NULL,
            Transportation NUMERIC NOT NULL,
            OTC NUMERIC NOT NULL,
            Food_Util NUMERIC NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


 # Load date into table
def insert_aep_data(aep2_data):
    connection = sqlite3.connect('aep2.db')
    cursor = connection.cursor()

    cursor.execute("""
       INSERT INTO aeptbl (State, Carrier, PlanName, PlanID, Network, MOOP, Premium, Medical, 
       RX, PCP, Specialist, Dental, Vision, Hearing, Transportation, OTC, Food_Util)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, aep2_data)

    connection.commit()
    connection.close()

def load_csv_data(file_name):
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            aep2_data = tuple(row)
            insert_aep_data(aep2_data)

if __name__ == "__main__":
    create_db()
    load_csv_data('aep2_data.csv')


"""
if __name__=='__main__':
    app.run(debug=True)
"""
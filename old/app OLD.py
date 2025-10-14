#https://www.jeremymorgan.com/tutorials/python-tutorials/python-flask-web-app/
from flask import Flask, request, render_template
import sqlite3
app=Flask(__name__)

#Main Page
def get_full_list():
    connection = sqlite3.connect('aep2.db')
    cursor = connection.cursor()

    cursor.execute ("SELECT * FROM aeptbl")
    full_carrier_list = cursor.fetchall()

    connection.close()
    return full_carrier_list

# Added after working Helping to get all name for dropdown
def get_names():
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName FROM aeptbl")
    names = cursor.fetchall()
    conn.close()
    return names

# Get Carriers
def get_carriers():
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT carrier from aeptbl")
    carriers = cursor.fetchall()
    conn.close()
    return carriers
    #return [row[0] for row in rows]

# ADDED - Helper to get planinfo by id
def get_plan_info(entry_id):
    conn = sqlite3.connect('aep2.db')
    conn.row_factory = sqlite3.Row  # Allows dict-like access
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aeptbl WHERE id = ?", (entry_id,))
    plan = cursor.fetchone()
    conn.close()

    return dict(plan) if plan else None


def get_db_connection():
    conn = sqlite3.connect('aep2.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_states():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT State FROM aeptbl")
    states = [row[0] for row in cursor.fetchall()]
    conn.close()
    return states
#______________________________________________

#For Main Page
@app.route('/')
def index():
    full_carrier_list = get_full_list()
    return render_template('index.html', full_carrier_list=full_carrier_list)
# End For Main Page

# Begin Plan Info - WORKING
@app.route('/get') #Select Plan names
def select_plan():
    names = get_names()
    return render_template('selectplaninfo.html', names=names)

@app.route('/show', methods=['POST'])
def show():
   entry_id = request.form['entry_id']
   PlanID, Carrier, PlanName = get_plan_info(entry_id)
   return render_template('results_plan.html', PlanID=PlanID,Carrier=Carrier,PlanName=PlanName)
# End Plan Info - WORKING

#Begin Carriers
@app.route('/getcarrier') #Get Carrier
def select_carriers():
    carriers = get_carriers()
    carriers_drop_down = [c[0] for c in carriers]
    return render_template('selectcarrier.html', carriers_drop_down=carriers_drop_down)

@app.route('/showcarrierplans', methods=['POST'])
def showcarrier():
    selected_carriers = request.form.getlist("carrier")  # Get multiple selected values

    if not selected_carriers:
        return render_template('show_plans.html', plans_by_carrier={})  # No selection case

    db = get_db_connection()

    # Dynamically create placeholders for SQL query based on number of selected carriers
    placeholders = ', '.join('?' for _ in selected_carriers)
    query = f"SELECT Carrier, PlanName FROM aeptbl WHERE Carrier IN ({placeholders})"

    rows = db.execute(query, selected_carriers).fetchall()
    db.close()

    # Group plans by carrier
    plans_by_carrier = {}
    for row in rows:
        carrier = row['Carrier']
        if carrier not in plans_by_carrier:
            plans_by_carrier[carrier] = []
        plans_by_carrier[carrier].append(row['PlanName'])

    return render_template('show_plans.html', plans_by_carrier=plans_by_carrier)


@app.route('/carriers_by_state/<state>')
def carriers_by_state(state):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Carrier FROM aeptbl WHERE State = ?", (state,))
    carriers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"carriers": carriers}

@app.route('/selectstatecarrier')
def select_state_carrier():
    states = get_states()
    return render_template("state_carrier_select.html", states=states)

@app.route('/compare')
def compare_select():
    plans = get_names()  # You already have this function: returns (id, PlanName)
    return render_template('compare_select.html', plans=plans)

@app.route('/compare_results', methods=['POST'])
def compare_results():
    selected_ids = request.form.getlist('plans')

    if len(selected_ids) < 2 or len(selected_ids) > 3:
        return "Please select 2 or 3 different plans.", 400

    # Fetch plans
    plans = [get_plan_info(pid) for pid in selected_ids]
    if not all(plans):
        return "One or more selected plans could not be found.", 404

    # Use the keys from the first plan as field names
    fields = list(plans[0].keys())

    return render_template(
        'compare_results.html',
        plans=plans,
        fields=fields
    )


if __name__=='__main__':
    app.run(debug=True)

#---------------------------------------------------------------------------------

"""
@app.route('/show', methods=['POST'])
def show():
    entry_id = request.form['entry_id']
    PlanID = get_planid_by_id(entry_id)
    return render_template('result.html', PlanID=PlanID)
"""

"""
#Begin Get Names
@app.route('/select') #Get Names
def select_form():
    names = get_names()
    return render_template('select_form.html', names=names)
"""
"""
# Helper to get planid by id
def get_planid_by_id(entry_id):
    conn = sqlite3.connect('aep.db')
    cursor = conn.cursor()
    cursor.execute("SELECT PlanID FROM aeptbl WHERE id = ?", (entry_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
"""
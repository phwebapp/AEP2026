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
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl")
    names = cursor.fetchall()
    conn.close()
    return names

def get_namescsnp():
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl WHERE Network LIKE '%CSNP%'")
    names = cursor.fetchall()
    conn.close()
    return names

def get_namesdsnp():
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl WHERE Network LIKE '%DSNP%'")
    names = cursor.fetchall()
    conn.close()
    return names

# ADDED - Helper to get planinfo by id
def get_plan_info(entry_id):
    conn = sqlite3.connect('aep2.db')
    conn.row_factory = sqlite3.Row  # Allows dict-like access
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aeptbl WHERE id = ?", (entry_id,))
    plan = cursor.fetchone()
    conn.close()

    return dict(plan) if plan else None

# Get Carriers
def get_carriers():
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT carrier from aeptbl")
    carriers = cursor.fetchall()
    conn.close()
    return carriers
    #return [row[0] for row in rows]

def get_db_connection():
    conn = sqlite3.connect('aep2.db')
    conn.row_factory = sqlite3.Row
    return conn

#______________________________________________

#For Main Page
@app.route('/')
def index():
    full_carrier_list = get_full_list()
    return render_template('index.html', full_carrier_list=full_carrier_list)
# End For Main Page

@app.route('/compare')
def compare_select():
    plans = get_names()  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_select.html', plans=plans)

### Begin CSNP and DSNP
@app.route('/comparecsnp')
def compare_selectcsnp():
    plans = get_namescsnp()  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_selectcsnp.html', plans=plans)

@app.route('/comparedsnp')
def compare_selectdsnp():
    plans = get_namesdsnp()  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_selectdsnp.html', plans=plans)
### End CSNP and DSNP

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
    #fields = list(plans[0].keys())---commented out to remove ID from results
    fields = [key for key in plans[0].keys() if key != 'Id']
    return render_template(
        'compare_results.html',
        plans=plans,
        fields=fields
    )
@app.route('/getcarrier') #Get Carrier
def select_carriers():
    carriers = get_carriers()
    carriers_drop_down = [c[0] for c in carriers]
    return render_template('selectcarrier.html', carriers_drop_down=carriers_drop_down)

"""
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

    return render_template('showcarrier.html', plans_by_carrier=plans_by_carrier)
"""
if __name__=='__main__':
    app.run(debug=True)


"""
# Get Carriers
def get_carriers():
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT carrier from aeptbl")
    carriers = cursor.fetchall()
    conn.close()
    return carriers
    #return [row[0] for row in rows]

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

    return render_template('showcarrier.html', plans_by_carrier=plans_by_carrier)
"""

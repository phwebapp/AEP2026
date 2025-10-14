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

# get_names BY STATE
def get_names_by_state(state):
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl WHERE State = ?",(state,))
    names = cursor.fetchall()
    conn.close()
    return names

def get_namescsnp(state):
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl WHERE Type LIKE '%CSNP%' and State = ?",(state,))
    names = cursor.fetchall()
    conn.close()
    return names

def get_namesdsnp(state):
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl WHERE Type LIKE '%DSNP%' and State = ?",(state,))
    names = cursor.fetchall()
    conn.close()
    return names

def get_namesgiveback(state):
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl WHERE PlanName LIKE '%Giveback%' and State = ?",(state,))
    names = cursor.fetchall()
    conn.close()
    return names

def get_namestransportation(state):
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, PlanName, PlanID FROM aeptbl WHERE Upper(Trim(Transportation)) NOT LIKE 'No%' and State = ?",(state,))
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

#Select Carriers By State
def get_carriers_by_state(state):
    conn = sqlite3.connect('aep2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT carrier from aeptbl WHERE State = ?",(state,))
    carriers = cursor.fetchall()
    conn.close()
    #return carriers
    return [row[0] for row in carriers]

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

# UPDATED to include STATE - Compare Plans by STATE
@app.route('/compare')
def compare_select():
    state=request.args.get('state')
    plans = get_names_by_state(state)  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_select.html', plans=plans,state=state)

@app.route('/comparecsnp')
def compare_selectcsnp():
    state = request.args.get('state')
    plans = get_namescsnp(state)  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_selectcsnp.html', plans=plans,state=state)

@app.route('/comparedsnp')
def compare_selectdsnp():
    state = request.args.get('state')
    plans = get_namesdsnp(state)  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_selectdsnp.html', plans=plans,state=state)

@app.route('/comparegiveback')
def compare_selectgiveback():
    state = request.args.get('state')
    plans = get_namesgiveback(state)  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_selectgiveback.html', plans=plans,state=state)

@app.route('/comparetransportation')
def compare_selecttransportation():
    state = request.args.get('state')
    plans = get_namestransportation(state)  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_selecttransportation.html', plans=plans,state=state)
### End CSNP and DSNP

@app.route('/compare_results', methods=['POST'])
def compare_results():
    selected_ids = request.form.getlist('plans')

    #if len(selected_ids) < 2 or len(selected_ids) > 3:
        #return "Please select 2 or 3 different plans.", 400

    if len(selected_ids) > 3:
        return "Only select up to 3 different plans at a time....Go Back", 400

    # Fetch plans
    plans = [get_plan_info(pid) for pid in selected_ids]
    if not all(plans):
        return "One or more selected plans could not be found.", 404

    # Limit number of selections

    # Use the keys from the first plan as field names
    #fields = list(plans[0].keys())---commented out to remove ID from results
    fields = [key for key in plans[0].keys() if key != 'Id']

    return render_template(
        'compare_results.html',
        plans=plans,
        fields=fields
    )

#Modified getcarrier to accomodate state
@app.route('/getcarrier') #Get Carrier
def select_carriers():
    state = request.args.get('state')
    if not state:
        return "<p>Please select a state first</p>"
    carriers_drop_down = get_carriers_by_state(state)
   #carriers_drop_down = [c[0] for c in carriers]
    return render_template('selectcarrier.html', carriers_drop_down=carriers_drop_down, state=state)

@app.route('/showselectcarrier', methods=['POST'])
def show_select_carriers():
    selected_carriers = request.form.getlist("carrier")  # Get multiple selected values
    selected_state = request.form.get("state")

    if not selected_carriers or not selected_state:
        return "<p>No carriers or state selected. Please go back and choose at least one.</p>"  # No selection case

    db = get_db_connection()

    # Dynamically create placeholders for SQL query based on number of selected carriers
    placeholders = ', '.join(['?'] * len(selected_carriers))
    query = f"""SELECT * FROM aeptbl WHERE Carrier IN ({placeholders}) AND State = ? Order by Carrier"""
    params = selected_carriers + [selected_state]
    rows = db.execute(query, params).fetchall()
    db.close()

    return render_template('showselectcarrier.html', full_carrier_list=rows)


#compare_all STATE
@app.route('/compareall')
def compare_all_plans():
    state=request.args.get('state')
    plans = get_names_by_state(state)  # You already have this function: returns (id, PlanName, PlanID)
    return render_template('compare_select_all.html', plans=plans,state=state)

#Updated for State
@app.route('/compare_results_all', methods=['POST'])
def compare_resultsall():
    selected_ids = request.form.getlist('plans')
    selected_state = request.form.get('state')

    # Convert to set for faster lookup
    #selected_ids_set = set(selected_ids)
    selected_ids_set = set(map(str, selected_ids))

    # Get the full list of all plans
    full_carrier_list = get_full_list()

    # Filter full list based on selected plan IDs (assuming plan ID is at index 4)
    filtered_plans = [plan for plan in full_carrier_list if plan[3] in selected_ids_set and plan[1]==selected_state]

    if not filtered_plans:
        return "No matching plans found for the selected IDs.", 404

    return render_template('compare_results_all.html', full_carrier_list=filtered_plans)

# End For Main Page

if __name__=='__main__':
    app.run(debug=True)



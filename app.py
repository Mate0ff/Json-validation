import json, re, webbrowser
from flask import Flask, render_template, request
from flask.json import dumps
from datetime import datetime, date


app = Flask(__name__)

def name_validate(policy_name)->bool:
    # Validate if 'PolicyName' is present and meets criteria
    if not (policy_name and re.match(r'^[\w+=,.@-]{1,128}$', policy_name)):
         return False
    else:
        return True

def document_validate(policy_document)->bool:
    # Validate if 'PolicyDocument' is present and is a dictionary
    if not (isinstance(policy_document, dict) and policy_document):
        return False
    else:
        return True

def statement_validate(statement)->bool:
    # Validate if statements are in JSON format 
    if not isinstance(statement,dict):
        return False
    # Validate if keys are exactly 'Sid', 'Effect', 'Action', 'Resource'
    if not (set(statement.keys()) == set(['Sid', 'Effect', 'Action', 'Resource'])):
        return False
    
    # Validate if values are empty or Effect is not Allow or Deny
    if not (statement['Sid'] and (statement['Effect'] in ['Allow','Deny']) and statement['Action'] and statement['Resource']):
        return False
    
    return True

def version_validate(policy_version)->bool:
    try:
        policy_version_date = datetime.strptime(policy_version, '%Y-%m-%d').date()
        today_date = date.today()

        if policy_version_date > today_date:
        # If policy_version_date is after today's date, it's invalid
            return False
    except ValueError:
        # If parsing fails, the string is not a valid date
        return False
    return True

def json_validate(json_data)->bool:

    # Validate if keys are exactly 'PolicyName', 'PolicyDocument'
    if set(json_data.keys()) == set(['PolicyName', 'PolicyDocument']):

        policy_name = json_data.get('PolicyName')
        if not name_validate(policy_name):
            return False

        policy_document = json_data.get('PolicyDocument')
        if not document_validate(policy_document):
            return False

        # Validate if keys are exactly 'Version', 'Statement'
        if set(policy_document.keys()) == set(['Version', 'Statement']):
            
            policy_version = json_data.get('PolicyDocument', {}).get('Version')
            if not version_validate(policy_version):
                return False

            try:
                statements = json_data.get('PolicyDocument', {}).get('Statement', [])
                # Validate if statements is empty list
                if not statements:
                    return False
                
                for statement in statements:
                    if not statement_validate(statement):
                        return False
                    
                    #Validate if Resource is *
                    resource = statement.get('Resource')
                    if resource == '*':
                        return False
                    
                return True
            
            except AttributeError:
                return False
        else:
            return False
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    json_data = None

    if request.method == 'POST':
        try:
            # Retrieve JSON data from the form input
            json_text = request.form['json_text']
            json_data = json.loads(json_text)
            result = json_validate(json_data)
            # Convert the JSON data back to a formatted string
            json_data = dumps(json_data, indent=4)
        except (json.JSONDecodeError, KeyError):
            result = False
            json_data = json_text

        # Handle JSON file uploads
        if 'json_file' in request.files:  
            json_file = request.files['json_file']
            if json_file.filename != '':
                json_data = json.loads(json_file.read().decode('utf-8'))
                result = json_validate(json_data)
                # Convert the JSON data back to a formatted string
                json_data = dumps(json_data, indent=4)


    return render_template('home.html', json_data=json_data, result=result)

# Open the web browser when the server starts
if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(port=5000)

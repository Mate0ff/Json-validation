# JSON Validation
Program verify if the input JSON data is according to AWS::IAM::Role Policy.

## Installation

1. Clone the repository:
```
  git clone https://github.com/Mate0ff/Json-validation.git
```

2. Navigate into the cloned directory:
```
  cd my-project
```

3. Create a virtual environment (optional but recommended):

    Depending on version of python 
```
  py -m venv venv
```
```
  python3 -m venv venv
```

4. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```

- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

5. Install the required dependencies from the `requirements.txt` file:
 ```
  pip install -r requirements.txt
  ```

6. Run the Flask application:
```
  python app.py
   or 
  py app.py
```

## Usage 

You have two options for input:
- **Upload JSON File:** Click on the "Choose File" button, select a JSON file from your local machine, and click "Verify".
- **Manually Enter JSON Data:** Enter JSON data into the text area provided, and click "Verify".

 After clicking "Verify", the application will validate the input JSON data. If the input meets the specified criteria, it will display a success message indicating that the input is correct. If the input does not meet the criteria, it will display an error message indicating that the input is incorrect.


## Unit tests

Unit tests for the validation methods are present in a separate file. The unit tests ensure the correctness of the validation logic.

You can run them by :

```
  python test_json_validate.py
   or 
  py test_json_validate.py
```


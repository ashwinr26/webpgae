from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Define the column names for your table
columns = ["Student_Name", "Student_Number", "Parent_Name", "Parent_Number",
           "Period1", "Period2", "Period3", "Period4", "Period5", "Period6", "Period7"]

# Initialize an empty DataFrame to store the data
data = pd.DataFrame(columns=columns)


@app.route('/AS')
def index():
    return render_template('index.html', columns=columns, data=data.to_html(classes="table table-striped"))


@app.route('/add_data', methods=['POST'])
def add_data():
    global data
    if request.method == 'POST':
        student_name = request.form["Student_Name"]
        parent_name = request.form["Parent_Name"]
        student_number = request.form["Student_Number"]
        parent_number = request.form["Parent_Number"]

        # Validation: Check if student_name contains only alphabets and spaces
        if not student_name.replace(" ", "").isalpha():
            return jsonify({"error": "Student Name must contain only alphabets and spaces."}), 400

        # Validation: Check if student_number and parent_number contain only numeric characters
        if not student_number.isnumeric():
            return jsonify({"error": "Student Number must contain only numeric characters."}), 400

        # Validation: Check if student_number and parent_number are 10 digits long
        if len(student_number) != 10:
            return jsonify({"error": "Student Number must be 10 digits long."}), 400

        # Validation: Check if Parent_name contains only alphabets and spaces
        if not parent_name.replace(" ", "").isalpha():
            return jsonify({"error": "Parent Name must contain only alphabets and spaces."}), 400

        # Validation: Check if parent_number contain only numeric characters
        if not parent_number.isnumeric():
            return jsonify({"error": "Parent Number must contain only numeric characters."}), 400

        # Validation: Check if parent_number are 10 digits long
        if len(parent_number) != 10:
            return jsonify({"error": "Parent Number must be 10 digits long."}), 400

        new_data = {col: request.form[col] for col in columns}
        data = data.append(new_data, ignore_index=True)

        return render_template('index.html', columns=columns, data=data.to_html(classes="table table-striped"))


@app.route('/save_csv', methods=['POST'])
def save_csv():
    data.to_csv('attendance.csv', index=False)
    return 'Data has been saved to attendance.csv'


if __name__ == '__main__':
    app.run()

import flask
from flask import render_template, request
import subprocess
import sqlite3

app = flask.Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def func():
    def evaluate_submission(submission_path, test_input):
        try:
            result = subprocess.run(['python', '-c', submission_path], input=test_input, text=True, capture_output=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    conn = sqlite3.connect('test.sqlite3')
    cursor = conn.cursor()

    x = ''  # Initialize x with a default value
    output = None  # Initialize output outside the conditional block
    tc = 0  # Initialize tc outside the conditional block

    try:
        cursor.execute('''SELECT * FROM "test"''')
        rows = cursor.fetchall()

        if request.method == 'POST':
            x = request.form['c1']

            for row in rows:
                test_input = row[0]
                output = evaluate_submission(x, str(test_input))

                try:
                    inout = int(output)
                    if row[1] == inout:
                        tc += 1
                except ValueError:
                    print(f"Error: Output '{output}' is not a valid integer.")

                print(f"Output: {output}")

            print(tc)

        d = {'output': output, 'tc': tc}

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.commit()
        conn.close()

    return render_template('index.html', output=d)

if __name__ == '__main__':
    app.run(debug=True)

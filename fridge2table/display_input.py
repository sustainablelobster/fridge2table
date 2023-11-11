from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>User Input Display</title>
</head>
<body>
    <h1>User Input:</h1>
    <div>{{ user_input | safe }}</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def display_user_input():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template_string(html_template, user_input=user_input)
    return render_template_string(html_template, user_input="")

if __name__ == '__main__':
    app.run(debug=True)

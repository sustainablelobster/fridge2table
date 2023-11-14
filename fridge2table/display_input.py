from flask import Flask, request, render_template_string

app = Flask(__name__)

def display_user_input():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template_string(html_template, user_input=user_input)
    return render_template_string(html_template, user_input="")

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret-key'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location URL', validators=[DataRequired(), URL(message="Invalid URL")])
    open_time = StringField('Open Time', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()],
                                choices=[("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"),
                                         ("☕☕☕☕☕", "☕☕☕☕☕")])
    wifi_rating = SelectField('Wifi Rating', validators=[DataRequired()],
                              choices=[("✘", "✘"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"),
                                       ("💪💪💪💪", "💪💪💪💪"),
                                       ("💪💪💪💪💪", "💪💪💪💪💪")])
    power_outlet_rating = SelectField('Power Outlet Rating', validators=[DataRequired()],
                                      choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"),
                                               ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
                                               ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        row = [form.cafe.data,
               form.location_url.data,
               form.open_time.data,
               form.closing_time.data,
               form.coffee_rating.data,
               form.wifi_rating.data,
               form.power_outlet_rating.data]
        with open('cafe-data.csv', "a", newline='\n', encoding="utf8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

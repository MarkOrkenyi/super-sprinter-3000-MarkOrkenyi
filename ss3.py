from flask import Flask, render_template, request, redirect
import csv
import time
app = Flask(__name__)


def read_csv():
    data_content = []
    with open("data.csv") as data:
        content = csv.reader(data, delimiter=',')
        for row in content:
            data_content.append(row)
    return data_content


def write_csv(data_content):
    with open("data.csv", mode="w") as data:
        datawriter = csv.writer(data, delimiter=',')
        for row in data_content:
            datawriter.writerow(row)


@app.route('/')
@app.route('/list')
def index():
    data_content = read_csv()
    return render_template('list.html', data_content=data_content)


@app.route('/formsubmit', methods=['POST'])
def add_entry():
    data_content = read_csv()
    to_add = []
    try:
        id_ = str(int(data_content[-1][0]) + 1)
    except IndexError:
        id_ = 0
    storytitle = str(request.form['story title'])
    userstory = str(request.form['user story'])
    acceptance = str(request.form['acceptance'])
    business_value = str(request.form['business value'])
    estimation = str(request.form['estimation'])
    status = str(request.form['status'])
    to_add.append(id_)
    to_add.append(storytitle)
    to_add.append(userstory)
    to_add.append(acceptance)
    to_add.append(business_value)
    to_add.append(estimation)
    to_add.append(status)
    data_content.append(to_add)
    write_csv(data_content)
    return redirect('/')


@app.route('/story/<int:storyid>/editform', methods=['POST'])
def edit_entry(storyid):
    data_content = read_csv()
    id_ = storyid
    storytitle = str(request.form['story title'])
    userstory = str(request.form['user story'])
    acceptance = str(request.form['acceptance'])
    business_value = str(request.form['business value'])
    estimation = str(request.form['estimation'])
    status = str(request.form['status'])
    row_to_edit = data_content[id_]
    row_to_edit[1] = storytitle
    row_to_edit[2] = userstory
    row_to_edit[3] = acceptance
    row_to_edit[4] = business_value
    row_to_edit[5] = estimation
    row_to_edit[6] = status
    write_csv(data_content)
    return redirect('/list')


@app.route('/story/<int:storyid>/delete')
def delete_entry(storyid):
    data_content = read_csv()
    id_ = storyid
    data_content.pop(id_)
    write_csv(data_content)
    return redirect('/list')


@app.route('/story/<int:storyid>', methods=['GET'])
def update_story(storyid):
    data_content = read_csv()
    story_id = storyid
    storytitle = data_content[story_id][1]
    userstory = data_content[story_id][2]
    acceptance = data_content[story_id][3]
    business_value = data_content[story_id][4]
    estimation = data_content[story_id][5]
    status = data_content[story_id][6]
    return render_template('form.html',
                           formsubmit="editform",
                           storyid=story_id,
                           storytitle=storytitle,
                           userstory=userstory,
                           acceptance=acceptance,
                           business_value=business_value,
                           estimation=estimation,
                           status=status)


@app.route('/story')
def story():
    return render_template('form.html', formsubmit="formsubmit")

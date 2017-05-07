from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)


def read_csv():
    '''Open csv file and create a list of lists with it's content'''
    csv_content = []
    with open("data.csv") as data:
        content = csv.reader(data, delimiter=',')
        for row in content:
            csv_content.append(row)
    return csv_content


def write_csv(csv_content):
    '''Writes out the list of lists to a csv file'''
    with open("data.csv", mode="w") as data:
        datawriter = csv.writer(data, delimiter=',')
        for row in csv_content:
            datawriter.writerow(row)


def generate_ids():
    '''Orders the IDs in the csv file'''
    csv_content = read_csv()
    i = 0
    for row in csv_content:
        row[0] = i
        i += 1
    write_csv(csv_content)


@app.route('/')
@app.route('/list')
def index():
    '''Generates ordered IDs and displays the content of the csv file in a html template "list.html"'''
    generate_ids()
    csv_content = read_csv()
    print(csv_content)
    return render_template('list.html', csv_content=csv_content)


@app.route('/formsubmit', methods=['POST'])
def add_entry():
    '''Add new entry to the csv file'''
    csv_content = read_csv()
    to_add = []
    try:
        id_ = str(int(csv_content[-1][0]) + 1)
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
    csv_content.append(to_add)
    write_csv(csv_content)
    return redirect('/')


@app.route('/story/<int:storyid>/editform', methods=['POST'])
def edit_entry(storyid):
    '''Edits entry of the csv file'''
    csv_content = read_csv()
    id_ = storyid
    storytitle = str(request.form['story title'])
    userstory = str(request.form['user story'])
    acceptance = str(request.form['acceptance'])
    business_value = str(request.form['business value'])
    estimation = str(request.form['estimation'])
    status = str(request.form['status'])
    row_to_edit = csv_content[id_]
    row_to_edit[1] = storytitle
    row_to_edit[2] = userstory
    row_to_edit[3] = acceptance
    row_to_edit[4] = business_value
    row_to_edit[5] = estimation
    row_to_edit[6] = status
    write_csv(csv_content)
    return redirect('/list')


@app.route('/story/<int:storyid>/delete')
def delete_entry(storyid):
    '''Deletes entry of the csv file'''
    csv_content = read_csv()
    id_ = storyid
    csv_content.pop(id_)
    write_csv(csv_content)
    return redirect('/list')


@app.route('/story/<int:storyid>', methods=['GET'])
def update_story(storyid):
    '''Renders the template "form.html" with pre-entered values to edit a given entry'''
    csv_content = read_csv()
    story_id = storyid
    storytitle = csv_content[storyid][1]
    userstory = csv_content[story_id][2]
    acceptance = csv_content[story_id][3]
    business_value = csv_content[story_id][4]
    estimation = csv_content[story_id][5]
    status = csv_content[story_id][6]
    return render_template('form.html',
                           formsubmit="editform",
                           form_submit_button="Update",
                           title="Edit Story",
                           storyid=story_id,
                           storytitle=storytitle,
                           userstory=userstory,
                           acceptance=acceptance,
                           business_value=business_value,
                           estimation=estimation,
                           status=status)


@app.route('/story')
def story():
    '''Renders the template "form.html" to add a new entry'''
    return render_template('form.html', formsubmit="formsubmit", form_submit_button="Submit", title="Add new Story")


if __name__ == '__main__':
    app.run(debug=True)

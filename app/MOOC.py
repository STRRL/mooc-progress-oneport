# -*- coding:utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import selectdata
import sys, os, csv

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.secret_key = "hello THe W?"
Bootstrap(app)
aliasdict = {}
with open(sys.path[0] + '/alias.csv', 'rb') as f:
    cr = csv.reader(f)
    for row in cr:
        aliasdict[row[1]] = row[0]


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", list=aliasdict)


# metadata
# @app.route('/<alias>/search/<stu_id>')
# def serch_by_id(stu_id):
#     return selectdata.select_by_id(stu_id)


@app.route('/<alias>/<stu_id>')
def search_by_id(alias, stu_id):
    (jo, name, mtime) = selectdata.select_by_id(alias, stu_id, "json")
    return render_template("progress.html", jo=jo, mtime=mtime)


@app.route('/<alias>')
def sub_index(alias):
    if os.path.exists(sys.path[0] + "/src/%s" % alias):

        return render_template('sub_index.html', classname=aliasdict[alias], alias=alias)
    else:
        return render_template('message.html', message="没有这个课程")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

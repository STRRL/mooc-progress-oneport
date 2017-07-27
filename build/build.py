# -*- coding:utf-8 -*-
import sys, csv, hashlib
import getdata

aliasdict = []


def downloaddata(username, password, classid, classname):
    tmp = hashlib.md5()
    tmp.update(classid)
    aliasdict.append([classname, tmp.hexdigest()])
    getdata.start(username, password, classid, tmp.hexdigest())


def wirtealiasdict():
    with open(sys.path[0] + "/../app/alias.csv", 'wb') as f:
        cw = csv.writer(f)
        cw.writerows(aliasdict)


def main():
    with open(sys.path[0] + "/list.csv", 'rb') as f:
        cr = csv.reader(f)
        # 账号 密码 ID name
        for row in cr:
            downloaddata(row[0], row[1], row[2], row[3])
    wirtealiasdict()


if __name__ == '__main__':
    main()

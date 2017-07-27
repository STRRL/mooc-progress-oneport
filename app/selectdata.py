# -*- coding:utf-8 -*-
import xlrd, json, os, sys, re, time, uniout

xlrd.Book.encoding = "utf-8"


# r = re.compile(r'.*(xlsx)+.*')

#
# def index_file(filepath):
#     filelist = []
#     files = os.listdir(filepath)
#     for fi in files:
#         fi_d = os.path.join(filepath, fi)
#         if os.path.isdir(fi_d):
#             filelist.extend(index_file(fi_d))
#         else:
#             if r.match(fi):
#                 filelist.append(os.path.join(filepath, fi_d))
#     filelist.sort()
#     return filelist
#
#
# def select_by_id(alias, stu_id, datatype="string"):
#     if stu_id == "favicon.ico":
#         return "", ""
#     dirpath = sys.path[0] + "/src/%s" % alias
#     filelist = index_file(dirpath)
#     ja = []
#     count = 0
#     for i in filelist:
#         tmp = search_file_by_id(i, stu_id)
#         if len(tmp) != 0:
#             temp = []
#             temp.append({"id": count})
#             temp.append({"content": tmp})
#             ja.append(temp)
#             count += 1
#     mtime = time.localtime(os.stat(filelist[0]).st_mtime)
#     detailtime = "%s-%s-%s" % (str(mtime.tm_year), str(mtime.tm_mon), str(mtime.tm_mday))
#     if datatype == "json":
#         return ja, detailtime
#     return json.dumps(ja),
#
#
# def search_file_by_id(filename, id):
#     title_id_start_col = 14  # 课程信息从第十四列开始
#     stu_name_col = 2  # 姓名在第三列
#     stu_id_col = 3  # 学号在第四列
#     rproblem = re.compile(r'.*(problem)+.*')
#     rvideo = re.compile(r'.*(video)+.*')
#     hiddenfile = re.compile(r'.*(~\$)+.*')  # 忽略office自动备份文件
#     if hiddenfile.match(filename):
#         return []
#     if rvideo.match(filename):
#         # print filename
#         with xlrd.open_workbook(filename=filename, encoding_override="utf8") as data:
#             sheet0 = data.sheet_by_index(0)
#             nrows = sheet0.nrows
#             jo = []
#             for i in range(1, nrows):
#                 if sheet0.cell(i, stu_id_col).value == id:
#                     for j in range(title_id_start_col, sheet0.ncols):
#                         jo.append({"name": unicode(sheet0.cell(0, j).value),
#                                    "progress": "%.2f %%" % (float(sheet0.cell(i, j).value) * 100)})
#                     return jo
#             return []
#     if rproblem.match(filename):
#         return []
#     return []

# def index_file(filepath):
#     filelist = []
#     files = os.listdir(filepath)
#     for fi in files:
#         fi_d = os.path.join(filepath, fi)
#         if os.path.isdir(fi_d):
#             filelist.extend(index_file(fi_d))
#         else:
#             if r.match(fi):
#                 filelist.append(os.path.join(filepath, fi_d))
#     filelist.sort()
#     return filelist
#
#
# def select_by_id(alias, stu_id, datatype="string"):
#     if stu_id == "favicon.ico":
#         return "", ""
#     dirpath = sys.path[0] + "/src/%s" % alias
#     filelist = index_file(dirpath)
#     ja = []
#     count = 0
#     for i in filelist:
#         tmp = search_file_by_id(i, stu_id)
#         if len(tmp) != 0:
#             temp = []
#             temp.append({"id": count})
#             temp.append({"content": tmp})
#             ja.append(temp)
#             count += 1
#     mtime = time.localtime(os.stat(filelist[0]).st_mtime)
#     detailtime = "%s-%s-%s" % (str(mtime.tm_year), str(mtime.tm_mon), str(mtime.tm_mday))
#     if datatype == "json":
#         return ja, detailtime
#     return json.dumps(ja),
def select_by_id(alias, stu_id, datatype="string"):
    if stu_id == "favicon.ico":
        return "", ""
    dirpath = sys.path[0] + "/src/%s" % alias
    return search_file_by_id("%s/file.xlsx" % dirpath, stu_id)


def search_file_by_id(filename, id):
    col_name = 0  # 姓名在第一列
    # col_stuid = 3  # 学号在第四列
    col_stuid = 1  # 学号在第二列
    col_videoinfo = 11  # 课程信息从第十一列开始
    Result = []
    with xlrd.open_workbook(filename=filename, encoding_override="utf8") as data:
        sheet0 = data.sheet_by_index(0)
        nrows = sheet0.nrows
        ncols = sheet0.ncols
        li = {}
        mtime = time.localtime(os.stat(filename).st_mtime)
        detailtime = "%s-%s-%s" % (str(mtime.tm_year), str(mtime.tm_mon), str(mtime.tm_mday))
        name = ""
        for i in range(1, nrows):
            if sheet0.cell(i, col_stuid).value == id:
                name = sheet0.cell(i, col_name)
                for j in range(col_videoinfo, ncols):
                    # ja[sheet0.cell(0, j)] = sheet0.cell(i, j).value
                    rednz = re.compile(u"第\d*章")
                    rerep = re.compile(u"第\d*章\:")
                    renum = re.compile("\d*")
                    dnz = rednz.search(sheet0.cell(0, j).value)
                    if not dnz.group() in li:
                        rename, a = rerep.subn("", sheet0.cell(0, j).value.replace("的学习比例", ""))
                        theid = renum.findall(dnz.group())[1]
                        li[dnz.group()] = {"name": rename, "detail": [], "id": theid}
                        li[dnz.group()]["detail"].append(
                            {"name": sheet0.cell(0, j).value.replace("的学习比例", ""), "value": sheet0.cell(i, j).value})
                    else:
                        li[dnz.group()]["detail"].append(
                            {"name": sheet0.cell(0, j).value.replace("的学习比例", ""), "value": sheet0.cell(i, j).value})
    for item in li:
        Result.append(li[item])
    if Result:
        Result = sorted(Result, mycompare)
        return Result, name, detailtime
    else:
        return Result, "", detailtime


def mycompare(x, y):
    if int(x['id']) > int(y['id']):
        return 1
    if int(x['id']) < int(y['id']):
        return -1
    return 0


if __name__ == '__main__':
    alias = "fc1689113684560d62966be8cde87d8c"
    stu_id = "20141120124"
    select_by_id(alias, "20141120124")

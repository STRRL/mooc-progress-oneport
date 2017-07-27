# 云南大学慕课进度查询工具 (单端口版)
云南大学慕课进度查询工具,方便同学查询自己的慕课课程进度. 

## 环境要求
linux

docker  

docekr-compose

## 部署

部署时将`list.csv.template`文件改名为`list.csv`  

填入老师的账号,密码,以及慕课平台上的ID,慕课课程要显示的名称  

(ID形如:`course-v1:ynu_ustcX+LB0520372,XXXXXXX`)  

执行`start.sh`即可

## 更新数据
只需要在crontab中定时执行`restart.sh`即可

[云南大学慕课平台](http://ynu.xuetangx.com/)

[项目传送门](http://progress.xuetangx.dev.ynuosa.org/)
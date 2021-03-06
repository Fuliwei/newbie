#/usr/bin/python
#coding:utf-8

from flask import Flask ,render_template,request
import MySQLdb as mysql
import json,time 
import datetime
import traceback
from datas import *

##连接数据库
conn = mysql.connect(user='root',host='127.0.0.1',passwd='123456',db='reboot',charset='utf8')
conn.autocommit(True)

cur = conn.cursor()

app = Flask(__name__)

def getNowTime():
	now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	return now

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == "POST":
		#dict(request.form)获取得value值为列表
		user_mes = dict(request.form)
		#插入数据库时,unicode编码不支持,所以需要将u'xx'使用str转换为字符串
		user_mes = dict((k,str(v[0])) for k ,v in user_mes.items() )
		print user_mes
		user_mes['create_time'] = getNowTime()
		if user_mes['status'] == "unlock":
			user_mes['status'] = 0
		else :
			user_mes['status'] = 1
		if (not user_mes['password']) or (not user_mes['repassword']) or (user_mes['password'] != user_mes['repassword']):
			errmes = "password not null or password different" 
			return render_template('userinfo.html',errmes = errmes,user = {})
		mes = addUser('users',user_mes)
		return render_template('userinfo.html',errmes = mes,user = user_mes)
	return render_template('register.html')

@app.route('/')
def index():
	return redirect('/login')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == "POST":
		data = dict((k,v[0]) for k ,v in  dict(request.form).items())
		#print data
		fields = ['id','name','password']
		alluser = getUsers('users')
		if (not data['name']) or (data['name'] not in [x['name'] for x in alluser]):
			errmsg = "Name is null or is not exists"
			return errmsg
		condition = "name = '%(name)s'" %data
		sql = "select %s from users where %s " %(','.join(fields),condition)
		cur.execute(sql)
		res = cur.fetchone()
		user = dict((v,res[k]) for k ,v in enumerate(fields))
		if user['password'] != data['password']:
			errmsg = "Wrong Password"
                        return errmsg
		else :
			condition = "id = '%(id)s'" %user
               		sql = "select %s from users where %s " %(','.join(['id','name','name_cn','mobile','email']),condition)
                	cur.execute(sql)
			re = cur.fetchone()
                	tmp = dict((v,re[k]) for k ,v in enumerate(['id','name','name_cn','mobile','email']))
			return render_template('userinfo.html',user=tmp,errmes = '')
	else:
		return render_template('login.html')


@app.route('/userlist')
def userlist():
	alluser = getUsers('users')
	return render_template("userlist.html",users = alluser,mes = '' )
@app.route('/delete')
def delete():
	u_id = request.args.get('id',None)
	mes = delUser('users',u_id)
	alluser = getUsers('users')
	return render_template('userlist.html',users = alluser,mes = mes  )

@app.route('/update',methods=['GET','POST'])
def update():
	if request.method == "POST":
		user = dict(request.form)
		user = dict((k,str(v[0])) for k ,v in user.items())
		mes = updateMes('users',user)
		alluser = getUsers('users')
		return render_template('userlist.html',users = alluser,mes = mes)
	u_id = request.args.get('id',None)
	print u_id
	user = getOne('users',u_id)
	print user
	return render_template('update.html',user=user)

@app.route('/changePwd',methods=['GET','POST'])
def changePwd():
	if request.method == "POST":
		tmp = dict(request.form)
		tmp = dict((k,str(v[0])) for k ,v in tmp.items())
		mes = modifyPasswd('users',tmp)
		alluser = getUsers('users')
		return render_template("userlist.html",users = alluser,mes = mes )
	u_id = request.args.get('id',None)
	user = getOne('users',u_id)
	#print user
	return render_template('password.html',user=user,mes = '')

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=888,debug=True)

# -*- coding=utf8 -*-
# 导入Flask库
from flask import Flask, flash, render_template
from flask import request, session, g, redirect, url_for, abort
# 导入MySQL库
import pymysql

app = Flask(__name__)
# 写好的数据库连接函数，
# 传入的是table，数据表的名称，
# 返回值是数据表中所有的数据，以元祖的格式返回
app.config['SECRET_KEY'] = '123456'
# or
app.secret_key = '123456'
# or
app.config.update(SECRET_KEY='123456')

def get_Table_Data(table):
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='',
        db='csp', charset='utf8',
    )
    cur = conn.cursor()
    res = cur.execute("select * from " + table)
    res = cur.fetchmany(res)
    cur.close()
    conn.commit()
    conn.close()
    return res
def connect_db():
    """Connects to the specific database."""
    db = pymysql.connect(host = '127.0.0.1',user = 'root',charset = 'utf8',passwd = '',db = 'csp')
    return db
# 启动服务器后运行的第一个函数，显示对应的网页内容
@app.route('/', methods=['GET', 'POST'])
def home():
    # return '<a href="/index"><h1 align="center">欢迎使用教务系统---点击进入</h1></a>'
    return render_template('login.html')

# 对登录的用户名和密码进行判断
@app.route('/login', methods=['GET','POST'])
def login():
    # 需要从request对象读取表单内容：
    error = None
    if request.method == 'POST':
        if request.form['classname']=='teacher':
            db = connect_db()
            cur = db.cursor()
            cur.execute('select username,password from user')
            pas = dict(cur.fetchall())
            db.close()
            if pas.get(request.form['username']) == None :
                flash("账号错误，请重新输入...")
                return render_template('login.html')
            elif request.form['password'] != pas[request.form['username']]:
                flash("密码错误，请重新输入...")
                return render_template('login.html')
            else:
                session['logged_th'] = request.form['username']
                db = connect_db()
                cur = db.cursor()
                sql = 'select username from user where username=%s'
                s=cur.execute(sql,(session['logged_th']))
                z=cur.fetchmany(s)
                db.commit()
                db.close()
                return render_template('teacher_index.html', error=error,name=z[0][0])
        if request.form['classname']=='student':
            db = connect_db()
            cur = db.cursor()
            sql = 'select number,password from xueshengleibie where number = %s'
            s=cur.execute(sql,(request.form['username']))
            z=cur.fetchmany(s)
            db.commit()
            db.close()
            if s==0 :
                flash("账号错误，请重新输入...")
                return render_template('login.html')
            if z[0][1]!=request.form['password']:
                flash("密码错误，请重新输入...")
                return render_template('login.html')
            else :
                session['logged_st'] = request.form['username']
                db = connect_db()
                cur = db.cursor()
                sql = 'select name from xueshengleibie where number=%s'
                s=cur.execute(sql,(session['logged_st']))
                z=cur.fetchmany(s)
                db.commit()
                db.close()
                return render_template('student_index.html',name=z[0][0])
    return render_template('login.html')

@app.route('/pwd', methods=['GET','POST'])
def pwd():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    if request.method=='POST':
        if request.form['pwd']==request.form['pwd1']:
            db = connect_db()
            cur = db.cursor()
            sql = 'update xueshengleibie set password=%s where number=%s'
            cur.execute(sql,(request.form['pwd'],session['logged_st']))
            db.commit()
            db.close()
            flash('修改密码成功，请重新登录')
            session.pop('logged_st',None)
            return render_template('login.html')
        else :
            flash('两次密码不相同，请重新输入')
            return render_template('pwd.html')
    return render_template('pwd.html')

@app.route('/pwdt', methods=['GET','POST'])
def pwdt():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    if request.method=='POST':
        if request.form['pwd']==request.form['pwd1']:
            db = connect_db()
            cur = db.cursor()
            sql = 'update user set password=%s where username=%s'
            cur.execute(sql,(request.form['pwd'],session['logged_th']))
            db.commit()
            db.close()
            flash('修改密码成功，请重新登录')
            session.pop('logged_th',None)
            return render_template('login.html')
        else :
            flash('两次密码不相等，请重新输入')
            return render_template('pwdt.html')
    return render_template('pwdt.html')


@app.route('/loginout', methods=['GET','POST'])
def loginout():
    flash('登出成功！')
    session.pop('logged_th',None)
    return render_template('login.html')

@app.route('/loginout2', methods=['GET','POST'])
def loginout2():
    flash('登出成功！')
    session.pop('logged_st',None)
    return render_template('login.html')     


# 显示学生首页的函数，可以显示首页里的信息
@app.route('/student_index', methods=['GET'])
def student_index():
    db = connect_db()
    cur = db.cursor()
    sql = 'select name from xueshengleibie where number=%s'
    s=cur.execute(sql,(session['logged_st']))
    z=cur.fetchmany(s)
    db.commit()
    db.close()
    return render_template('student_index.html',name=z[0][0])

# 显示教师首页的函数，可以显示首页里的信息
@app.route('/teacher_index', methods=['GET'])
def teacher_index():
    db = connect_db()
    cur = db.cursor()
    sql = 'select username from user where username=%s'
    s=cur.execute(sql,(session['logged_th']))
    z=cur.fetchmany(s)
    db.commit()
    db.close()
    return render_template('teacher_index.html',name=z[0][0])

# 显示教学计划的函数，当有请求发生时，去数据库里查找对应的数据，
# 然后将数据的格式用for循环进行遍历，变成列表的格式，然后返回到页面中，
# 再由页面进行显示数据
@app.route('/jxjh', methods=['GET','POST'])
def jxjh():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    # 调用数据库函数，获取数据
    data = get_Table_Data('jihuaxijie')
    # 用列表的格式存放全部数据
    titile={
        'a':'课程名称',
        'b':'任课老师',
        'c':'考核方式',
    }
    url='jxjh'
    path="/jxjh"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]

        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from jihuaxijie where coursename = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from jihuaxijie where coursename = %s'
            s=cur.execute(sql,(request.form['bbb']))
            if s !=0:
                z=cur.fetchmany(s)
                posts1 = []
                for value in z:
                    dict_data = {}
                    dict_data['课程名称'] = value[0]
                    dict_data['任课老师'] = value[1]
                    dict_data['考核方式'] = value[2]
                    posts1.append(dict_data)
                flash(posts1)
            else:
                flash('未查询到...')
        return redirect(url_for('jxjh'))
    #print(posts)
    return render_template('teacher.html', posts=posts,titile=titile,path=path,url=url)


# 显示管理班的函数页面
@app.route('/guanliban', methods=['GET','POST'])
def guanliban():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('guanliban')
    # 用列表的格式存放全部数据
    titile={
        'a':'ID',
        'b':'专业',
        'c':'年级',
        'd':'班级'
    }
    path="/guanliban"
    url="guanliban"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from guanliban where id = %s '
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from guanliban where specialities = %s'
            s=cur.execute(sql,(request.form['bbb']))
            if s!=0:
                z=cur.fetchmany(s)
                posts1 = []
                for value in z:
                    dict_data = {}
                    dict_data['ID'] = value[0]
                    dict_data['专业'] = value[1]
                    dict_data['年级'] = value[2]
                    dict_data['班级'] = value[3]
                    posts1.append(dict_data)
                flash(posts1)
            else:
                flash('未查询到...')
        return redirect(url_for('guanliban'))
    # print posts
    return render_template('teacher.html', posts=posts,titile=titile,path=path,url=url)

# 显示排课信息的函数页面
@app.route('/paike_js', methods=['GET','POST'])
def paike_js():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('paike_js')
    # 用列表的格式存放全部数据
    titile={
        'a':'课程名称',
        'b':'课程教室',
        'c':'课程时间'
    }
    path="/paike_js"
    url="paike_js"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from paike_js where course_name = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
            db = connect_db()
            cur = db.cursor()
            sql='select * from paike_js where course_name = %s'
            s=cur.execute(sql,(request.form['bbb']))
            if s !=0:
                z=cur.fetchmany(s)
                posts1 = []
                for value in z:
                    dict_data = {}
                    dict_data['课程名称'] = value[0]
                    dict_data['课程教室'] = value[1]
                    dict_data['课程时间'] = value[2]
                    posts1.append(dict_data)
                flash(posts1)
            else:
                flash('未查询到...')
        return redirect(url_for('paike_js'))
    # print posts
    return render_template('teacher.html', posts=posts,titile=titile,path=path,url=url)

# 显示学生成绩的页面，包括调用学生成绩数据表
@app.route('/xscj', methods=['GET','POST'])
def xscj():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('xueshengchengji')
    # 用列表的格式存放全部数据
    titile={
        'a':'学生学号',
        'b':'学生姓名',
        'c':'课程名称',
        'd':'学生成绩'
    }
    path="/xscj"
    url="xscj"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from xueshengchengji where course_name = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
           db = connect_db()
           cur = db.cursor()
           sql='select * from xueshengchengji where course_name = %s'
           s=cur.execute(sql,(request.form['bbb']))
           if s!=0:
               z=cur.fetchmany(s)
               posts1 = []
               for value in z:
                   dict_data = {}
                   dict_data['学生学号'] = value[0]
                   dict_data['学生姓名'] = value[1]
                   dict_data['课程名称'] = value[2]
                   dict_data['学生成绩'] = value[3]
                   posts1.append(dict_data)
               flash(posts1)
           else:
               flash('未查询到...')
        return redirect(url_for('xscj'))
    # print posts
    return render_template('teacher.html',posts=posts,titile=titile,path=path,url=url)

# 显示学生类别的页面，包括调用学生成绩数据表
@app.route('/xslb', methods=['GET','POST'])
def xslb():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('xueshengleibie')
    # 用列表的格式存放全部数据
    titile={
        'a':'学生姓名',
        'b':'学生学号',
        'c':'学生专业',
        'd':'学生班级'
    }
    path="/xslb"
    url="xslb"
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        posts.append(dict_data)
    if request.method=='POST':
        if request.form['test']=='delete':
            db = connect_db()
            cur = db.cursor()
            sql = 'delete from xueshengleibie where name = %s'
            cur.execute(sql,(request.form['aaa']))
            db.commit()
            db.close()
            flash('删除成功！')
        if request.form['test']=='search':
          db = connect_db()
          cur = db.cursor()
          sql='select * from xueshengleibie where name = %s'
          s=cur.execute(sql,(request.form['bbb']))
          if s!=0:
              z=cur.fetchmany(s)
              posts1 = []
              for value in z:
                  dict_data = {}
                  dict_data['学生姓名'] = value[0]
                  dict_data['学生学号'] = value[1]
                  dict_data['学生专业'] = value[2]
                  dict_data['学生班级'] = value[3]
                  posts1.append(dict_data)
              flash(posts1)
          else:
              flash('未查询到...')
        return redirect(url_for('xslb'))
    # print posts
    return render_template('teacher.html', posts=posts,titile=titile,path=path,url=url)


# 显示田楼教室的函数页面
@app.route('/tjiaoshi', methods=['GET','POST'])
def tjiaoshi():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('paike_js')
    titile={
        'a':'课程名称',
        'b':'上课教室',
        'c':'上课时间'
    }
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    if request.method=='POST':
        db = connect_db()
        cur = db.cursor()
        sql='select * from paike_js where course_name = %s'
        s=cur.execute(sql,(request.form['bbb']))
        if s !=0:
            z=cur.fetchmany(s)
            posts1 = []
            for value in z:
                dict_data = {}
                dict_data['课程名称'] = value[0]
                dict_data['课程教室'] = value[1]
                dict_data['课程时间'] = value[2]
                posts1.append(dict_data)
            flash(posts1)
        else:
            flash('未查询到...')
        return redirect(url_for('tjiaoshi'))
    # print posts
    return render_template('student.html', posts=posts,titile=titile)

# 显示课程的函数页面
@app.route('/kecheng', methods=['GET','POST'])
def kecheng():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('jihuaxijie')
    titile={
        'a':'课程名称',
        'b':'任课老师',
        'c':'考核方式',
    }
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        posts.append(dict_data)
    if request.method=='POST':
        db = connect_db()
        cur = db.cursor()
        sql='select * from jihuaxijie where coursename = %s'
        s=cur.execute(sql,(request.form['bbb']))
        if s !=0:
            z=cur.fetchmany(s)
            posts1 = []
            for value in z:
                dict_data = {}
                dict_data['课程名称'] = value[0]
                dict_data['任课老师'] = value[1]
                dict_data['考核方式'] = value[2]
                posts1.append(dict_data)
            flash(posts1)
        else:
            flash('未查询到...')
        return redirect(url_for('kecheng'))
    # print posts
    return render_template('student.html', posts=posts,titile=titile)

# 显示专业的函数页面
@app.route('/zhuanye', methods=['GET'])
def zhuanye():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    data = get_Table_Data('zhuanye')
    # 用列表的格式存放全部数据
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        dict_data['e'] = value[4]
        posts.append(dict_data)
    # print posts
    return render_template('student.html', posts=posts)

# 显示学生成绩页面
@app.route('/chengji', methods=['GET','POST'])
def chengji():
    if not session.get('logged_st'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    # 调用数据库函数，获取数据
    db = connect_db()
    cur = db.cursor()
    sql='select * from xueshengchengji where course_name = %s'
    s=cur.execute(sql,(session['logged_st']))
    data=cur.fetchmany(s)
    # 用列表的格式存放全部数据
    titile={
        'a':'学生学号',
        'b':'学生姓名',
        'c':'课程名称',
        'd':'学生成绩',
    }
    posts = []
    for value in data:
        dict_data = {}
        dict_data['a'] = value[0]
        dict_data['b'] = value[1]
        dict_data['c'] = value[2]
        dict_data['d'] = value[3]
        posts.append(dict_data)
    if request.method=='POST':
        db = connect_db()
        cur = db.cursor()
        sql='select * from xueshengchengji where course_name = %s'
        s=cur.execute(sql,(request.form['bbb']))
        if s!=0:
            z=cur.fetchmany(s)
            posts1 = []
            for value in z:
                dict_data = {}
                dict_data['学生学号'] = value[0]
                dict_data['学生姓名'] = value[1]
                dict_data['课程名称'] = value[2]
                dict_data['学生成绩'] = value[3]
                posts1.append(dict_data)
            flash(posts1)
        else:
            flash('未查询到...')
        return redirect(url_for('chengji'))
    # print posts
    return render_template('student.html', posts=posts,titile=titile)



@app.route('/add_jxjh', methods=['POST','GET'])
def add_jxjh():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'课程名称:',
        'b':'任课老师:',
        'c':'考核方式:',
        'add':'jxjh'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into jihuaxijie(coursename,coursetime,courseplan)VALUES(%s,%s,%s)'
    if request.method == 'POST':
        cur.execute(sql,(request.form['coursename'],request.form['coursetime'],request.form['courseplan']))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('jxjh'))

    return render_template('add.html',titile=titile)

@app.route('/add_guanliban', methods=['POST','GET'])
def add_guanliban():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'专业:',
        'b':'年级:',
        'c':'班级:',
        'add':'guanliban'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into guanliban(specialities,grade,class)VALUES(%s,%s,%s)'
    if request.method == 'POST':
        cur.execute(sql,(request.form['specialities'],request.form['grade'],request.form['class']))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('guanliban'))

    return render_template('add.html',titile=titile)

@app.route('/add_paike_js', methods=['POST','GET'])
def add_paike_js():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'课程名称:',
        'b':'课程教室:',
        'c':'课时时间:',
        'add':'paike_js'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into paike_js(course_name,course_class,course_plan)VALUES(%s,%s,%s)'
    if request.method == 'POST':
        cur.execute(sql,(request.form['course_name'],request.form['course_class'],request.form['course_plan']))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('paike_js'))

    return render_template('add.html',titile=titile)

@app.route('/add_xscj', methods=['POST','GET'])
def add_xscj():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'学生学号',
        'b':'学生姓名',
        'c':'课程名称',
        'd':'学生成绩',
        'add':'xscj'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into xueshengchengji(course_name,student_name,student_class,student_score)VALUES(%s,%s,%s,%s)'
    if request.method == 'POST':
        cur.execute(sql,(request.form['course_name'],request.form['student_name'],request.form['student_class'],request.form['student_score']))
        db.commit()
        db.close()
        flash('添加成功！')
        redirect(url_for('xscj'))

    return render_template('add.html',titile=titile)

@app.route('/add_xslb', methods=['POST','GET'])
def add_xslb():
    if not session.get('logged_th'):
        flash('请先登录，再访问页面...')
        return redirect(url_for('login'))
    error = None
    titile={
        'a':'学生姓名:',
        'b':'学生学号:',
        'c':'学生专业:',
        'd':'学生班级:',
        'add':'xslb'
    }
    db = connect_db()
    cur = db.cursor()
    sql='insert into xueshengleibie(name,number,specialities,class,password)VALUES(%s,%s,%s,%s,%s)'
    if request.method == 'POST':
        cur.execute(sql,(request.form['name'],request.form['number'],request.form['specialities'],request.form['class'],request.form['number']))
        db.commit()
        db.close()
        flash('添加成功!')
        redirect(url_for('xslb'))

    return render_template('add.html',titile=titile)


# 主函数
if __name__ == '__main__':
    # app.debug = True
    app.run()
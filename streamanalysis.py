from flask import Flask, render_template, request, session, jsonify,redirect
import datetime
import random
from flask_mail import Mail,Message
from DBConnection import Db
app = Flask(__name__)
app.secret_key = 'college_web'

staticpath = 'C:\\College_Web\\static\\'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'riss.anoopjayaprakash@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'riss.anoopjayaprakash@gmail.com'
app.config['MAIL_PASSWORD'] = 'anoop.nandana.anoop'
mail = Mail(app)


@app.route('/')
def login():
    try:
        return render_template("login.html")
    except:
        return render_template("login.html")

@app.route('/login_post', methods=['post'])
def login_post():
    username = request.form["textfield"]
    password = request.form["textfield2"]
    db = Db()
    qry = "select * from login WHERE username='" + username + "' and password='" + password + "'"
    res = db.selectOne(qry)
    if res != None:
        session['login_id'] = res['lid']
        session['lid'] = res['lid']
        type = res['type']
        if type == 'admin':
            return admin()
        elif type == 'subadmin':
            res = db.selectOne("SELECT * FROM subadmin WHERE sublid='" + str(res["lid"]) + "'")
            session["sub_img"]=res["photo"]
            session["sub_name"] = res["name"]
            return subadmin_home()

        elif type == 'student':
            res = db.selectOne("SELECT * FROM student WHERE slid='" + str(res["lid"]) + "'")
            session["std_img"] = res["photo"]
            session["std_name"] = res["sname"]
            return render_template("student/student_home.html")

        elif type == 'parent':
            res = db.selectOne("SELECT * FROM student WHERE slid='" + str(res["stlid"]) + "'")
            session["std_img"] = res["photo"]
            session["std_name"] = res["sname"]
            return render_template("student/student_home.html")

        elif type == 'hod':
            res = db.selectOne("SELECT * FROM staff WHERE staff_lid='" + str(res["lid"]) + "'")
            session["hod_img"] = res["photo"]
            session["hod_name"] = res["staff_name"]
            return render_template("hod/hod_home.html")

        elif type == 'parent':
            res = db.selectOne("SELECT * FROM parent WHERE plid='" + str(res["lid"]) + "'")
            session["par_img"] = res["photo"]
            session["par_name"] = res["pname"]
            session['lid'] = res['stlid']
            return render_template("parent/home.html")

        elif type == 'staff':
            res = db.selectOne("SELECT * FROM staff WHERE staff_lid='" + str(res["lid"]) + "'")
            session["stf_img"] = res["photo"]
            session["stf_name"] = res["staff_name"]
            return render_template("staff/home.html")

        else:
            return '''<script>alert('This user not allowed to login);window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/'</script>'''

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")


# --------------------------------------------------------------------------------------- admin

@app.route('/admin')
def admin():
    return render_template("admin/hm.html")

                                    #  sub admin management  #



@app.route('/admin_add_subadmin')
def admin_add_subadmin():
    return render_template("admin/sub_admin.html")


@app.route('/admin_add_subadmin_post', methods=['post'])
def admin_add_subadmin_post():
    name = request.form["textfield"]
    gender = request.form["radio"]
    phone = request.form["textfield2"]
    photo = request.files["fileField"]
    email = request.form["textfield3"]
    designation = request.form["textfield4"]
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save(staticpath + "subadmin\\" + dt + ".jpg")
    path = "/static/subadmin/" + dt + ".jpg"
    db = Db()
    password = random.randint(1000, 10000)
    msg = Message(subject="Your email and password",
                  sender=app.config.get("riss.anoopjayaprakash@gmail.com"),
                  recipients=[email],
                  body="Username : " + email + " & " + "Password : " + str(password))
    try:
        mail.send(msg)
    except:
        pass


    qry1 = "insert into login(username,password,type)values('" + email + "','" + str(password) + "','subadmin')"
    res1 = db.insert(qry1)
    qry = "INSERT INTO `subadmin`(sublid,`name`,`phone`,`email`,`designation`,`photo`,`gender`)VALUES('" + str(res1) + "','" + name + "','" + phone + "','" + email + "','" + designation + "','" + path + "','" + gender + "')"
    res = db.insert(qry)
    return '''<script>alert("sunadmin succesfully registerd");window.location="/admin_add_subadmin"</script>'''


@app.route('/sub_email_check', methods=['post'])
@app.route('/sub_email_check', methods=['post'])
def sub_email_check():
    db = Db()
    email = request.form['email']
    res = db.selectOne("select * from login where username='" + email + "'")
    if res != None:
        return jsonify(status='ok')
    else:
        return jsonify(status='not')


@app.route('/admin_view_subadmin')
def admin_view_subadmin():
    qry = "SELECT * FROM subadmin ORDER BY subadmin_id DESC"
    db = Db()
    res = db.select(qry)
    return render_template("admin/view subadmin.html", data=res)


@app.route('/admin_view_subadmin_post', methods=['post'])
def admin_view_subadmin_post():
    name=request.form['name']
    qry = "SELECT * FROM subadmin where name like'"+name+"%'"
    db = Db()
    res = db.select(qry)
    print(qry)
    return render_template("admin/view subadmin.html", data=res)


@app.route('/admin_dlt_subadmin/<id>')
def admin_dlt_subadmin(id):
    qry = "delete FROM subadmin where subadmin_id='" + str(id) + "'"
    db = Db()
    res = db.delete(qry)
    return admin_view_subadmin()


@app.route('/admin_edit_subadmin/<id>')
def admin_edit_subadmin(id):
    qry = "SELECT * FROM `subadmin` WHERE `subadmin_id`='" + str(id) + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("admin/edit_subadmin.html", data=res)


@app.route('/admin_edit_subadmin_post', methods=['post'])
def admin_edit_subadmin_post():
    name = request.form["textfield"]
    gender = request.form["radio"]
    phone = request.form["textfield2"]
    designation = request.form["textfield4"]
    db = Db()
    sid = request.form['id']
    if 'fileField' in request.files:
        photo = request.files["fileField"]
        if photo.filename != "":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            photo.save(staticpath + "subadmin\\" + dt + ".jpg")
            path = "/static/subadmin/" + dt + ".jpg"
            db = Db()
            qry = "UPDATE `subadmin` SET `name`='" + name + "',`phone`='" + phone + "',`designation`='" + designation + "',`photo`='" + path + "',`gender`='" + gender + "' WHERE `subadmin_id`='" + sid + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("updated succesfully");window.location="/admin_view_subadmin"</script>'''
        else:
            qry = "UPDATE `subadmin` SET `name`='" + name + "',`phone`='" + phone + "',`designation`='" + designation + "',`gender`='" + gender + "' WHERE `subadmin_id`='" + sid + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data entered succesfully");window.location="/admin_view_subadmin"</script>'''
    else:
        qry = "UPDATE `subadmin` SET `name`='" + name + "',`phone`='" + phone + "',designation`='" + designation + "',`gender`='" + gender + "' WHERE `subadmin_id`='" + sid + "'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data entered succesfully");window.location="/admin_view_subadmin"</script>'''




                                         #  department management  #



@app.route('/admin_add_dept')
def admin_add_dept():
    return render_template("admin/department.html")

@app.route('/depart_check', methods=['post'])
def depart_check():
    db = Db()
    dept = request.form['dept']
    res = db.selectOne("select * from department where department_name='" + dept + "'")
    print(dept)
    if res != None:
        return jsonify(status='ok')
    else:
        return jsonify(status='not')


@app.route('/admin_add_dept_post', methods=['post'])
def admin_add_dept_post():
    department_name = request.form["textfield"]
    db = Db()
    qry = "INSERT INTO `stream`(`department_name`)VALUES('" + department_name + "')"
    res = db.insert(qry)
    print(res)
    return render_template('admin/department.html')


@app.route('/admin_view_dept')
def admin_view_dept():
    qry = "SELECT * FROM stream ORDER BY did DESC"
    db = Db()
    res = db.select(qry)
    return render_template("admin/view department.html", data=res)


@app.route('/admin_delete_dept/<did>')
def admin_delete_dept(did):
    qry = "delete FROM department where did='" + did + "'"
    db = Db()
    res = db.delete(qry)
    return admin_view_dept()


@app.route('/admin_edit_dept/<did>')
def admin_edit_dept(did):
    qry = "SELECT * FROM `stream` WHERE `did`='" + did + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("admin/edit_dept.html", data=res)


@app.route('/admin_edits_post', methods=['post'])
def admin_edits_post():
    did = request.form['nn']
    department_name = request.form["textfield"]
    db = Db()
    qry = "UPDATE `stream` SET `department_name`='" + department_name + "' WHERE `did`='" + did + "' "
    res = db.update(qry)
    print(qry)
    return admin_view_dept()


@app.route('/admin_add_dept_search_post', methods=['post'])
def admin_add_dept_search_post():
    dept = request.form["name"]
    db = Db()
    qry = "SELECT * FROM `stream`WHERE `department_name` like '%" + dept + "%'"
    res = db.select(qry)
    return render_template("admin/view department.html", data=res)



                                          #  department hod management  #










@app.route('/admin_add_course')
def admin_add_course():
    c = Db()
    qry = "SELECT * FROM `stream`"
    res = c.select(qry)
    return render_template("admin/couse.html", data=res)


@app.route('/course_check', methods=['post'])
def course_check():
    db = Db()
    dept=request.form['dept']
    code = request.form['code']
    res = db.selectOne("select * from course where did='"+dept+"' and course_code='" + code + "'")
    if res != None:
        return jsonify(status='ok')
    else:
        return jsonify(status='not')

@app.route('/admin_add_course_post', methods=['post'])
def admin_add_course_post():
    department = request.form["select"]
    course_code = request.form["textfield"]
    course_name = request.form["textfield2"]

    db = Db()
    qry = "INSERT INTO course(`did`,`course_code`,`course_name`)VALUES ('" + department + "','" + course_code + "','" + course_name + "')"
    res = db.insert(qry)
    print(res)
    return admin_add_course()


@app.route('/admin_view_couse')
def admin_view_couse():
    qry = "SELECT course.*,stream.* from course INNER JOIN stream ON course.did=stream.did"
    c = Db()
    res = c.select(qry)
    return render_template("admin/view course.html", data=res)


@app.route('/admin_delete_course/<course_id>')
def admin_delete_course(course_id):
    qry = "delete FROM course where course_id='" + course_id + "'"
    db = Db()
    res = db.delete(qry)
    return admin_view_couse()


@app.route('/admin_edits_course/<course_id>')
def admin_edits_course(course_id):
    qry = "SELECT * FROM `course` WHERE `course_id`='" + course_id + "'"
    db = Db()
    res = db.selectOne(qry)

    qry3 = "SELECT `stream`.* FROM `stream`,`course` WHERE `course`.`did`=`stream`.`did` AND `course`.`course_id`='" + course_id + "'"
    db = Db()
    res3 = db.selectOne(qry3)

    qry12 = "SELECT * FROM stream"
    db = Db()
    res22 = db.select(qry12)
    return render_template("admin/edit_course.html", data=res, dd=res22, db=res3)


@app.route('/admin_edit_course_post', methods=['post'])
def admin_edit_course_post():
    department = request.form["select"]
    course_code = request.form["textfield"]
    course_name = request.form["textfield2"]

    db = Db()
    hh = request.form['hh']
    qry = "UPDATE `course` SET `did`='" + department + "',`course_code`='" + course_code + "',`course_name`='" + course_name + "'  WHERE `course_id`='" + hh + "'"
    res = db.update(qry)
    print(res)
    return admin_view_couse()


@app.route('/admin_add_course_search_post', methods=['post'])
def admin_add_course_search_post():
    dept = request.form["textfield"]
    db = Db()
    qry = "SELECT course.*, stream.*  from course INNER JOIN stream ON course.did=stream.did WHERE department_name='" + dept + "'"
    res = db.select(qry)
    return render_template("admin/view course.html", data=res)

@app.route('/admin_add_password')
def admin_add_password():
    return render_template("admin/password.html")


@app.route('/admin_add_password_post', methods=['post'])
def admin_add_password_post():
    current_password = request.form["textfield"]
    new_password = request.form["textfield2"]
    confirm_password = request.form["textfield3"]
    db = Db()
    qry = "SELECT * FROM login WHERE password='" + current_password + "'"
    res = db.selectOne(qry)
    if res != None:
        if (new_password == confirm_password):
            qry1 = "UPDATE login SET `password`='" + new_password + "' WHERE lid ='" + str(session['login_id']) + "' "
            db.update(qry1)
            return '''<script>alert("password created");window.location="/"</script>'''
        else:
            return '''<script>alert("new password and confirm password not matching");window.location="/admin_add_password"</script>'''
    else:
        return '''<script>alert("old password not matching");window.location="/admin_add_password"</script>'''


@app.route('/admin_add_sub_post', methods=['post'])
def admin_add_sub_post():
    sub = request.form["textfield"]
    db = Db()
    qry = "SELECT * from subadmin WHERE `name`LIKE '%" + sub + "%'"
    res = db.select(qry)
    return render_template("admin/view subadmin.html", data=res)


@app.route('/admin_add_punishment')
def admin_add_punishment():
    return render_template("admin/assignment.html")


@app.route('/admin_add_punishment_post', methods=['post'])
def admin_add_punishment_post():
    name = request.form["textfield"]
    photo = request.files["imageField"]
    reason = request.form["textfield2"]
    punishment = request.form["textfield3"]
    from_date = request.form["textfield4"]
    to_date = request.form["textfield5"]
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\assignment\\" + dt + ".jpg")
    path = "/static/assignment/" + dt + ".jpg"

    db = Db()
    qry = "INSERT INTO `assignment`(`slid`,`photo`,`reason`,`assignment`,`from_date`,`to_date`)VALUES('" + str(session[
                                                                                                                   'login_id']) + "','" + path + "','" + reason + "','" + punishment + "','" + from_date + "','" + to_date + "')"
    res = db.insert(qry)
    print(res)
    return 'ok'


@app.route('/admin_view_punishment')
def admin_view_punishment():
    qry = "SELECT `assignment`.*,`student`.`sname` FROM `assignment` INNER JOIN`student` ON `assignment`.`slid`=`student`.`slid`  "
    db = Db()
    res = db.select(qry)
    return render_template("admin/view assignment.html", data=res)


@app.route('/admin_add_punishment_search_post', methods=['post'])
def admin_add_punishment_search_post():
    frm = request.form["textfield"]
    to = request.form["textfield2"]
    db = Db()
    qry = "SELECT * FROM `assignment`WHERE `from_date`BETWEEN '" + frm + "' AND '" + to + "'"
    res = db.select(qry)
    return render_template("admin/view assignment.html", data=res)


@app.route('/admin_delete_punishment/<pid>')
def admin_delete_punishment(pid):
    qry = "delete FROM assignment where pid='" + pid + "'"
    db = Db()
    res = db.delete(qry)
    return admin_view_punishment()


@app.route('/admin_edit_punishment/<pid>')
def admin_edit_punishment(pid):
    qry = "SELECT * FROM `assignment` WHERE `pid`='" + pid + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("admin/punishment_edit.html", data=res)


@app.route('/admin_edit_punishment_post', methods=['post'])
def admin_edit_punishment_post():
    name = request.form["textfield"]
    photo = request.files["imageField"]
    reason = request.form["textfield2"]
    punishment = request.form["textfield3"]
    from_date = request.form["textfield4"]
    to_date = request.form["textfield5"]
    pun_id = request.form["pun_id"]

    db = Db()

    if 'imageField' in request.files:
        photo = request.files["imageField"]

        if photo.filename != "":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\assignment\\" + dt + ".jpg")
            path = "/static/assignment/" + dt + ".jpg"
            qry = "UPDATE `assignment` SET `name`='" + name + "',`photo`='" + path + "', `reason`='" + reason + "',`assignment`='" + punishment + "', `from_date`='" + from_date + "',`to_date`='" + to_date + "' WHERE `pid`='" + pun_id + "'"

            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited successfully");window.location="/admin_view_punishment"</script>'''
        else:
            db = Db()
            qry = "UPDATE `assignment` SET `name`='" + name + "',`photo`='" + path + "', `reason`='" + reason + "',`assignment`='" + punishment + "', `from_date`='" + from_date + "',`to_date`='" + to_date + "' WHERE `pid`='" + pun_id + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited succesfully");window.location="/admin_view_punishment"</script>'''
    else:
        db = Db()
        qry = "UPDATE `assignment` SET `name`='" + name + "',`reason`='" + reason + "',`assignment`='" + punishment + "',`from_date`='" + from_date + "',`to_date`='" + to_date + "' where `pid`='" + pun_id + "'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data edited succesfully");window.location="/admin_view_punishment"</script>'''


@app.route('/admin_add_fee')
def admin_add_fee():
    c = Db()
    qry = "SELECT * FROM `course`"
    res = c.select(qry)
    print(res)
    return render_template("admin/fee.html", data=res)


@app.route('/admin_view_fee')
def admin_view_fee():
    qry = "SELECT `fee`.*, `course`.`course_name` FROM `course` INNER JOIN `fee` ON `course`.`course_id`=`fee`.`cid`"
    db = Db()
    res = db.select(qry)
    return render_template("admin/viewfee.html", data=res)


@app.route('/admin_add_fee_search_post', methods=['post'])
def admin_add_fee_search_post():
    course = request.form["textfield"]
    db = Db()
    qry = "SELECT fee.*,course.* FROM `fee` INNER JOIN course ON fee.cid=course.course_id WHERE course_name LIKE '%" + course + "%'"
    res = db.select(qry)
    return render_template("admin/viewfee.html", data=res)


@app.route('/admin_add_fee_post', methods=['post'])
def admin_add_fee_post():
    course = request.form["select"]
    sem = request.form["select1"]
    fee = request.form["textfield3"]
    due_date = request.form["textfield4"]
    last_date = request.form["textfield5"]
    db = Db()
    qry = "INSERT INTO `fee`(`cid`,`sem`,`fee`,`due_date`,`late_date`)VALUES('" + course + "','" + sem + "','" + fee + "','" + due_date + "','" + last_date + "')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/admin_add_fee"</script>'''


@app.route('/admin_delete_fee/<fid>')
def admin_delete_fee(fid):
    qry = "delete FROM fee where fid='" + fid + "'"
    db = Db()
    res = db.delete(qry)
    return admin_view_fee()


@app.route('/admin_add_admin_home')
def admin_add_admin_home():
    return render_template("admin/admin_home.html")



























# ----------------------------subadmin------------------------------------------------------------


@app.route('/subadmin_home')
def subadmin_home():
    return render_template("subadmin/hm.html")



@app.route('/subadmin_add_notification')
def subadmin_add_notification():
    return render_template("subadmin/notification.html")


@app.route('/subadmin_view_notification')
def subadmin_view_notification():
    qry = "SELECT * FROM `notification` where lid=''"
    db = Db()
    res = db.select(qry)
    return render_template("subadmin/view notifation.html", data=res)


@app.route('/subadmin_add_notification_post', methods=['post'])
def subadmin_add_notification_post():
    title = request.form["textfield"]
    content = request.form["textarea"]

    db = Db()
    qry = "INSERT INTO `notification`(`lid`,`title`,`content`,`date`) VALUES('" + str(
        session['login_id']) + "','" + title + "','" + content + "',now())"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_notification"</script>'''


@app.route('/subadmin_delete_notification/<nid>')
def subadmin_delete_notification(nid):
    qry = "delete FROM notification where nid='" + nid + "'"
    db = Db()
    res = db.delete(qry)
    return subadmin_view_notification()


@app.route('/subadmin_edit_notification/<nid>')
def subadmin_edit_notification(nid):
    qry = "SELECT * FROM `notification` WHERE `nid`='" + nid + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("subadmin/notification_edit.html", data=res)


@app.route('/subadmin_edit_notification_post', methods=['post'])
def subadmin_edit_notification_post():
    not_id = request.form['n']
    title = request.form["textfield"]
    content = request.form["textarea"]
    date = request.form["textfield1"]
    db = Db()
    qry = "UPDATE `notification` SET `title`='" + title + "',`content`='" + content + "',`date`='" + date + "' WHERE `nid`='" + not_id + "' "
    res = db.update(qry)
    print(qry)
    return '''<script>alert('Updated');window.location='/subadmin_view_notification'</script>'''


@app.route('/subadmin_add_notification_search_post', methods=['post'])
def subadmin_add_notification_search_post():
    frm = request.form["textfield"]
    to = request.form["textfield1"]
    db = Db()
    qry = "SELECT * FROM `notification`WHERE `date` BETWEEN '" + frm + "' AND '" + to + "'"
    res = db.select(qry)
    return render_template("subadmin/view notifation.html", data=res)


@app.route('/subadmin_add_staff')
def subadmin_add_staff():
    qr = "SELECT * FROM `department`"
    d = Db()
    res = d.select(qr)
    return render_template("subadmin/staff.html", dept=res)


@app.route('/subadmin_add_staff_post', methods=['post'])
def subadmin_add_staff_post():
    staff_name = request.form["textfield"]
    dept = request.form["dept"]
    gender = request.form["radio"]
    dob = request.form["dob"]
    photo = request.files["imageField"]
    qualification = request.form["textfield2"]
    experience = request.form["textfield3"]
    contact = request.form["textfield4"]
    email = request.form["textfield5"]
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save(staticpath+"\\staff\\" + dt + ".jpg")
    path = "/static/staff/" + dt + ".jpg"
    db = Db()
    import random
    c=random.randint(0000, 99999)

    psw = str(c)
    qry1 = "INSERT INTO `login`(`username`,`password`,`type`)VALUE('" + email + "','" + psw + "','staff')"
    lid = db.insert(qry1)

    qry = "INSERT INTO `staff`(`staff_name`,`gender`,`dob`,`photo`,`qualification`,`experience`,`contact`,`email`,`staff_lid`,`did`) VALUES('" + staff_name + "','" + gender + "','" + dob + "','" + path + "','" + qualification + "','" + experience + "','" + contact + "','" + email + "','" + str(
        lid) + "','" + dept + "')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_staff"</script>'''


@app.route('/subadmin_view_staff')
def subadmin_view_staff():
    qry = "SELECT `staff`.*  FROM `staff`"
    db = Db()
    res = db.select(qry)
    return render_template("subadmin/view staff.html", data=res)


@app.route('/subadmin_delete_staff/<staff_id>')
def subadmin_delete_staff(staff_id):
    qry = "delete FROM staff where staff_id='" + staff_id + "'"
    db = Db()
    res = db.delete(qry)
    return subadmin_view_staff()


@app.route('/subadmin_edit_staff/<staff_id>')
def admin_edit_staff(staff_id):
    db = Db()
    qry = "SELECT * FROM `staff` WHERE `staff_id`='" + staff_id + "'"
    res = db.selectOne(qry)
    qry1 = "SELECT * FROM `department`"
    res1 = db.select(qry1)
    return render_template("subadmin/staff_edit.html", data=res, dept=res1)


@app.route('/subadmin_edit_staff_post', methods=['post'])
def subadmin_edit_staff_post():
    staff_name = request.form["textfield"]
    staffid = request.form['staffid']
    dept = request.form["dept"]
    gender = request.form["radio"]
    dob = request.form["dob"]

    qualification = request.form["textfield2"]
    experience = request.form["textfield3"]
    contact = request.form["textfield4"]
    email = request.form["textfield5"]
    if "imageField" in request.files:
        photo = request.files["imageField"]
        if photo.filename=="":
            db = Db()
            qry = "UPDATE `staff` SET `did`='" + dept + "',`staff_name`='" + staff_name + "',`gender`='" + gender + "',`dob`='" + dob + "',`qualification`='" + qualification + "',`experience`='" + experience + "',`contact`='" + contact + "',`email`='" + email + "' where `staff_id`='" + staffid + "'"
            res = db.update(qry)
        else:



            import datetime

            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            photo.save(staticpath+"\\staff\\" + dt + ".jpg")
            path = "/static/staff/" + dt + ".jpg"
            db = Db()
            qry = "UPDATE `staff` SET `did`='" + dept + "',`staff_name`='" + staff_name + "',`gender`='" + gender + "',`dob`='" + dob + "',`photo`='" + path + "',`qualification`='" + qualification + "',`experience`='" + experience + "',`contact`='" + contact + "',`email`='" + email + "' where `staff_id`='" + staffid + "'"
            res = db.update(qry)
            print(res)
    else:
        db = Db()
        qry = "UPDATE `staff` SET `did`='" + dept + "',`staff_name`='" + staff_name + "',`gender`='" + gender + "',`dob`='" + dob + "',`qualification`='" + qualification + "',`experience`='" + experience + "',`contact`='" + contact + "',`email`='" + email + "' where `staff_id`='" + staffid + "'"
        res = db.update(qry)
    return subadmin_view_staff()


@app.route('/subadmin_add_staff_search_post', methods=['post'])
def subadmin_add_staff_search_post():
    staff_name = request.form["textfield"]
    db = Db()
    qry = "SELECT `staff`.* FROM `staff`  WHERE `staff_name` like '%" + staff_name + "%'"
    res = db.select(qry)
    return render_template("subadmin/view staff.html", data=res)


@app.route('/subadmin_add_student')
def subadmin_add_student():
    c = Db()
    qry = "SELECT * FROM course"
    res = c.select(qry)
    return render_template("subadmin/student.html", data=res)

    return render_template("subadmin/student.html")


@app.route('/subadmin_student_post', methods=['post'])
def subadmin_add_student_post():
    sname = request.form["textfield"]
    gender = request.form["radio"]
    course = request.form["select"]

    sem = request.form["textfield2"]
    photo = request.files["imageField"]
    admission_no = request.form["textfield3"]
    dob = request.form["dob"]
    contact = request.form["textfield4"]
    email = request.form["textfield5"]
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save(staticpath+"\\student\\" + dt + ".jpg")
    path = "/static/student/" + dt + ".jpg"
    db = Db()

    import  random
    m=random.randint(100,10000)
    password= str(m)


    qry="INSERT INTO login (`username`,`password`,`type`) VALUES ('"+email+"','"+password+"','student')"
    lid=db.insert(qry)


    qry = "INSERT INTO `student`(`sname`,`gender`,`cid`,`sem`,`photo`,`admission_no`,`dob`,`contact`,`email`,slid) VALUES('" + sname + "','" + gender + "','" + course + "','" + sem + "','" + path + "','" + admission_no + "','" + dob + "','" + contact + "','" + email + "','"+str(lid)+"')"
    res = db.insert(qry)

    qry = "INSERT INTO login (`username`,`password`,`type`,stlid) VALUES ('" + email + "','" + str(m+200) + "','parent','"+str(lid)+"')"
    lid = db.insert(qry)


    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_student"</script>'''


@app.route('/subadmin_view_student')
def subadmin_view_student():
    qry = "SELECT *  FROM `student`"
    db = Db()
    res = db.select(qry)
    return render_template("subadmin/view student.html", data=res)


@app.route('/subadmin_delete_student/<sid>')
def subadmin_delete_student(sid):
    qry = "delete FROM student where sid='" + sid + "'"
    db = Db()
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/subadmin_view_student'</script>'''


@app.route('/subadmin_edit_student/<sid>')
def subadmin_edit_student(sid):
    qry = "SELECT * FROM `student` WHERE `sid`='" + sid + "'"
    db = Db()
    res = db.selectOne(qry)
    qry1 = "SELECT * FROM `course`"
    res1 = db.select(qry1)
    return render_template("subadmin/edit_student.html", data=res, dept=res1)


@app.route('/subadmin_edit_student_post', methods=['post'])
def subadmin_edit_student_post():
    sname = request.form["textfield"]
    s_id = request.form["sid"]
    gender = request.form["radio"]
    course = request.form["dept"]
    sem = request.form["textfield2"]

    admission_no = request.form["textfield3"]
    dob = request.form["dob"]
    contact = request.form["textfield4"]
    email = request.form["textfield5"]

    if "imageField" in request.files:
        photo = request.files["imageField"]
        if photo.filename=="":
            db=Db()
            qry = "UPDATE `student` SET `sname`='" + sname + "',`gender`='" + gender + "',`cid`='" + course + "',`sem`='" + sem + "',`admission_no`='" + admission_no + "',`dob`='" + dob + "',`contact`='" + contact + "',`email`='" + email + "' WHERE `sid`='" + s_id + "' "
            res = db.update(qry)
        else:



            db = Db()

            import datetime
            dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            photo.save(staticpath+"\\student\\" + dt + ".jpg")
            path = "/static/student/" + dt + ".jpg"

            qry = "UPDATE `student` SET `sname`='" + sname + "',`gender`='" + gender + "',`cid`='" + course + "',`sem`='" + sem + "',`photo`='" + path + "',`admission_no`='" + admission_no + "',`dob`='" + dob + "',`contact`='" + contact + "',`email`='" + email + "' WHERE `sid`='" + s_id + "' "
            res = db.update(qry)
            print(qry)
    else:
        db = Db()
        qry = "UPDATE `student` SET `sname`='" + sname + "',`gender`='" + gender + "',`cid`='" + course + "',`sem`='" + sem + "',`admission_no`='" + admission_no + "',`dob`='" + dob + "',`contact`='" + contact + "',`email`='" + email + "' WHERE `sid`='" + s_id + "' "
        res = db.update(qry)

    return '''<script>alert('Updated');window.location='/subadmin_view_student'</script>'''


@app.route('/subadmin_add_student_search_post', methods=['post'])
def subadmin_add_student_search_post():
    student = request.form["textfield"]
    db = Db()
    qry = "SELECT * FROM `student`WHERE `sname` like '%" + student + "%'"
    res = db.select(qry)
    return render_template("subadmin/view student.html", data=res)


@app.route('/subadmin_add_punishment/<slid>')
def subadmin_add_punishment(slid):


    return render_template("subadmin/assignment.html",slid=slid)


@app.route('/subadmin_add_punishment_post', methods=['post'])
def subadmin_add_punishment_post():
    slid=request.form["slid"]
    photo = request.files["imageField"]
    reason = request.form["textfield2"]
    punishment = request.form["textfield3"]
    from_date = request.form["textfield4"]
    to_date = request.form["textfield5"]
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    photo.save(staticpath+"assignment\\" + dt + ".jpg")
    path = "/static/assignment/" + dt + ".jpg"

    db = Db()
    qry = "INSERT INTO `assignment`(`slid`,`photo`,`reason`,`assignment`,`from_date`,`to_date`)VALUES('" + slid + "','" + path + "','" + reason + "','" + punishment + "','" + from_date + "','" + to_date + "')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert("data entered succesfully");window.location="/subadmin_add_punishment"</script>'''


@app.route('/subadmin_view_punishment')
def subadmin_view_punishment():
    qry = "SELECT assignment.*, student.sname  FROM assignment,student where `assignment`.`slid`=`student`.`sid`"
    db = Db()
    res = db.select(qry)
    return render_template("subadmin/view assignment.html", data=res)

@app.route('/subadmin_delete_punishment/<pid>')
def subadmin_delete_punishment(pid):
    qry = "delete FROM assignment where pid='" + pid + "'"
    db = Db()
    res = db.delete(qry)
    return subadmin_view_punishment()

@app.route('/subadmin_edit_punishment/<pid>')
def subadmin_edit_punishment(pid):
    qry = "SELECT * FROM `assignment` WHERE `pid`='" + pid + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("subadmin/punishment_edit.html", data=res)

@app.route('/subadmin_edit_punishment_post', methods=['post'])
def subadmin_edit_punishment_post():
    name = request.form["textfield"]
    photo = request.files["imageField"]
    reason = request.form["textfield2"]
    punishment = request.form["textfield3"]
    from_date = request.form["textfield4"]
    to_date = request.form["textfield5"]
    pun_id = request.form["pun_id"]

    db = Db()

    if 'imageField' in request.files:
        photo = request.files["imageField"]

        if photo.filename != "":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            photo.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\assignment\\" + dt + ".jpg")
            path = "/static/assignment/" + dt + ".jpg"

            qry = "UPDATE `assignment` SET `name`='" + name + "',`photo`='" + path + "', `reason`='" + reason + "',`assignment`='" + punishment + "', `from_date`='" + from_date + "',`to_date`='" + to_date + "' WHERE pid='" + pun_id + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited successfully");window.location="/subadmin_view_punishment"</script>'''
        else:
            db = Db()
            qry = "UPDATE `assignment` SET `name`='" + name + "',`photo`='" + path + "', `reason`='" + reason + "',`assignment`='" + punishment + "', `from_date`='" + from_date + "',`to_date`='" + to_date + "' WHERE pid='" + pun_id + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited succesfully");window.location="/subadmin_view_punishment"</script>'''
    else:
        db = Db()
        qry = "UPDATE `assignment` SET `name`='" + name + "',`reason`='" + reason + "',`assignment`='" + punishment + "',`from_date`='" + from_date + "',`to_date`='" + to_date + "' where pid='" + pun_id + "'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data edited succesfully");window.location="/subadmin_view_punishment"</script>'''


@app.route('/subadmin_add_punishment_search_post', methods=['post'])
def subadmin_add_punishment_search_post():
    frm = request.form["textfield"]
    to = request.form["textfield2"]
    db = Db()
    qry = "SELECT * FROM `assignment`WHERE `from_date`BETWEEN '" + frm + "' AND '" + to + "'"
    res = db.select(qry)
    return render_template("subadmin/view assignment.html", data=res)


@app.route('/subadmin_add_subadmin_home')
def admin_add_subadmin_home():
    return render_template("subadmin/subadmin_home.html")





















# ------------hod-------------------------------------

@app.route('/hod_home')
def hod_home():
    return render_template('hod/change_password.html')


@app.route('/hod_change_password')
def hod_change_password():
    return render_template('hod/change_password.html')


@app.route('/hod_change_password_post', methods=['post'])
def hod_change_password_post():
    current_password = request.form['textfield']
    new_password = request.form['textfield2']
    confirm_password = request.form['textfield3']

    db = Db()
    qry = "SELECT * FROM login WHERE lid='" + str(session['login_id']) + "'"
    print(qry)
    res = db.selectOne(qry)

    if res is not None:
        if confirm_password == new_password:
            qry1 = "UPDATE login SET `password`='" + confirm_password + "' WHERE lid='" + str(session['login_id']) + "'"
            db.update(qry1)
            return '''<script>alert('Password created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/hod_change_password'</script>'''
    else:
        return '''<script>alert('Please enter your current password');window.location='/hod_change_password'</script>'''


@app.route('/hod_add_staff')
def hod_add_staff():
    return render_template("hod/view staff.html")


@app.route('/hod_view_staff')
def hod_view_staff():
    db = Db()
    qry = 'select * from staff'
    res = db.select(qry)
    return render_template("hod/view staff.html", data=res)


@app.route('/hod_view_staff_search_post', methods=['post'])
def hod_view_staff_search_post():
    staffname = request.form["textfield"]
    db = Db()
    qry = "select * from staff where  staff_name like '%" + staffname + "%'"
    res = db.select(qry)
    return render_template("hod/view staff.html", data=res)


@app.route('/hod_edit_staff/<staff_id>')
def hod_edit_staff(staff_id):
    qry = "select * from staff where where staff_id='" + staff_id + "'"
    db = Db()
    res = db.selectone(qry)
    return


@app.route('/hod_delete_staff/<staff_id>')
def hod_delete_staff(staff_id):
    qry = "delete FROM staff where staff_id='" + staff_id + "'"
    db = Db()
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/hod_view_staff'</script>'''


@app.route('/hod_add_subject')
def hod_add_subject():
    db = Db()
    qry = "SELECT * FROM `course`"
    res = db.select(qry)
    return render_template("hod/subject.html", data=res)


@app.route('/hod_add_subject_post', methods=['post'])
def hod_add_subject_post():
    course = request.form['textfield']
    sem = request.form["textfield2"]
    subject_code = request.form["textfield3"]
    subject_name = request.form["textfield4"]
    db = Db()
    qry1 = "INSERT INTO `subject`(`cid`,`sem`,`sub_code`,`sub_name`) VALUES('" + course + "','" + sem + "','" + subject_code + "','" + subject_name + "')"
    res = db.insert(qry1)
    print(res)
    return '''<script>alert('Added Successfully');window.location='/hod_add_subject'</script>'''


@app.route('/hod_view_subject')
def hod_view_subject():
    c = Db()
    qry = "SELECT `subject`.*,`course`.`course_name` FROM `course` INNER JOIN `subject` ON `subject`.`cid`=`course`.`course_id`"
    res = c.select(qry)
    qry1 = "select * from course"
    res1 = c.select(qry1)
    return render_template("hod/view subject.html", data=res, data1=res1)


@app.route('/hod_view_subject_search', methods=['post'])
def hod_view_subject_search():
    course = request.form['select']
    db = Db()
    qry1 = "select * from course"
    res1 = db.select(qry1)
    qry = "SELECT `subject`.*,`course`.`course_name` FROM `course` INNER JOIN `subject` ON `subject`.`cid`=`course`.`course_id` WHERE `course`.`course_name` LIKE '%" + course + "%'"
    res = db.select(qry)
    return render_template("hod/view subject.html", data=res, data1=res1)


@app.route('/delete_subject/<sid>')
def delete_subject(sid):
    db = Db()
    qry = " DELETE FROM `subject` WHERE `sub_id` = '" + sid + "'"
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.locatio='/hod_view_subject'</script>'''


@app.route('/edit_subject/<sid>')
def edit_subject(sid):
    db = Db()
    qry = "SELECT * FROM `subject` WHERE `sub_id` ='" + sid + "'"
    res = db.selectOne(qry)

    qry1 = "select * from course"
    res1 = db.select(qry1)

    return render_template('hod/edit_subject.html', res=res, res1=res1)


@app.route('/edit_subject_post', methods=['post'])
def edit_subject_post():
    iid = request.form["id"]
    cid = request.form["textfield"]
    sem = request.form["textfield2"]
    sub_code = request.form["textfield3"]
    sub_name = request.form["textfield4"]
    db = Db()
    qry = "update subject set cid='" + cid + "',sem='" + sem + "' ,sub_code='" + sub_code + "',sub_name='" + sub_name + "' where sub_id='" + str(
        iid) + "'"
    res = db.update(qry)
    return '''<script>alert('update Successfully');window.location='/hod_view_subject'</script>'''


@app.route('/hod_add_staff_subject_allocation')
def hod_add_subject_allocation():
    c = Db()
    qry = "SELECT * FROM course"
    res = c.select(qry)
    qry1 = "select * from staff"
    res1 = c.select(qry1)
    qry2 = "select * from subject"
    res2 = c.select(qry2)
    return render_template("hod/staff subject allocation.html", data=res, res1=res1, res2=res2)


@app.route('/hod_add_staff_subject_allocation_post', methods=['post'])
def hod_add_staff_subject_allocation_post():
    course_name = request.form['textfield1']
    staff = request.form["textfield"]
    subject = request.form["textfield3"]
    semester = request.form['textfield2']
    db = Db()
    qry1 = "INSERT INTO `subject_allocation`(sub_id,staff_id) VALUES('" + subject + "','" + staff + "')"
    res = db.insert(qry1)
    print(res)
    return '''<script>alert('Added Successfully');window.location='/hod_add_staff_subject_allocation'</script>'''


@app.route('/hod_view_staff_subject_allocation')
def hod_view_staff_subject_allocation():
    c = Db()
    qry1 = "SELECT * FROM SUBJECT"
    res1 = c.select(qry1)
    qry = "SELECT `course`.`course_name`,`subject`.sub_name, `subject`.`sem`, staff.staff_name,staff.email,subject_allocation.alloc_id FROM  course INNER JOIN  SUBJECT ON `course`.`course_id`=`subject`.`cid` INNER JOIN subject_allocation ON `subject_allocation`.`sub_id`=`subject`.`sub_id` INNER JOIN  staff ON `staff`.`staff_id`=`subject_allocation`.`staff_id` "
    res = c.select(qry)
    return render_template("hod/view staff allocation.html", data=res, data1=res1
                           )


#
# @app.route('/hod_add_staff_subject_allocation_post')
# def hod_add_staff_subject_allocation_post():
#    return render_template("hod/staff subject allocation.html")

@app.route('/staff_subject_allocation_search', methods=['post'])
def staff_subject_allocation_search():
    select_sub = request.form['select']
    db = Db()
    qry1 = "SELECT * FROM SUBJECT"
    res1 = db.select(qry1)
    qry = "SELECT `course`.`course_name`,`subject`.sub_name, `subject`.`sem`, staff.staff_name,staff.email,subject_allocation.alloc_id FROM  course INNER JOIN  SUBJECT ON `course`.`course_id`=`subject`.`cid` INNER JOIN subject_allocation ON `subject_allocation`.`sub_id`=`subject`.`sub_id` INNER JOIN  staff ON `staff`.`staff_id`=`subject_allocation`.`staff_id` WHERE `subject`.`sub_name` LIKE '%" + select_sub + "%' "
    res = db.select(qry)
    return render_template("hod/view staff allocation.html", data=res, data1=res1)


@app.route('/delete_staff_allocate/<id>')
def delete_staff_allocate(id):
    db = Db()
    qry = "DELETE FROM `subject_allocation` WHERE `alloc_id`='" + id + "'"
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/hod_view_staff_subject_allocation'</script>'''


@app.route('/edit_staff_allocate/<id>')
def edit_staff_allocate(id):
    db = Db()
    qry = "SELECT * FROM `subject_allocation` WHERE `alloc_id` ='" + id + "'"
    res = db.selectOne(qry)
    qry1 = "SELECT * FROM course"
    res1 = db.select(qry1)
    qry2 = "select * from staff"
    res2 = db.select(qry2)
    qry3 = "select * from subject"
    res3 = db.select(qry3)
    return render_template('hod/edit_staff_sub_allocation.html', edit=res, data=res1, )


@app.route('/hod_add_timetable')
def hod_add_timetable():
    c = Db()
    qry = "SELECT * FROM course"
    res = c.select(qry)
    qry1 = "select * from subject"
    res1 = c.select(qry1)
    return render_template("hod/timetable.html", data=res, res1=res1)


@app.route('/hod_add_time_table_post', methods=['post'])
def hod_add_time_table_post():
    subject = request.form["textfield"]
    course = request.form["textfield1"]
    sem = request.form["textfield2"]
    day = request.form["textfield3"]
    hour = request.form["textfield4"]
    db = Db()
    qry1 = "INSERT INTO `time_table`(sub_id,day,hour,couse_id,sem) VALUES('" + subject + "','" + day + "','" + hour + "','" + course + "','" + sem + "')"
    res = db.insert(qry1)
    print(res)
    return '''<script>alert('Added Successfully');window.location='/hod_add_timetable'</script>'''


@app.route('/hod_add_complaints')
def hod_add_complaints():
    return render_template("hod/complaints.html")


@app.route('/hod_view_complaints')
def hod_view_complaints():
    return render_template("hod/complaints.html")


@app.route('/hod_add_complaints_post', methods=['post'])
def hod_add_complaints_post():
    complaint = request.form["textarea"]
    db = Db()
    qry1 = "INSERT INTO `complaint`(complint,date,status,replay,lid) VALUES('" + complaint + "',curdate(),'pending','pending','" + str(
        session['login_id']) + "')"
    res = db.insert(qry1)
    print(res)
    return '''<script>alert('send Successfully');window.location='/hod_add_complaints'</script>'''


@app.route('/hod_view_complaint')
def hod_view_complaint():
    db = Db()
    qry = "SELECT *  FROM complaint WHERE lid = '" + str(session['login_id']) + "'"
    res = db.select(qry)
    return render_template('hod/view complaints.html', data=res)


@app.route('/delete_send_complaint/<id>')
def delete_send_complaint(id):
    db = Db()
    qry = "DELETE FROM `complaint` WHERE cid = '" + id + "'"
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/hod_view_complaint'</script>'''


@app.route('/hod_add_notification')
def hod_add_notification():
    return render_template("hod/notification.html")


@app.route('/hod_view_notification')
def hod_view_notification():
    db=Db()
    qry="SELECT * FROM `notification` WHERE `lid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("hod/view notifation.html",data=res)


@app.route('/hod_delete_notification/<nid>')
def hod_delete_notification(nid):
    db=Db()
    qry="delete from `notification` WHERE `nid`='"+nid+"'"
    db.delete(qry)
    return "<script>alert('Notification deleted successfully');window.location='/hod_view_notification'</script>"

@app.route('/hod_add_notification_post',methods=['post'])
def hod_add_notification_post():
    title=request.form["textfield"]
    message=request.form["textarea"]

    qry="INSERT INTO `notification` (`lid`,`title`,`content`,`date`) VALUES ('"+str(session['lid'])+"','"+title+"','"+message+"',NOW())"
    db=Db()
    db.insert(qry)

    return "<script>alert('Notification added successfully');window.location='/hod_add_notification'</script>"


@app.route('/hod_add_feedback')
def hod_add_feedback():
    return render_template("hod/feedback.html")


@app.route('/hod_view_feedback')
def hod_view_feedback():
    return render_template("hod/feedback.html")


@app.route('/hod_add_feedback_post',methods=['post'])
def hod_add_feedback_post():
    db=Db()
    feedback=request.form["feedback"]
    qry="INSERT INTO `feedback`(`lid`,`feedback`,`type`,DATE) VALUES ('"+str(session["lid"])+"','"+feedback+"','',NOW())"
    db.insert(qry)
    return render_template("hod/feedback.html")


@app.route('/hod_add_hod_home')
def hod_add_hod_home():
    return render_template("hod/hod_home.html")































# ----------------------------------------student---------------------------


@app.route('/student_add_password')
def student_add_password():
    return render_template('student/password.html')


@app.route('/student_add_password_post', methods=['post'])
def student_add_password_post():
    cur_password = request.form['textfield']
    new_password = request.form['textfield2']
    con_password = request.form['textfield3']

    db = Db()
    qry = "SELECT * FROM login WHERE `password`='" + cur_password + "'"
    res = db.selectOne(qry)

    if res != None:
        if new_password == con_password:
            qry1 = "UPDATE login SET `password`='" + new_password + "' WHERE lid ='" + str(session['login_id']) + "'"
            res = db.update(qry1)
            return '''<script>alert('Password Created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/student_add_password'</script>'''
    else:
        return '''<script>alert('Please enter your current password');window.location='/student_add_password'</script>'''


@app.route('/student_view_note')
def student_view_note():
    qry = "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id`"
    db = Db()
    res = db.select(qry)
    return render_template("student/view notes.html", data=res)


@app.route('/student_notes_search_post', methods=['post'])
def student_notes_search_post():
    course = request.form["textfield"]
    db = Db()
    qry = "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id` WHERE `course_name`='" + course + "'"
    res = db.select(qry)
    return render_template("student/view notes.html", data=res)


@app.route('/student_send_complaint')
def student_send_complaints():
    return render_template('student/complaints.html')


@app.route('/student_send_complaint_post', methods=['post'])
def student_send_complaints_post():
    complaint = request.form["textarea"]
    db = Db()
    qry = "INSERT INTO complaint(`lid`,`type`,`complint`,`reply`,`date`,`status`) VALUES ('" + str(
        session['login_id']) + "','student','" + complaint + "','pending',CURDATE(),'pending')"
    db.insert(qry)
    return render_template('student/complaints.html')


@app.route('/student_view_complaint')
def student_view_complaints():
    qry = "SELECT * FROM complaint WHERE lid='" + str(session['login_id']) + "'"
    db = Db()
    res = db.select(qry)
    return render_template('student/viewassignment.html', data=res)


@app.route('/student_delete_complaint/<cid>')
def student_delete_complaint(cid):
    qry = "delete FROM complaint where cid='" + cid + "'"
    db = Db()
    res = db.delete(qry)
    return student_view_complaints()


@app.route('/student_view_timetable')
def student_view_timetable():
    q = "SELECT `slid`,`cid`,`sem` FROM `student` WHERE `student`.`slid`='" + str(session['login_id']) + "'"
    db = Db()
    resa = db.selectOne(q)
    if resa is not None:

        cid = resa['cid']
        sem = resa['sem']

        hr = ["1", "2", "3", "4", "5"]
        day = ["monday", "tuesday", "wednesday", "thursday", "friday"]

        a = []

        for i in day:

            f = []

            for k in hr:
                qry = "SELECT * FROM `time_table` where course_id='" + str(cid) + "' and sem='" + str(
                    sem) + "' and hour='" + k + "' and day='" + i + "'"
                res = db.selectOne(qry)
                if res is not None:

                    subid = str(res['sub_id'])
                    qry1 = "SELECT `sub_name` FROM `subject` WHERE `sub_id`='" + subid + "'"
                    res1 = db.selectOne(qry1)

                    f.append(res1['sub_name'])
                else:
                    f.append("Free")

            a.append(f)

        return render_template('student/view timetable.html', a=a)
    else:
        return render_template("student/student_home.html")


@app.route('/student_view_profile')
def student_view_pofile():
    qry = "SELECT * FROM `student` where slid='"+str(session['lid'])+"'"
    db = Db()
    i = db.selectOne(qry)
    return render_template('student/student profile.html', i=i)


@app.route('/student_send_feedback')
def student_send_feedback():
    return render_template('student/feedback.html')


@app.route('/student_send_feedback_post', methods=['post'])
def student_send_feedback_post():
    feedback = request.form["textarea"]
    db = Db()
    qry = "INSERT INTO feedback(`lid`,`feedback`,`date`,`type`) VALUES ('" + str(
        session['login_id']) + "','" + feedback + "',CURDATE(),'student')"
    db.insert(qry)
    return '''<script>alert('feedback send');window.location='/student_send_feedback'</script>'''


@app.route('/student_add_student_home')
def student_add_student_home():
    return render_template("student/student_home.html")


@app.route('/student_view_notification')
def student_view_notification():
    qry = "SELECT * FROM `notification`"
    db = Db()
    res = db.select(qry)
    return render_template("student/view notifation.html", data=res)

@app.route("/staffaddclass")
def staffaddclass():
    db=Db()
    qry1 = "select * from course"
    res1 = db.select(qry1)
    return render_template("staff/staff_addclasses.html",data1=res1)


@app.route("/staffviewclass")



@app.route("/staffaddclasspost",methods=['post'])
def staffaddclasspost():
    cid=request.form["course"]
    sem=request.form["semester"]
    date=request.form["date"]
    link=request.form["link"]
    qry="INSERT INTO `classes` (`crsid`,`sem`,`link`,`date`,`slid`) VALUES ('"+cid+"','"+sem+"','"+link+"',NOW(),'"+str(session['lid'])+"')"
    db=Db()
    db.insert(qry)
    return "<script>alert('Classes added successfully');window.location='/staffaddclass'</script>"


@app.route('/staffviewclass')
def staffviewclass():
    qry="SELECT `classes`.*,`course`.* FROM `classes` INNER JOIN `course` ON `classes`.`crsid`=`course`.`course_id` WHERE `classes`.`slid`='"+str(session['lid'])+"'"
    db=Db()
    res=db.select(qry)
    return render_template('staff/viewclass.html',res=res)


@app.route("/staffdeleteclass/<id>")
def staffdeleteclass(cid):
    db=Db()
    qry="DELETE FROM `classes` WHERE `classid`='"+cid+"'"
    db.delete(qry)
    return "<script>alert('Deleted Successfully');window.location='/staffviewclass'</script>"


@app.route('/student_view_attendance_post', methods=['post'])
def student_view_attendance_post():
    year = request.form["select"]
    month = request.form["select2"]

    sid = str(session["login_id"])

    hr = ["1", "2", "3", "4", "5"]

    db = Db()
    attendence = []
    for i in range(1, 32):
        f = year + "-" + month + "-" + str(i)
        aa = []
        for i in hr:

            qry = "SELECT  slid FROM `attendance` WHERE `slid`='" + sid + "' and year(date)='" + year + "' and month(date)='" + month + "' and date='" + f + "' and hour='" + str(
                i) + "'"

            res = db.selectOne(qry)
            if res is not None:
                print(qry)
                aa.append("P")
            else:
                aa.append("A")
        attendence.append(aa)

    print(res)
    print("-------------------------------------------------")
    print(attendence)
    return render_template('student/attendance view.html', data=attendence, cnt=len(attendence))


@app.route('/student_view_internal_mark')
def student_view_internal_mark():
    # qry="select * from internal_mark"
    # db=Db()
    # res=db.select(qry)
    return render_template('student/view internal mark.html')


@app.route('/student_view_internal_mark_post', methods=['post'])
def student_view_internal_mark_post():
    sem = request.form["select"]
    db = Db()
    qry = "SELECT `internal_mark`.*, `subject`.`sub_name` FROM `subject` INNER JOIN `internal_mark` ON `internal_mark`.`subid`=`subject`.`sub_id` WHERE slid='" + str(
        session['login_id']) + "' and subject.sem='" + sem + "'"
    res = db.select(qry)
    print(res)

    return render_template('student/view internal mark.html', data=res)


@app.route('/student_viewpunishment')
def student_viewpunishment():
    db = Db()
    qry = "SELECT * FROM `assignment` WHERE slid='" + str(session["login_id"]) + "'"
    res = db.select(qry)

    return render_template("student/view_punishment.html", res=res)





















#----------------------------------------------------------staffs-------------------------------------
@app.route('/staff_add_password')
def staff_add_password():
    return render_template('staff/password.html')
@app.route('/staff_add_password_post', methods=['post'])
def staff_add_password_post():
    cur_password = request.form['textfield']
    new_password = request.form['textfield2']
    con_password = request.form['textfield3']

    db = Db()
    qry = "SELECT * FROM login WHERE  lid='"+str(session['lid'])+"' and `password`='" + cur_password + "'"
    res = db.selectOne(qry)

    if res is not  None:
        if new_password == con_password:
            qry1 = "UPDATE login SET `password`='" + new_password + "' WHERE lid ='" + str(session['login_id']) + "'"
            res = db.update(qry1)
            return '''<script>alert('Password Created');window.location='/'</script>'''
        else:
            return '''<script>alert('Password mismatch');window.location='/'</script>'''
    else:
        return '''<script>alert('Please enter your current password');window.location='/'</script>'''


@app.route('/staff_addinternalmark/<subid>')
def staff_addinternalmark(subid):
    db = Db()
    qry = "SELECT `student`.*,`course`.`course_name` FROM `student` INNER JOIN `course` ON `student`.`cid`=`course`.`course_id`"
    res = db.select(qry)
    return render_template("staff/addinternalmark.html",data=res,subid=subid)

@app.route('/staff_viewinternalmark/<subid>')
def staff_viewinternalmark(subid):
    db = Db()
    qry="SELECT student.*,`internal_mark`.`mark` FROM student INNER JOIN `internal_mark` ON `internal_mark`.`slid`=`student`.`slid` WHERE `internal_mark`.`subid`='"+subid+"'"
    res=db.select(qry)
    return  render_template("staff/viewmarks.html",data=res)



@app.route('/staff_Addmark_post',methods=['post'])
def staff_Addmark_post():

    subid=request.form["subid"]
    db = Db()
    slid=request.form.getlist("id")
    a=request.form.getlist("mark")

    for i in range (len(a)):
        qry="INSERT INTO `internal_mark` (`slid`,`subid`,`mark`) VALUES ('"+ slid[i] +"','"+subid+"','"+a[i]+"')"
        db.insert(qry)

    return "<script>alert('Mark added successfully');window.location='/staff_viewassignedsubject'</script>"




@app.route('/staff_viewnotification')
def staffviewnotification():
    db = Db()
    qry = "select * from notification"
    res = db.select(qry)

    return render_template("staff/viewnotification.html", data=res)


@app.route('/staff_viewassignedsubject')
def staff_viewassignedsubject():
    db = Db()
    qry = "SELECT subject.*,`course`.`course_code`,`course`.`course_name` FROM SUBJECT INNER JOIN `subject_allocation` ON `subject`.`sub_id`=`subject_allocation`.`sub_id` INNER JOIN `staff` ON `staff`.`staff_id`=`subject_allocation`.`staff_id` INNER JOIN `course` ON `course`.`course_id`=`subject`.`cid` WHERE `staff`.`staff_lid`='" + str(
        session["login_id"]) + "'"
    res = db.select(qry)

    return render_template("staff/viewallocatedsubject.html", data=res)


@app.route('/staff_add_notes')
def staff_add_notes():
    qry = "select * from subject"
    db = Db()
    res = db.select(qry)
    qry1 = "select * from course"
    res1 = db.select(qry1)

    return render_template("staff/uploadnotes.html", data=res, data1=res1)


@app.route('/staff_add_notes_post', methods=['post'])
def staff_add_notes_post():
    subject = request.form['select']
    note = request.form['textfield']
    file = request.files['fileField']
    course = request.form['select2']
    import datetime
    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    file.save(staticpath+"notes\\" + dt + ".pdf")
    path = "/static/notes/" + dt + ".pdf"
    qry = "INSERT INTO `notes` (`sub_id`,`course_id`,`notes`,`description`,`staff_lid`) VALUES ('" + subject + "','" + course + "','" + path + "','" + note + "','" + str(
        session['login_id']) + "')"
    db = Db()
    res = db.insert(qry)
    return "<script>alert('notes uploaded succesfully');window.location='/staff_add_notes'</script>"


@app.route('/staff_view_note')
def staff_view_note():
    qry = "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id`"
    db = Db()
    res = db.select(qry)
    return render_template("staff/view notes.html", data=res)


@app.route('/staff_notes_search_post', methods=['post'])
def staff_notes_search_post():
    course = request.form["textfield"]
    db = Db()
    qry = "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id` WHERE `course_name`='" + course + "'"
    res = db.select(qry)
    return render_template("staff/view notes.html", data=res)


@app.route('/staff_delete_note/<note_id>')
def staff_delete_note(note_id):
    qry = "delete FROM notes where note_id='" + note_id + "'"
    db = Db()
    res = db.delete(qry)
    return '''<script>alert('Deleted');window.location='/staff_view_note'</script>'''


@app.route('/staff_edit_note/<note_id>')
def staff_edit_note(note_id):
    qry = "SELECT `notes`.*, `course`.`course_name`, `subject`.`sub_name` FROM `subject` INNER JOIN `notes` ON `notes`.`sub_id`=`subject`.`sub_id` INNER JOIN `course` ON `course`.`course_id`=`notes`.`course_id` where notes.note_id='" + note_id + "'"
    db = Db()
    res = db.selectOne(qry)
    qry1 = "select * from subject"
    res1 = db.select(qry1)
    qry2 = "select * from course"
    res2 = db.select(qry2)

    return render_template("staff/edit note.html", data=res, data1=res1, data2=res2)


@app.route('/staff_edit_note_post', methods=['post'])
def staff_edit_note_post():
    subject = request.form['select']
    note = request.form['textfield']
    file = request.files['fileField']
    course = request.form['select2']
    nid = request.form['nid']
    db = Db()

    if 'filefield' in request.files:
        file = request.files["imageField"]

        if file.filename != "":
            import datetime
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
            file.save("C:\\Users\\shuha\\PycharmProjects\\College_Web\\static\\notes\\" + dt + ".pdf")
            path = "/static/notes/" + dt + ".pdf"

            qry = "UPDATE `notes` SET `sub_id`='" + subject + "',`course_id`='" + course + "',`notes`='" + path + "', `description`='" + note + "' WHERE note_id='" + nid + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited successfully");window.location="/staff_view_note"</script>'''
        else:
            db = Db()
            qry = "UPDATE `notes` SET `sub_id`='" + subject + "',`course_id`='" + course + "',`notes`='" + path + "', `description`='" + note + "' WHERE note_id='" + nid + "'"
            res = db.update(qry)
            print(res)
            return '''<script>alert("data edited succesfully");window.location="/staff_view_note"</script>'''
    else:
        db = Db()
        qry = "UPDATE `notes` SET `sub_id`='" + subject + "',`course_id`='" + course + "',`description`='" + note + "' WHERE note_id='" + nid + "'"
        res = db.update(qry)
        print(res)
        return '''<script>alert("data edited succesfully");window.location="/staff_view_note"</script>'''


@app.route('/staff_send_feedback')
def staff_send_feedback():
    return render_template('staff/feedback.html')


@app.route('/staff_send_feedback_post', methods=['post'])
def staff_send_feedback_post():
    feedback = request.form["textarea"]
    db = Db()
    qry = "INSERT INTO feedback(`lid`,`feedback`,`date`,`type`) VALUES ('" + str(
        session['login_id']) + "','" + feedback + "',CURDATE(),'staff')"
    db.insert(qry)
    return '''<script>alert('feedback send');window.location='/staff_send_feedback'</script>'''


@app.route('/staff_view_timetable')
def staff_view_timetable():
    qry = "SELECT `subject`.`sub_name`,`time_table`.`day`,`time_table`.`hour`,`subject_allocation`.`staff_id`,`course`.`sem`,`course`.`course_name` FROM `subject` INNER JOIN `subject_allocation` ON `subject`.`sub_id`=`subject_allocation`.`sub_id` INNER JOIN `time_table` ON `subject`.`sub_id`=`time_table`.`sub_id` INNER JOIN `staff` ON `staff`.`staff_id`=`subject_allocation`.`staff_id` INNER JOIN `course` ON `course`.`course_id`=`subject`.`cid`WHERE `staff`.`staff_lid`='" + str(
        session['login_id']) + "'"
    print(qry)
    db = Db()
    res = db.select(qry)
    return render_template('staff/staff timetable.html', data=res)


@app.route('/staff_view_punishment')
def staff_view_punishment():
    qry = "SELECT * FROM assignment"
    db = Db()
    res = db.select(qry)
    return render_template("staff/view assignment.html", data=res)


@app.route('/staff_view_student')
def staff_view_student():
    db = Db()
    qry = "SELECT `student`.*,`course`.`course_name` FROM `student` INNER JOIN `course` ON `student`.`cid`=`course`.`course_id`"
    res = db.select(qry)

    return render_template("staff/view student.html", data=res)











@app.route('/studentchat')
def studentchat():
    return render_template("student/fur_chat.html")

@app.route("/studentchatview",methods=['post'])
def studentchatview():
    db=Db()
    res=db.select("SELECT * FROM staff")
    return jsonify(data=res)

@app.route('/webviewmsg/<sid>')
def webviewmsg(sid):
    a=str(session["lid"])

    qry="SELECT * FROM chat  WHERE ( (from_id='"+a+"' AND to_id='"+sid+"') OR (from_id='"+sid+"' AND to_id='"+a+"') )"
    db=Db()
    res= db.select(qry)
    return jsonify(data=res)


@app.route('/web_insert_chat/<sid>/<msg>')
def web_insert_chat(sid,msg):
    a=str(session["lid"])

    qry="insert into `chat` (`date`,`from_id`,`to_id`,`message`) values (now(),'"+a+"','"+sid+"','"+msg+"')"
    db=Db()
    res= db.insert(qry)
    return jsonify(status="ok")














@app.route('/staffchat')
def staffchat():
    return render_template("staff/fur_chat.html")

@app.route("/staffchatview",methods=['post'])
def staffchatview():
    db=Db()
    res=db.select("SELECT * FROM student")
    return jsonify(data=res)






# --------------------------parent------------------









@app.route("/staffviewprofile")
def staffviewprofile():
    db=Db()
    qry="SELECT * FROM `staff` WHERE `staff_lid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("/staff/profile.html",data=res)

@app.route("/staffaddexam")
def staffaddexam():
    qry="select * from course"
    db=Db()
    res=db.select(qry)
    return render_template('/staff/staff_addexam.html',data=res)

@app.route("/staffaddexampost",methods=['post'])
def staffaddexampost():

    cid=request.form["course"]
    exam=request.form["examname"]
    date=request.form["date"]
    semester=request.form["semester"]

    db=Db()
    qry="INSERT INTO `exam` (`examname`,`cid`,`sem`,`date`,`slid`) VALUES ('"+exam+"','"+cid+"','"+semester+"',CURDATE(),'"+str(session['lid'])+"')"
    db.insert(qry)
    return "<script>alert('Exam added successfully');window.location='/staffaddexam'</script>"



@app.route("/staffaddvideo")
def staffaddvideo():
    qry="select * from course"
    db=Db()
    res=db.select(qry)
    return render_template('/staff/staff_addvideo.html',data=res)

@app.route("/staffaddvideopost",methods=['post'])
def staffaddvideopost():
    cid=request.form["course"]
    title=request.form["title"]

    semester=request.form["semester"]
    file=request.files["file"]
    path="C:\\College_Web\\static\\videos\\"
    import time
    timestr = time.strftime("%Y%m%d%H%M%S")

    file.save(path+timestr+file.filename)

    p="/static/videos/"+timestr+file.filename



    db=Db()
    qry="INSERT INTO `videos` (`title`,`filename`,`crsid`,`sem`,`date`,`slid`) VALUES ('"+title+"','"+p+"','"+cid+"','"+semester+"',CURDATE(),'"+str(session['lid'])+"')"
    db.insert(qry)

    return "<script>alert('Vedio uploaded successfully');window.location='/staffaddexam'</script>"

@app.route("/staffvieweam")
def staffviewexam():
    db=Db()
    qry="select exam.*,course.* from exam inner join course on `course`.`course_id`=`exam`.`cid` where slid='"+str(session['lid'])+"'"
    res=db.select(qry)
    return  render_template("/staff/staff_viewexam.html",data=res)


@app.route("/staffdeleteexam/<examid>")
def staffdeleteexam(examid):
    db=Db()
    qry="delete from exam where examid='"+examid+"'"
    db.delete(qry)
    return "<Script>alert('Exam deleted successfully');window.location='/staffvieweam'</script>"



@app.route("/staffviewvideos")
def staffviewvideos():
    db=Db()
    qry="SELECT `videos`.*,`course`.* FROM `videos` INNER JOIN `course` ON `course`.`course_id`=`videos`.`crsid` WHERE `videos`.`slid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("staff/viewvedios.html",res=res)


@app.route("/studentvedios")
def studentvedios():
    db=Db()
    qry="SELECT `videos`.*,`course`.* ,staff.* FROM `videos` INNER JOIN `course` ON `course`.`course_id`=`videos`.`crsid` INNER JOIN `staff` ON `staff`.`staff_lid`=`videos`.`slid`  INNER JOIN student ON  `student`.`cid`=`course`.`course_id`  WHERE `student`.`slid`='"+str(session['lid'])+"'"
    print(qry)
    res=db.select(qry)
    return render_template("student/viewvedios.html",res=res)




@app.route("/deletevedio/<id>")
def deletevedio(id):
    qry="DELETE FROM `videos` WHERE `vid`='"+id+"'"
    db=Db()
    db.delete(qry)
    return "<Script>alert('Vedio deleted successfully');window.location='/staffviewvideos'</script>"




@app.route("/staffaddquestions/<examid>")
def staaddquestions(examid):
    return render_template("/staff/Staff_addquestions.html",id=examid)


@app.route("/staffaddquestionspost",methods=['POST'])
def staffaddquestionspost():
    question=request.form["question"]
    option1=request.form["option1"]
    option2=request.form["option2"]
    option3=request.form["option3"]
    option4=request.form["option4"]
    c=request.form["answer"]
    examid=request.form["id"]
    db=Db()

    qry="INSERT INTO `questions` (`question`,`op1`,`op2`,`op3`,`op4`,`answer`,`examid`)  VALUES ('"+question+"','"+option1+"','"+option2+"','"+option3+"','"+option4+"','"+c+"','"+examid+"')"
    db.insert(qry)
    return "<script>alert('Question added successfully');window.location='/staffaddquestions/"+examid+"'</script>"

@app.route("/staffviewquestions/<examid>")
def staffviewquestions(examid):
    db=Db()
    qry="SELECT * FROM `questions` WHERE `examid`='"+examid+"'"
    res=db.select(qry)
    return render_template("/staff/staff_viewquestions.html",res=res)


@app.route('/staffdeletequestons/<examid>/<qid>')
def staffdeletequestons(examid,qid):
    db=Db()
    qry="delete from questions where qid='"+qid+"'"
    db.delete(qry)
    return "<Script>alert('Question deleted successfully');window.location='/staffviewquestions/"+examid+"'</script>"

@app.route("/staffaddassignment")
def staffaddassignment():
    qry="select * from course"
    db=Db()
    res=db.select(qry)
    return render_template('/staff/staff_addassignment.html',data=res)

@app.route("/staffaddassignmentpost",methods=['post'])
def staffaddassignmentpost():

    cid=request.form["course"]
    exam=request.form["assignment"]
    date=request.form["date"]
    semester=request.form["semester"]

    db=Db()
    qry="INSERT INTO `assignement` (`assignmentname`,`crsid`,`sem`,`date`,`lastdate`,`slid`)  VALUES ('"+exam+"','"+cid+"','"+semester+"',CURDATE(),'"+date+"','"+str(session['lid'])+"')"
    db.insert(qry)
    return "<script>alert('Assignment addes successfully');window.location='/staffaddassignment'</script>"


@app.route("/staffviewassignemnt")
def staffviewassignment():

    db=Db()
    qry="select `assignement`.*, `course`.`course_code`,`course`.`course_name` FROM `assignement` INNER JOIN `course` ON `assignement`.`crsid`=`course`.`course_id` where slid='"+str(session['lid'])+"'"
    res=db.select(qry)
    return  render_template('staff/staff_viewassignement.html',data=res)


@app.route("/staffviewdeleteassignment/<aid>")
def staffviewdeleteassignment(aid):
    db=Db()
    qry="delete from `assignement` where assid='"+aid+"'"
    db.delete(qry)
    return "<script>alert('Assignment deleted successfully');window.location='/staffviewassignemnt'</script>"


@app.route('/studentaskdoubt')
def studentaskdoubt():
    db=Db()
    qry="SELECT `staff`.* FROM `staff` INNER JOIN `course` ON `course`.`did`=`staff`.`did` INNER JOIN `student` ON `student`.`cid`=`course`.`course_id` WHERE `student`.`slid`='"+str(session['lid'])+"'"
    res=db.select(qry)


    qry="SELECT `doubt`.*,`staff`.* FROM `staff` INNER JOIN `doubt` ON `doubt`.`stfflid`=`staff`.`staff_lid` WHERE `doubt`.`slid`='"+str(session['lid'])+"'"
    resa=db.select(qry)



    return render_template("/student/studentaskdoubts.html",data=res,d=resa)


@app.route("/studentviewassignment")
def studentviewassignment():
    db=Db()
    qry="SELECT `assignement`.*,`course`.*,staff.* FROM `assignement` INNER JOIN `course` ON `course`.`course_id`=`assignement`.`crsid` INNER JOIN staff ON `assignement`.`slid`=`staff`.`staff_lid` INNER JOIN `student` ON `student`.`cid`=`assignement`.`crsid` WHERE `assignement`.`sem`=`student`.`sem` AND `student`.`slid`='"+str(session['lid'])+"' AND `assignement`.`assid` NOT IN (SELECT  assid FROM asssubmission WHERE slid='"+str(session['lid'])+"' )"
    data=db.select(qry)
    return render_template("student/viewassignment.html",data=data)



@app.route("/studentviewexamsa")
def studentviewexamsa():
    qry="SELECT `exam`.*,`course`.* FROM exam INNER JOIN course ON `course`.`course_id`=`exam`.`cid` INNER JOIN `student` ON `student`.`cid`=`course`.`course_id` WHERE `student`.`slid`='"+str(session['lid'])+"'"
    db=Db()
    res=db.select(qry)
    return render_template("student/viewexam.html",data=res)


@app.route("/studentviewassignmentuploaded")
def studentviewassignmentuploaded():
    db=Db()
    qry="SELECT `assignement`.*,`course`.*,staff.*,filename FROM `assignement` INNER JOIN `course` ON `course`.`course_id`=`assignement`.`crsid` INNER JOIN staff ON `assignement`.`slid`=`staff`.`staff_lid` INNER JOIN `student` ON `student`.`cid`=`assignement`.`crsid`  inner join `asssubmission` ON `asssubmission`.`assid`=`assignement`.`assid`  WHERE `assignement`.`sem`=`student`.`sem` AND `student`.`slid`='"+str(session['lid'])+"' AND `assignement`.`assid`"
    data=db.select(qry)
    return render_template("student/viewassignmentuploaded.html",data=data)




@app.route('/studentupload/<assid>')
def studentupload(assid):
    return render_template("student/upload.html",assid=assid)

@app.route("/studentuploadpost",methods=['post'])
def studentuploadpost():
    id=request.form["assid"]
    file=request.files["file"]

    db=Db()

    dt = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M-%S")
    file.save(staticpath + "assignment\\" + dt + file.filename)
    path = "/static/assignment/" + dt + file.filename

    qry="INSERT INTO `asssubmission` (`assid`,`slid`,`filename`,`date`) VALUES ('"+id+"','"+str(session['lid'])+"','"+path+"',NOW())"
    db.insert(qry)
    return "<script>alert('Assignment Uploaded Successfully');window.location='/studentviewassignment'</script>"





@app.route('/studentaskdoubtpost',methods=['post'])
def studentaskdoubtpost():
    db=Db()
    doubt=request.form["doubt"]
    sid=request.form["sid"]

    qry="INSERT INTO `doubt` (`slid`,`stfflid`,`doubt`,`date`,`reply`) VALUES ('"+str(session['lid'])+"','"+sid+"','"+doubt+"',NOW(),'pending')"
    db=Db()
    db.insert(qry)
    return "<script>alert('Doubt sent successfully');window.location='/studentaskdoubt'</script>"












@app.route("/studentviewexams")
def studentviewexams():
    db=Db()
    qry="SELECT `course`.*,`assignement`.* FROM `assignement` INNER JOIN `course` ON `assignement`.`crsid`=`course`.`course_id` INNER JOIN `student` ON `student`.`cid`=`course`.`course_id` WHERE `student`.`sem`=`assignement`.`sem` AND `student`.`slid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("/student/viewexams.html",data=res)


@app.route("/apply/<examid>")
def apply(examid):
    session["examid"]=examid
    session["qid"]="0"
    session["mark"]="0"

    qry="SELECT `questions`.* FROM `questions` WHERE examid='"+examid+"' AND qid > 0 ORDER BY qid ASC"
    db=Db()
    res=db.select(qry)
    if len(res)>0:
        i=res[0]
        session["qid"]=i['qid']
        return render_template("/student/attendexam.html",i=res[0])
    else:

        return "<script>alert('Exam Finished');window.location='/studentviewexamsa'</script>"


@app.route("/nextquestions")
def nextquestions():



    qry="SELECT `questions`.* FROM `questions` WHERE examid='"+str(session['examid'])+"' AND qid > "+str(session['qid'])+" ORDER BY qid ASC"
    db=Db()
    res=db.select(qry)
    if len(res)>0:
        i=res[0]
        session["qid"]=i['qid']
        return render_template("/student/attendexam.html",i=res[0])
    else:
        qry="INSERT INTO `exammarks` (`examid`,`mark`,`slid`) VALUES ('"+str(session['examid'])+"','"+str(session['mark'])+"','"+str(session["lid"])+"')"
        db=Db()
        db.insert(qry)
        return "<script>alert('Exam finished');window.location='/studentviewexamsa'</script>"



@app.route("/answer",methods=['post'])
def ans():
    answer= request.form["radio"]
    db=Db()
    qry="SELECT * FROM `questions` WHERE `qid`='"+str(session['qid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        correctanswer=""
        if res['answer']==1:
            correctanswer=res['op1']
        elif res['answer']==2:
            correctanswer=res['op2']
        elif res['answer']==3:
            correctanswer=res['op3']
        elif res['answer']==4:
            correctanswer=res['op4']

        if correctanswer== answer:
            m=int(session["mark"])
            m=m+1
            session["mark"]=str(m)

    return redirect('/nextquestions')


@app.route("/studentviewmarks")
def studentviewmarks():
    db=Db()
    qry="SELECT `exam`.*,`course`.*,`exammarks`.* FROM `exammarks` INNER JOIN `exam` ON `exam`.`examid`=`exammarks`.`examid` INNER JOIN `course` ON `course`.`course_id`=`exam`.`cid` WHERE `exammarks`.`slid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("student/viewmarks.html",d=res)

@app.route("/staffviewdoubts")
def staffviewdoubts():
    qry="SELECT `doubt`.*,`student`.* FROM student INNER JOIN doubt ON `student`.`slid`=`doubt`.`slid` WHERE `stfflid`='"+str(session['lid'])+"'"
    db=Db()
    res=db.select(qry)
    return  render_template("staff/viewdoubts.html", data=res)

@app.route("/staffrep/<id>")
def staffrep(id):
    return render_template("staff/sentreply.html",id=id)

@app.route("/staffsentdoubtreply",methods=['post'])
def staffsentdoubtreply():
    id=request.form["id"]
    reply=request.form["doubt"]
    db=Db()
    qry="UPDATE `doubt` SET `reply`='"+reply+"' WHERE doubtid='"+id+"'"
    db.update(qry)
    return "<script>alert('Reply sent successfully');window.location='/staffviewdoubts'</script>"


if __name__ == '__main__':
    app.run(debug=True,port=3308)

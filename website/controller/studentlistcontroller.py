import json
import os
from datetime import datetime
from flask import Blueprint, render_template, request, flash, jsonify
from website import db
from website.model.student import Student
import re

template_dir = os.path.abspath('website/view')
student = Blueprint('student', __name__, template_folder=template_dir)


@student.route('/', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.order_by(Student.id).paginate(page=page, per_page=5)
    return render_template("studentlistview.html", pagination=pagination)


@student.route('/delete-student', methods=['POST'])
def delete_student():
    current_student = json.loads(request.data)
    Id = current_student['id']
    student = Student.query.get(Id)
    if student:
        db.session.delete(student)
        db.session.commit()

    return jsonify({})

@student.route('/add-student', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        id = request.form.get('id')
        frstname = request.form.get('frstname')
        lstname = request.form.get('lstname')
        email = request.form.get('email')
        birthday = datetime.strptime(request.form.get('birthday'), "%Y-%m-%d")
        birthplace = request.form.get('birthplace')
        point = request.form.get('point')

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        errors = False

        if not id.isnumeric():
            flash('ID should be a numberic!', category='error')
            errors = True
        else:
            student = Student.query.get(id)
            if student:
                flash('This student is existed!', category='error')
                errors = True

        if not point.isnumeric():
            flash('Point should be a numberic!', category='error')
            errors = True

        if not re.fullmatch(regex, email):
            flash('Invalid email!', category='error')
            errors = True

        if not errors:
            new_student = Student(id=id, frstname=frstname, lstname=lstname, email=email, birthday=birthday,
                                  birthplace=birthplace, point=point)
            db.session.add(new_student)
            db.session.commit()
            flash('Student added!', category='success')
    return render_template("studentaddview.html")

@student.route('/edit-student', methods=['POST', 'GET'])
def edit_student():
    if request.method == 'POST':
        new_id = request.args.get('id')
        new_frstname = request.form.get('frstname')
        new_lstname = request.form.get('lstname')
        new_email = request.form.get('email')
        str_birth = request.form.get('birthday')
        str_birth = str_birth[:10]
        new_birthday = datetime.strptime(str_birth, "%Y-%m-%d")
        new_birthplace = request.form.get('birthplace')
        new_point = request.form.get('point')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        errors = False

        student = Student.query.filter_by(id=new_id).first()
        student.frstname = new_frstname
        student.lstname = new_lstname
        student.email = new_email
        student.birthday = new_birthday
        student.birthplace = new_birthplace
        student.point = new_point

        if not new_point.isnumeric():
            flash('Point should be a numberic!', category='error')
            errors = True

        if not re.fullmatch(regex, new_email):
            flash('Invalid email!', category='error')
            errors = True

        if not errors:

            db.session.commit()
            flash('Student updated!', category='success')
    else:
        edit_id = request.args.get('id')
        student = Student.query.filter_by(id=edit_id).first()

    return render_template("studenteditview.html",student=student)


from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from app import db
from app.models import Course, Lesson


course_bp = Blueprint('courses', __name__)

@course_bp.route('/courses')
@login_required
def course_list():
    courses = Course.query.all()
    return render_template('courses/list.html', courses=courses)


@course_bp.route('/courses/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('courses/detail.html', course=course)

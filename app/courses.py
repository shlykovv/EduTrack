from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import Course, Lesson, LessonProgress


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


@course_bp.route('/course/<int:course_id>/subscribe')
@login_required
def subscribe(course_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.courses:
        current_user.courses.append(course)
        db.session.commit()
        flash(f'Вы записались на курс "{course.title}".')
    else:
        flash('Вы уже записаны на этот курс.')
    return redirect(url_for('profile.dashboard'))


@course_bp.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(user_id=current_user.id, lesson_id=lesson_id, completed=True)
        db.session.add(progress)
    else:
        progress.completed = not progress.completed
    
    db.session.commit()
    flash('Прогресс обновлён.')
    return redirect(request.referrer or url_for('courses.course_list'))

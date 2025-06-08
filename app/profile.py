from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import Course, LessonProgress
from app.forms import EditProfileForm, ChangePasswordForm


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.all()
    progress_map = {}
    
    for course in courses:
        course_progress = {}
        for lesson in course.lessons:
            progress = LessonProgress.query.filter_by(
                user_id=current_user.id, lesson_id=lesson.id
            ).first()
            course_progress.append({
                'lesson': lesson,
                'completed': progress.completed if progress else False
            })
        progress_map[course] = course_progress
    
    return render_template('profile/dashboard.html', progress_map=progress_map)


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Профиль обновлен')
        return redirect(url_for('profile.dashboard'))
    return render_template('profile/edit_profile.html', form=form)


@profile_bp.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Пароль обновлён.')
            return redirect(url_for('profile.dashboard'))
        else:
            flash('Старый пароль неверен.')
    return render_template('profile/change_password.html', form=form)

from app.models import Course, LessonProgress


def get_course_progress(user_id: int, course: Course):
    total_lessons = len(course.lessons)
    if total_lessons == 0:
        return 0
    completed = LessonProgress.query.filter(
        LessonProgress.user_id == user_id,
        LessonProgress.completed == True,
        LessonProgress.lesson_id.in_([l.id for l in course.lessons])
    ).count()
    result = int((completed / total_lessons) * 100)
    print(result)
    return result
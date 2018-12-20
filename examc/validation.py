import textx.exceptions as exceptions
from textx.scoping.tools import get_location
from textx import get_children_of_type


def check_exam(exam):
    min_dur = exam.get_points()
    if exam.duration < min_dur:
        raise exceptions.TextXSemanticError(
            'duration ({}) too short (< sumPoints {})'.format(
              exam.duration, exam.get_points()
            ), *get_location(exam))

    max_dur = exam.get_points() * 100 / 80
    max_dur = max(max_dur, exam.get_points()+5)
    if exam.duration > max_dur:
        raise exceptions.TextXSemanticError(
            'duration ({}) too long (> f(sumPoints) {})'.format(
                exam.duration, max_dur
            ), *get_location(exam))

    for exercise_ref in get_children_of_type('PExerciseRef', exam):
        exercise = exercise_ref.ref
        if len(list(filter(
                lambda x: x==exercise, exam.get_exercises()))) > 1:
            raise exceptions.TextXSemanticError(
                'exercise {} used more than once'.format(
                    exercise.name
                ), *get_location(exercise_ref))


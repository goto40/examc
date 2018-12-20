from examc.metamodel import init_metamodel, get_all
from os.path import dirname, join
from pytest import raises
import textx.exceptions as exceptions

def test_verification_exam_time():
    mm, repo, config = init_metamodel(join(dirname(__file__), "..", "examples"))

    with(raises(exceptions.TextXSemanticError, match=r'too long')):
        mm.model_from_file(join(dirname(
            __file__), join(dirname(__file__), "..",
                            "examples", "Probe03_too_long_time.exam")))

    with(raises(exceptions.TextXSemanticError, match=r'too short')):
        mm.model_from_file(join(dirname(
            __file__), join(dirname(__file__), "..",
                            "examples", "Probe03_too_short_time.exam")))


def test_verification_exam_double_exercise():
    mm, repo, config = init_metamodel(join(dirname(__file__), "..", "examples"))

    with(raises(exceptions.TextXSemanticError, match=r'used more than once')):
        mm.model_from_file(join(dirname(
            __file__), join(dirname(__file__), "..",
                            "examples", "Probe03_double_exercise.exam")))

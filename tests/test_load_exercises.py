from examc.metamodel import init_metamodel
from os.path import dirname, join


def test_load_exam():
    mm, repo, config = init_metamodel(join(dirname(__file__),
                                           "..", "examples"))

    assert mm is not None
    assert repo is not None

    exam = mm.model_from_file(join(dirname(__file__),
                                   join(dirname(__file__), "..",
                                        "examples", "Probe01.exam")))
    assert exam.get_points() == 9

    exam = mm.model_from_file(join(dirname(__file__),
                                   join(dirname(__file__), "..",
                                        "examples", "Probe02.exam")))
    assert exam.get_points() == 18

    exam = mm.model_from_file(join(dirname(__file__),
                                   join(dirname(__file__), "..",
                                        "examples", "Probe03.exam")))
    assert exam.get_points() == 22

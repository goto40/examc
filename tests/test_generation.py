from examc.metamodel import init_metamodel
from os.path import dirname, join
from examc.generator import generate_csv
import csv


def test_generation():
    mm, repo, config = init_metamodel(join(dirname(__file__),
                                           "..", "examples"))

    exam = mm.model_from_file(join(dirname(__file__),
                                   join(dirname(__file__), "..",
                                        "examples", "Probe03.exam")))

    fn = "src-gen/test.csv"
    generate_csv(exam, fn)
    with open(fn, 'r') as csvfile:
        r = csv.reader(csvfile)

        row = r.__next__()
        assert next is not None
        assert row[1] == 'uebung.vererbung2'
        assert row[2] == 'uebung.funktionaufloesung1'
        assert row[3] == 'uebung.mehrfach_vererbung1'
        assert row[4] == 'uebung.raii1'

        row = r.__next__()
        assert next is not None
        assert row[1] == '1'
        assert row[2] == '2'
        assert row[3] == '3'
        assert row[4] == '4'

        row = r.__next__()
        assert next is not None
        assert row[1] == '4'
        assert row[2] == '4'
        assert row[3] == '4'
        assert row[4] == '10'

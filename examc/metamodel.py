from textx import metamodel_from_file, get_children_of_type, get_metamodel
import textx.scoping.providers as scoping_providers
from textx.scoping import GlobalModelRepository, MetaModelProvider
from os.path import dirname, abspath, join


class ModelBase(object):
    def __init__(self):
        pass

    def _init_xtextobj(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class PExam(ModelBase):
    def __init__(self, **kwargs):
        super(PExam, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_exercises(self):
        from textx.scoping.tools import textx_isinstance
        mm = get_metamodel(self)
        lst = list(filter(
            lambda x: textx_isinstance(x.content, mm['PExerciseRef']),
            self.exercises_or_raw_content))
        return list(map(lambda x: x.content.ref, lst))

    def get_points(self):
        return sum(map(lambda x: x.points, self.get_exercises()))


def init_metamodel(path):
    this_folder = dirname(abspath(__file__))

    global_repo = GlobalModelRepository()
    global_repo_provider = scoping_providers.FQNGlobalRepo(
        glob_args={"recursive": True})
    global_repo_provider.register_models(path+"/**/*.exercise")

    mm_exercise = metamodel_from_file(join(this_folder, "Exercise.tx"),
                                      global_repository=global_repo,
                                      use_regexp_group=True)
    mm_exercise.register_obj_processors({
        "MYFLOAT": lambda x: float(x),
        "MYINT": lambda x: int(x),
    })

    mm_exam = metamodel_from_file(join(this_folder, "Exam.tx"),
                                  global_repository=global_repo,
                                  use_regexp_group=True,
                                  classes=[PExam])
    mm_exam.register_scope_providers({
        "*.*": global_repo_provider,
    })

    MetaModelProvider.clear()
    MetaModelProvider.add_metamodel("*.exercise", mm_exercise)
    MetaModelProvider.add_metamodel("*.exam", mm_exam)

    return (mm_exam, global_repo_provider.load_models_in_model_repo().
            all_models)


def get_all(model_repo, what="PExercise"):
    lst = []
    for m in model_repo.filename_to_model.values():
        lst = lst + get_children_of_type(what, m)
    return lst

from textx import metamodel_from_file, get_children_of_type
import textx.scoping.providers as scoping_providers
from textx.scoping import GlobalModelRepository, MetaModelProvider
from os.path import dirname, abspath, join
import examc.mm_classes as cl

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
                                  classes=[cl.PExam])
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

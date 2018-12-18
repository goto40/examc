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
    global_repo_provider.register_models(path+"/**/*.config")

    exam_classes = [cl.PExam,
                   ]
    exercise_classes = [
        cl.PExam,
        cl.PExercise,
        cl.PAsciiContent,
        cl.PCodeContent,
        cl.PFreeSpaceContent,
        cl.PImage,
        cl.PLatexContent,
        cl.PPlantUmlContent
    ]

    mm_exercise = metamodel_from_file(join(this_folder, "Exercise.tx"),
                                      global_repository=global_repo,
                                      use_regexp_group=True,
                                      classes=exercise_classes)

    mm_exercise.register_obj_processors({
        "MYFLOAT": lambda x: float(x),
        "MYINT": lambda x: int(x),
    })

    mm_exam = metamodel_from_file(join(this_folder, "Exam.tx"),
                                  global_repository=global_repo,
                                  use_regexp_group=True,
                                  referenced_metamodels=[mm_exercise],
                                  classes=exam_classes)
    mm_exam.register_scope_providers({
        "*.*": global_repo_provider,
    })


    mm_config = metamodel_from_file(join(this_folder, "Config.tx"),
                                      global_repository=global_repo,
                                      use_regexp_group=True)

    print("PSTRING-exerc:" + str(mm_exercise['PSTRING'])+ "--" + str(mm_exercise))
    print("PSTRING-exam:" + str(mm_exam['PSTRING'])+ "--" + str(mm_exam))

    MetaModelProvider.clear()
    MetaModelProvider.add_metamodel("*.exercise", mm_exercise)
    MetaModelProvider.add_metamodel("*.exam", mm_exam)
    MetaModelProvider.add_metamodel("*.config", mm_config)

    all_models = global_repo_provider.load_models_in_model_repo().\
        all_models
    configs = get_all(all_models, what='Config')

    if len(configs) > 1:
        raise Exception("found more than one config: {}".format(
            "and ".join(map(lambda  x: x._tx_filename, configs))))
    if len(configs) != 1:
        raise Exception("found no config")

    return mm_exam, all_models, configs[0]


def get_all(model_repo, what="PExercise"):
    lst = []
    for m in model_repo.filename_to_model.values():
        lst = lst + get_children_of_type(what, m)
    return lst

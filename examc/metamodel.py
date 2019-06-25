from textx import metamodel_from_file, get_children_of_type, register_language, clear_language_registrations
import textx.scoping.providers as scoping_providers
from textx.scoping import GlobalModelRepository
from os.path import dirname, abspath, join
import examc.mm_classes as cl
import examc.validation as validation


def init_metamodel(path):
    this_folder = dirname(abspath(__file__))

    global_repo = GlobalModelRepository()
    global_repo_provider = scoping_providers.FQNGlobalRepo(
        glob_args={"recursive": True})
    global_repo_provider.register_models(path+"/**/*.config")

    all_classes = [
        cl.PExam,
        cl.PExamContentContainer,
        cl.PExerciseRef,
        cl.PExercise,
        cl.PAsciiContent,
        cl.PCodeContent,
        cl.PFreeSpaceContent,
        cl.PImage,
        cl.PLatexContent,
        cl.PPlantUmlContent
    ]

    mm_exercise = metamodel_from_file(
        join(this_folder, "Exercise.tx"),
        global_repository=global_repo,
        use_regexp_group=True,
        classes=all_classes)

    mm_exercise.register_obj_processors({
        "MYFLOAT": lambda x: float(x),
        "MYINT": lambda x: int(x),
    })

    def name2file(name):
        return name.replace(".", "/")+".exercise"

    mm_exam = metamodel_from_file(join(this_folder, "Exam.tx"),
                                  global_repository=global_repo,
                                  use_regexp_group=True,
                                  classes=all_classes)
    mm_exam.register_scope_providers({
        "*.*": global_repo_provider,
        "dummy.dummy": scoping_providers.FQNImportURI(
            importURI_converter=name2file,
            search_path=[path]),
    })

    mm_exam.register_obj_processors({
        "MYFLOAT": lambda x: float(x),
        "MYINT": lambda x: int(x),
        "PExam": validation.check_exam
    })

    mm_config = metamodel_from_file(join(this_folder, "Config.tx"),
                                    global_repository=global_repo,
                                    use_regexp_group=True)

    clear_language_registrations()
    register_language("exam-exercise-lang","*.exercise", metamodel=mm_exercise)
    register_language("exam-lang","*.exam", metamodel=mm_exam)
    register_language("exam-config-lang","*.config", metamodel=mm_config)

    all_models = global_repo_provider.load_models_in_model_repo().\
        all_models
    configs = get_all(all_models, what='Config')

    if len(configs) > 1:
        raise Exception("found more than one config: {}".format(
            "and ".join(map(lambda x: x._tx_filename, configs))))
    if len(configs) != 1:
        raise Exception("found no config")

    return mm_exam, all_models, configs[0]


def get_all(model_repo, what="PExercise"):
    lst = []
    for m in model_repo.filename_to_model.values():
        lst = lst + get_children_of_type(what, m)
    return lst

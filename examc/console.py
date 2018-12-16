import argparse
from examc.metamodel import init_metamodel, get_all
from textx import get_model
from examc.generator import generate_tex
from os.path import join

def examc():
    parser = argparse.ArgumentParser(description='examc')
    parser.add_argument('--in-folder', dest='in_folder', default=".", type=str,
                        help='folder where to look for model data')
    parser.add_argument('-o', '--out-folder', dest='out_folder', default="src-gen", type=str,
                        help='out folder')
    parser.add_argument('-l', '--list-exercises', dest='list_exercises',
                        default=False, action='store_true',
                        help='show list of exercises')
    parser.add_argument('-e', '--exam', dest='generate_exam', type=str, default=None,
                        help='generate exam documents')

    args = parser.parse_args()
    if args.generate_exam is not None:
        generate_exam(inpath=args.in_folder,
                      outpath=args.out_folder,
                      exam=args.generate_exam)
    elif args.list_exercises:
        show_list(path=args.in_folder)


def generate_exam(inpath, outpath, exam_fn):
    mm, model_repo = init_metamodel(inpath)
    exam = mm.model_from_file(exam_fn)
    generate_tex(exam, join(outpath, "out.tex"), False)

def show_list(path):
    mm, model_repo = init_metamodel(path)
    print("list of exercises:")

    for e in get_all(model_repo, what="PExercise"):
        print("{:<30}: {:<30} from {}".format(
            e.name,
            e.points,
            get_model(e)._tx_filename
        ))


if __name__ == "__main__":
    examc()

import argparse
from examc.metamodel import init_metamodel, get_all
from textx import get_model


def examc():
    parser = argparse.ArgumentParser(description='examc')
    parser.add_argument('--in-folder', dest='in_folder', default=".", type=str,
                        help='folder where to look for model data')
    parser.add_argument('-l', '--list-exercises', dest='list_exercises', default=True,
                        action='store_true', help='show list of exercises')

    args = parser.parse_args()
    if args.list_exercises:
        show_list(path=args.in_folder)


def show_list(path):
    mm, model_repo = init_metamodel(path)
    print("list of exercises:")

    for e in get_all(model_repo, what="PExercise"):
        print("{:<30}: {:<30} from {}".format(
            e.name,
            e.points,
            get_model(e)._tx_filename
        ))


if __name__=="__main__":
    examc()

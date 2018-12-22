import argparse
import subprocess
from examc.generator import generate_exam
import sys


def examc():
    parser = argparse.ArgumentParser(description='examc')
    parser.add_argument('-I', '--in-folder', dest='in_folder',
                        default=None, type=str,
                        help='folder where to look for model data')
    parser.add_argument('-o', '--out-folder', dest='out_folder',
                        default="src-gen", type=str,
                        help='out folder')
    parser.add_argument('-x', '--execute-latex', dest='execute_latex',
                        action='store_true', default=False,
                        help='execute latex after document generation')
    parser.add_argument(
        'model_files', metavar='model_files', type=str, nargs='+',
        help='model filenames')

    args = parser.parse_args()
    for model_file in args.model_files:
        try:
            mypath, myscript = generate_exam(inpath=args.in_folder,
                                             outpath_base=args.out_folder,
                                             exam_fn=model_file)
            if args.execute_latex:
                subprocess.call(["sh", myscript], cwd=mypath)
        except Exception as err:
            sys.exit("in {}".format(model_file) + "\n" + str(err))


if __name__ == "__main__":
    examc()

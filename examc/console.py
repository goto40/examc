import argparse
import subprocess
from examc.metamodel import init_metamodel
from examc.generator import generate_tex, generate_pu_files, \
    generate_script, generate_csv
from os.path import join, exists, abspath, dirname
from os import makedirs


def examc():
    parser = argparse.ArgumentParser(description='examc')
    parser.add_argument('-I', '--in-folder', dest='in_folder',
                        default=None, type=str,
                        help='folder where to look for model data')
    parser.add_argument('-o', '--out-folder', dest='out_folder',
                        default="src-gen", type=str,
                        help='out folder')
    parser.add_argument('-e', '--exam', dest='generate_exam', type=str,
                        default=None, help='generate exam documents')
    parser.add_argument('-x', '--execute-latex', dest='execute_latex',
                        action='store_true', default=False,
                        help='execute latex after document generation"\
                             "(only applicable with -e)')

    args = parser.parse_args()
    if args.generate_exam is not None:
        mypath, myscript = generate_exam(inpath=args.in_folder,
                                         outpath_base=args.out_folder,
                                         exam_fn=args.generate_exam)
        if args.execute_latex:
            subprocess.call(["sh", myscript], cwd=mypath)
    elif args.list_exercises:
        infolder = args.in_folder
        if infolder is None:
            infolder = "."
        show_list(path=infolder)


def generate_exam(inpath, outpath_base, exam_fn):
    if inpath is None:
        inpath = abspath(dirname(exam_fn))
    mm, model_repo, config = init_metamodel(inpath)
    exam = mm.model_from_file(exam_fn)
    outpath = join(outpath_base, exam.name)
    if not exists(outpath):
        makedirs(outpath)

    generate_tex(exam, config,
                 join(outpath, exam.name+".tex"), False)
    generate_tex(exam, config,
                 join(outpath, exam.name+"_solution.tex"), True)
    generate_pu_files(exam, outpath)

    myscript = join(outpath, "generate.sh")
    generate_script(exam, myscript)

    generate_csv(exam, join(outpath, exam.name+".csv"))

    return abspath(outpath), abspath(myscript)


if __name__ == "__main__":
    examc()

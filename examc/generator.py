import jinja2
from os.path import dirname, abspath, join
from functools import reduce
from os import makedirs
from os.path import exists
from examc.metamodel import init_metamodel


def _generate_pu_files(exam, out_dir):
    for exercise in exam.get_exercises():
        for pu in exercise.get_pu_contents():
            out_file_name = join(out_dir, pu.basename()+".pu")
            with open(out_file_name, 'w') as f:
                f.write(pu.render())


def _generate_tex(exam, config, out_file_name="src-gen/out.tex",
                  generate_solution=False):
    this_folder = dirname(abspath(__file__))
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)
    template = jinja_env.get_template('master.tex.template')
    with open(out_file_name, 'w') as f:
        f.write(template.render(exam=exam, config=config,
                                generate_solution=generate_solution,
                                solution=str(generate_solution).lower()))


def _generate_script(exam, out_file_name):
    script = "#build\n"
    for exercise in exam.get_exercises():
        for pu in exercise.get_pu_contents():
            script = script + f"plantuml {pu.basename()}.pu && \\"
    script = script + f'''
pdflatex {exam.name}.tex && \
pdflatex {exam.name}.tex && \
pdflatex {exam.name}_solution.tex && \
pdflatex {exam.name}_solution.tex
#xdg-open {exam.name}.pdf
#xdg-open {exam.name}_solution.pdf'''
    with open(out_file_name, 'w') as f:
        f.write(script)


def generate_csv(exam, out_file_name="src-gen/out.csv"):
    exercises = exam.get_exercises()
    outpath = dirname(out_file_name)
    if not exists(outpath):
        makedirs(outpath)

    csv_num = "num:," + \
              reduce(lambda x, y: x + "," + y,
                     map(lambda x: str(x.get_num(exam)),
                         exercises)) + "\n"
    csv_titles = "title:," + \
                 reduce(lambda x, y: x + "," + y,
                        map(lambda x: x.basename(exam),
                            exercises)) + "\n"
    csv_points = "points:," + \
                 reduce(lambda x, y: x + "," + y,
                        map(lambda x: str(x.points),
                            exercises)) + "\n"

    csv_text = csv_titles + csv_num + csv_points
    with open(out_file_name, 'w') as f:
        f.write(csv_text)


def generate_exam(inpath, outpath_base, exam_fn):
    if inpath is None:
        inpath = abspath(dirname(exam_fn))
    mm, model_repo, config = init_metamodel(inpath)
    exam = mm.model_from_file(exam_fn)
    outpath = join(outpath_base, exam.name)
    if not exists(outpath):
        makedirs(outpath)

    _generate_tex(exam, config,
                  join(outpath, exam.name+".tex"), False)
    _generate_tex(exam, config,
                  join(outpath, exam.name+"_solution.tex"), True)
    _generate_pu_files(exam, outpath)

    myscript = join(outpath, "generate.sh")
    _generate_script(exam, myscript)

    generate_csv(exam, join(outpath, exam.name+".csv"))

    return abspath(outpath), abspath(myscript)

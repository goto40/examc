import jinja2
from os.path import dirname, abspath, join


def generate_pu_files(exam, out_dir):
    for exercise in exam.get_exercises():
        for pu in exercise.get_pu_contents():
            out_file_name = join(out_dir, pu.basename()+".pu")
            with open(out_file_name, 'w') as f:
                f.write(pu.render())


def generate_tex(exam, config, out_file_name="src-gen/out.tex", generate_solution=False):
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


def generate_script(exam, out_file_name):
    script = "#build\n"
    for exercise in  exam.get_exercises():
        for pu in exercise.get_pu_contents():
            script = script + f"plantuml {pu.basename()}.pu && \\"
    script = script + f'''
pdflatex {exam.name}.tex && \
pdflatex {exam.name}.tex && \
pdflatex {exam.name}_solution.tex && \
pdflatex {exam.name}_solution.tex && \
xdg-open {exam.name}.pdf && \
xdg-open {exam.name}_solution.pdf'''
    with open(out_file_name, 'w') as f:
        f.write(script)

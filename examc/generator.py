import jinja2

def generate_tex(exam, out_file_name="src-gen/out.tex", generate_solution=False):
    this_folder = dirname(abspath(__file__))
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)
    template = jinja_env.get_template('master.tex.template')
    with open(out_file_name, 'w') as f:
        f.write(template.render(exam=exam))


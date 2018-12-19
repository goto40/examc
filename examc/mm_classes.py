from textx import get_metamodel, get_children_of_type

class ModelBase(object):
    def __init__(self):
        pass

    def _init_xtextobj(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])
        if hasattr(self, "printtype"):
            if self.printtype is None:
                self.printtype = "BOTH"


class PExam(ModelBase):
    def __init__(self, **kwargs):
        super(PExam, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_exercises(self):
        from textx.scoping.tools import textx_isinstance
        mm = get_metamodel(self)
        lst = list(filter(
            lambda x: x.content.exercise is not None,
            self.exercises_or_raw_content))
        return list(map(lambda x: x.content.exercise.ref, lst))

    def get_exercises_and_extra_contents(self):
        from textx.scoping.tools import textx_isinstance
        mm = get_metamodel(self)
        def mapper(x):
            if x.content.exercise is not None:
                return x.content.exercise.ref
            else:
                return x.content.direct
        return list(map(mapper, self.exercises_or_raw_content))

    def get_exercise_count(self):
        return len(self.get_exercises())

    def get_points(self):
        return sum(map(lambda x: x.points, self.get_exercises()))

    def get_additional_front_page_info(self):
        if self.additional_front_page_info is not None:
            return self.additional_front_page_info
        else:
            return ""


class PExercise(ModelBase):
    def __init__(self, **kwargs):
        super(PExercise, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_pu_contents(self):
        return get_children_of_type('PPlantUmlContent', self)

    def get_num(self, exam):
        return exam.get_exercises().index(self)


class PLatexContent(ModelBase):
    def __init__(self, **kwargs):
        super(PLatexContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return self.text


class PCodeContent(ModelBase):
    def __init__(self, **kwargs):
        super(PCodeContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return f'''
\\begin{{lstlisting}}[style=customcpp]
{self.text.text}
\\end{{lstlisting}}
        '''


class PAsciiContent(ModelBase):
    def __init__(self, **kwargs):
        super(PAsciiContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return f'''
        \\begin{{lstlisting}}[style=customtxt]
        {self.text.text}
        \\end{{lstlisting}}
                '''


class PPlantUmlContent(ModelBase):
    def __init__(self, **kwargs):
        super(PPlantUmlContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def basename(self):
        exercise = self.parent
        group = exercise.parent
        return "uml_{}_{}_{}".format(
            group.name,
            exercise.name,
            exercise.content.index(self))

    def render(self):
        return self.text.text

    def generate(self):
        return f'''
\\begin{{center}}
\\includegraphics[width=0.75\\textwidth]{{ {self.basename()}.png }}
\\end{{center}}
        '''


class PFreeSpaceContent(ModelBase):
    def __init__(self, **kwargs):
        super(PFreeSpaceContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return r'\karos{{\textwidth}}{{ {}cm}}'.format(self.height)


class PImage(ModelBase):
    def __init__(self, **kwargs):
        super(PImage, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return f'''
\\begin{{center}}
\\includegraphics[width={self.localWidth}\\textwidth]{{ {self.fileSource} }}
\\end{{center}}
        '''

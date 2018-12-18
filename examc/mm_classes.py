from textx import get_metamodel

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
        return list(map(lambda x: x.content.ref, lst))

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
\begin{{lstlisting}}[style=customcpp]
{self.text.text}
\end{{lstlisting}}
        '''


class PAsciiContent(ModelBase):
    def __init__(self, **kwargs):
        super(PAsciiContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return ""


class PPlantUmlContent(ModelBase):
    def __init__(self, **kwargs):
        super(PPlantUmlContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return ""


class PFreeSpaceContent(ModelBase):
    def __init__(self, **kwargs):
        super(PFreeSpaceContent, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return ""


class PImage(ModelBase):
    def __init__(self, **kwargs):
        super(PImage, self).__init__()
        self._init_xtextobj(**kwargs)

    def generate(self):
        return ""

from textx import get_metamodel

class ModelBase(object):
    def __init__(self):
        pass

    def _init_xtextobj(self, **kwargs):
        for k in kwargs.keys():
            setattr(self, k, kwargs[k])


class PExam(ModelBase):
    def __init__(self, **kwargs):
        super(PExam, self).__init__()
        self._init_xtextobj(**kwargs)

    def get_exercises(self):
        from textx.scoping.tools import textx_isinstance
        mm = get_metamodel(self)
        lst = list(filter(
            lambda x: textx_isinstance(x.content, mm['PExerciseRef']),
            self.exercises_or_raw_content))
        return list(map(lambda x: x.content.ref, lst))

    def get_points(self):
        return sum(map(lambda x: x.points, self.get_exercises()))

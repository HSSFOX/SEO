





from PyQt5.QtGui import QValidator

class FixedPartValidator(QValidator):
    def __init__(self, fixed_str_l):
        super().__init__()
        self.fixed_str_l = fixed_str_l

    def validate(self, input_str, pos):
        # s = len(self.fixed_str_l)
        for i in self.fixed_str_l:
            if input_str.startswith(i):
                return (QValidator.Acceptable, input_str, pos)
        return (QValidator.Invalid, input_str, pos)



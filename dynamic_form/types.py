import enum


class TriggerEventTypes(enum.Enum):
    BLUR = 'blur'
    CHANGE = 'change'
    CLICK = 'click'
    DOUBLE_CLICK = 'dblclick'
    INPUT = 'input'
    KEY_UP = 'keyup'
    KEY_DOWN = 'keydown'
    SELECT = 'select'

    def __str__(self):
        return self.value

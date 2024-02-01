from enum import Enum

# Browser
class BrowserType(Enum):
    CHROME = 0
    FIREFOX = 1

class SimpleAction(Enum):
    CLICK = 0
    DOUBLE_CLICK = 1

class AdvancedAction(Enum):
    CLICK_AND_HOLD = 0
    DOUBLE_CLICK = 1
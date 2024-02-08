from enum import Enum

# Browser
class BrowserType(Enum):
    CHROME = 0
    FIREFOX = 1

class SimpleAction(Enum):
    LEFT_CLICK = 0
    RIGHT_CLICK = 1
    DOUBLE_CLICK = 2
    CLICK_AND_HOLD = 3
    RELEASE = 4

class DriverAction(Enum):
    FORWARD = 0
    BACK = 1
    REFRESH = 2
    FULL_SCREEN = 3
    MINIMIZE_WINDOW = 4


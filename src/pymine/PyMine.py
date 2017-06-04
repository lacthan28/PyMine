from ..spl.stubs.Core import *
from ..spl.stubs.core_d import *

is_array = lambda var: isinstance(var, (list, tuple))


def str_repeat(the_str, multiplier):
    return the_str * multiplier


def safe_var_dump():
    cnt = 0
    for var in func_get_arg():
        if is_array(var):
            print(str_repeat("  ", cnt) + "{" + PYTHON_EOL)
            for key, value in var:
                print(
                    str_repeat("  ", cnt + 1) + (isinstance(key, int) if key else ('"' + key + '"') + ":" + PYTHON_EOL))
                ++cnt
                safe_var_dump(value)
                --cnt
            print(str_repeat("  ", cnt) + "}" + PYTHON_EOL)
        elif isinstance(var, int):
            print(str_repeat("  ", cnt) + "int(" + var + ")" + PYTHON_EOL)
        elif isinstance(var, float):
            print(str_repeat("  ", cnt) + "float(" + var + ")" + PYTHON_EOL)
        elif isinstance(var, bool):
            print(str_repeat("  ", cnt) + "bool(" + (var == True if "true" else "false") + ")" + PYTHON_EOL)
        elif isinstance(var, str):
            print(str_repeat("  ", cnt) + "string(" + len(var) + ")\\" + var + "\\" + PYTHON_EOL)
        elif isinstance(var, object):
            print(str_repeat("  ", cnt) + "object(" + type(var).__name__ + ")" + PYTHON_EOL)
        elif var is None:
            print(str_repeat("  ", cnt) + "NULL" + PYTHON_EOL)


def dummy(): pass


class PyMine:
    VERSION = "2.0dev";

    API_VERSION = "3.0.0";

    CODENAME = "PyMine";

    MINECRAFT_VERSION = "v1.0.9 alpha";

    MINECRAFT_VERSION_NETWORK = "1.0.9";

    PYMINE_VERSION = "0.0.1";

    # if Egg

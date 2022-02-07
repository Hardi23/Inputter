import inspect
import os
from typing import Optional


class TermColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


WARNING_FORMAT_STR = "{}[WARNING]{} - {}"
ERROR_FORMAT_STR = "{}[ERROR]{} - {}"
INFO_FORMAT_STR = "{}[INFO]{} - {}"
INPUT_FORMAT_STR = "{}[INPUT]{} - {}"
ERROR_EXCEEDED_RETRIES = "Too many bad inputs!"

format_prompt = False


def is_directory(input_str: str) -> Optional[str]:
    if input_str is not None and os.path.isdir(input_str):
        return input_str
    print_warning(f"{input_str} is not a valid directory!")
    return None


def is_file(input_str: str) -> Optional[str]:
    if input_str is not None and os.path.isfile(input_str):
        return input_str
    print_warning(f"{input_str} is not a valid file!")
    return None


def is_int(input_str: str) -> Optional[int]:
    try:
        int_val = int(input_str)
        return int_val
    except ValueError:
        print_warning(f"{input_str} is not an integer!")
        return None


def is_float(input_str: str) -> Optional[float]:
    try:
        float_val = float(input_str)
        return float_val
    except ValueError:
        print_warning(f"{input_str} is not a decimal number!")
        return None


def is_integer_in_range(input_str: str, min_val: int, max_val: int) -> Optional[int]:
    try:
        int_val = int(input_str)
        if int_val < min_val or int_val > max_val:
            print_warning(f"Value should be in range {min_val} - {max_val}")
            return None
        return int_val
    except ValueError:
        print_warning("Input is not an integer")
        return None


def not_empty(input_str: str) -> Optional[str]:
    if input_str and input_str != "":
        return input_str
    print_warning("Input can not be empty!")
    return None


def print_error(msg: str):
    print(ERROR_FORMAT_STR.format(TermColors.RED, TermColors.ENDC, msg))


def print_warning(msg: str):
    print(WARNING_FORMAT_STR.format(TermColors.YELLOW, TermColors.ENDC, msg))


def print_info(msg: str):
    print(INFO_FORMAT_STR.format(TermColors.OKCYAN, TermColors.ENDC, msg))


def check_constraint_function(function: callable = None, params: list = None) -> bool:
    if function is None:
        print_warning("No input constraint function specified!")
        return True
    if not (callable(function)):
        print_error("Constraint function is not of type Callable!")
        return False
    func_sig = inspect.signature(function)
    func_params = func_sig.parameters.values()
    func_param_count = len(func_params)
    if func_param_count == 0:
        print_error("Constraint function does not accept parameters,"
                    " the function should accept at least one parameter of type str.\n"
                    "You can pass None, Default is not_empty")
        return False
    passing_param_count = len(params) + 1
    if passing_param_count > func_param_count:
        print_error("Constraint function accepts less parameters than would be passed!")
        return False

    for index, param in enumerate(func_params):
        if index == 0:
            if param.annotation is not None and param.annotation is not str:
                print_error("First parameter of constraint function must be of type str!")
                return False
        else:
            if param.annotation is not None and type(params[index - 1]) is not param.annotation:
                print_warning(f"Constraint function parameter {index + 1} is specified as"
                              f" {param.annotation}, passed argument will be of type "
                              f"{type(params[index - 1])}")
    return True


def test_input(function: callable, params: list) -> bool:
    return function(*params)


def get_input(prompt, f_constraint: callable = not_empty,
              f_additional_params: list = None, max_tries: int = -1) -> Optional:
    if f_additional_params is None:
        f_additional_params = []
    if f_constraint is not None and not check_constraint_function(f_constraint, f_additional_params):
        return None
    output = None
    counter = 0
    if format_prompt:
        prompt = INPUT_FORMAT_STR.format(TermColors.OKGREEN, TermColors.ENDC, prompt)
    while output is None:
        if 0 < max_tries <= counter:
            print_error(ERROR_EXCEEDED_RETRIES)
            return None
        in_str = input(prompt)
        if f_constraint is not None:
            param_list = [in_str, *f_additional_params]
            output = test_input(f_constraint, param_list)
        else:
            output = in_str
        counter += 1
    return output


if __name__ == '__main__':
    # print(f"You typed: {get_input('Running main, give me some input: ')}")
    format_prompt = True
    a = get_input("Float pls: ", is_float, max_tries=5)
    print_info(f"You typed: {a}")

import builtins
import io
import unittest
from unittest.mock import patch
import Inputter
from contextlib import redirect_stdout, redirect_stderr

PROMPT = "Input: "
MAX_TRIES = 5


def run_collecting_stdout(function, args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        with redirect_stderr(buf):
           result = function(*args)
    return buf.getvalue(), result


def run_overriding_input(input_ret_val, f_constraint, additionals=None):
    with unittest.mock.patch('builtins.input', return_value=input_ret_val):
        return Inputter.get_input(PROMPT, f_constraint, f_additional_params=additionals, max_tries=MAX_TRIES)


class TestFileName(unittest.TestCase):
    def test_existing_file(self):
        self.assertEqual(run_overriding_input("test.txt", Inputter.is_file), "test.txt")

    def test_file_not_exist(self):
        self.assertEqual(run_overriding_input("Nothing.py", Inputter.is_file), None)

    def test_long_path(self):
        self.assertEqual(run_overriding_input("C:\\Windows\\System32\\cmd.exe", Inputter.is_file)
                         , "C:\\Windows\\System32\\cmd.exe")


class TestInteger(unittest.TestCase):
    def test_is_integer(self):
        self.assertEqual(run_overriding_input("2", Inputter.is_int), 2)

    def test_is_large_integer(self):
        self.assertEqual(run_overriding_input("1203469875211", Inputter.is_int), 1203469875211)

    def test_is_large_negative_int(self):
        self.assertEqual(run_overriding_input("-1203469875211", Inputter.is_int), -1203469875211)

    def test_is_zero(self):
        self.assertEqual(run_overriding_input("0", Inputter.is_int), 0)

    def test_is_not_integer(self):
        self.assertEqual(run_overriding_input("a", Inputter.is_int), None)


class TestIntegerRange(unittest.TestCase):
    def test_int_in_range(self):
        self.assertEqual(run_overriding_input("101", Inputter.is_integer_in_range, additionals=[0, 101]), 101)

    def test_int_not_in_range(self):
        self.assertEqual(
            run_overriding_input("1203469875211", Inputter.is_integer_in_range, additionals=[0, 100]), None)

    def test_int_in_range_bad_input(self):
        self.assertEqual(run_overriding_input("abcz", Inputter.is_integer_in_range, additionals=[0, 100]), None)


class TestTestInputInternal(unittest.TestCase):
    def test_constraint_ok(self):
        self.assertEqual(Inputter.test_input(Inputter.is_int, ["2"]), 2)

    def test_constraint_not_ok(self):
        self.assertEqual(Inputter.test_input(Inputter.is_int, ["a"]), None)


class TestIsDirectory(unittest.TestCase):
    def test_is_dir(self):
        self.assertEqual(run_overriding_input("testfolder", Inputter.is_directory), "testfolder")

    def test_is_not_dir(self):
        self.assertEqual(run_overriding_input("randomFolder", Inputter.is_directory), None)


class TestEmptyInput(unittest.TestCase):
    def test_input_not_empty(self):
        self.assertEqual(run_overriding_input("0", Inputter.not_empty), "0")

    def test_input_empty(self):
        self.assertEqual(run_overriding_input("", Inputter.not_empty), None)


class TestMaxTries(unittest.TestCase):
    def test_too_many_tries(self):
        msg_buf, result = run_collecting_stdout(run_overriding_input, ["a", Inputter.is_int, []])
        self.assertEqual(result, None) and self.assertEqual(msg_buf, '\033[91m[ERROR]\033[0m - Too many bad inputs!')


def bad_func():
    pass


def not_enough_args(input_str: str):
    pass


def bad_first_arg(test: int):
    pass


class TestBadConstraintFunction(unittest.TestCase):
    def test_bad_func(self):
        msg_buf, result = run_collecting_stdout(run_overriding_input, ["a", bad_func, []])
        self.assertEqual(result, None) and \
            self.assertEqual(msg_buf,
                             "\033[91m[ERROR]\033[0m - Constraint function does not accept parameters,"
                             " the function should accept at least one parameter of type str.\nYou can pass None,"
                             " Default is not_empty\n")

    def test_too_many_arguments(self):
        msg_buf, result = run_collecting_stdout(run_overriding_input, ["a", not_enough_args, [1, 2, 3]])
        self.assertEqual(result, None) and \
            self.assertEqual(msg_buf, "\033[91m[ERROR]\033[0m - Constraint function accepts less parameters"
                                      " than would be passed!\n")

    def test_first_arg_not_string(self):
        msg_buf, result = run_collecting_stdout(run_overriding_input, ["a", bad_first_arg, []])
        self.assertEqual(result, None) and \
            self.assertEqual(msg_buf, "\033[91m[ERROR]\033[0m - First parameter of constraint function"
                                      " must be of type str!\n")

    def test_constraint_func_none(self):
        msg_buf, result = run_collecting_stdout(Inputter.check_constraint_function, [None, []])
        self.assertEqual(result, True) and \
            self.assertEqual(msg_buf, "\033[93m[WARNING]\033[0m - No input constraint function specified!\n")

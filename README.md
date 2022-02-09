# Inputter - Just getting input
___
A small library to get user input in a quick and easy way.

Feel free to submit pull requests.

## Usage
___
### Use Inputter in your code
Clone or download the Inputter.py file or install via pip.
```
pip install inputtr
```

```python
from inputtr import inputter
# Inputter.get_input(prompt, f_constraint: callable = not_empty, f_additional_params=None, max_tries: int = -1) -> Optional:
in_str = inputter.get_input("Prompt: ", constraint_function, [additional, parameters], max_tries=5)

# prompt: The prompt which is shown when input is required.
# f_constraint: Constraint function to check the input against,
#               this function is also allowed to transform the output.
# f_additional_params: List of parameters to supply to the constraint function.
# max_tries: Negative for no limit, otherwise cancel after x and show error.
```
### Flags

```python
# Available flags are:
from inputtr import inputter

inputter.format_prompt = (True / False) # Format the input prompt with badge and color (Default: True)
inputter.silent = (True / False) # Suppresses or enables all output except prompting (Default: False)
inputter.disable_colors = (True / False) # Enables / Disables colored output but keeps badges  (Default: False)
inputter.disable_badges = (True / False) # Enables / Disables badges in output  (Default: False)
inputter.throw_on_constraint_func_error = (True / False) # Changes constraint function error behaviour  (Default: False)
```
### Creating new constraint functions
To create a custom constraint function, your function should follow some simple rules
1. Accept str as first parameter, this will be the user input
2. To generate warnings without crashes your function should supply parameter types
3. The function should return an Optional type and return None if checking was not successful

Your function will be checked before trying to execute it, any minor errors will be output as warnings.

Errors which would crash execution will be output as errors and the ```get_input() ``` returns ```None```, this behaviour
can be changed with the flag mentioned above in which case a RuntimeError is also thrown.

The only exception to this, is the case where you do not supply enough parameters, and the constraint function
does not have sufficient default parameters in which case a TypeError is always thrown.

Example:

```python
from inputtr import inputter


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


user_input = Inputter.get_input("Input: ", is_integer_in_range, [0, 100])
```
As shown in the example to keep the look of printed text the same,
you should use the print_error and print_warning function of Inputter.

### Changing colors and formatting
___
Inputter has a selection of colors and modifiers to choose from,
the ones available can be accessed via the TermColors class.

Since we are dealing with console output the colors are determined by ANSI escape sequences,
to get more information about this read: https://en.wikipedia.org/wiki/ANSI_escape_code

```python
from inputtr import inputter

inputter.info_color = inputter.TermColors.OKBLUE
inputter.error_color = inputter.TermColors.RED
inputter.prompt_color = inputter.TermColors.OKGREEN
inputter.warning_color = inputter.TermColors.YELLOW
```

All of these colors can of course also be combined with formatting changes.

```python
from inputtr import inputter

Inputter.prompt_color = inputter.TermColors.OKGREEN + inputter.TermColors.BOLD
```

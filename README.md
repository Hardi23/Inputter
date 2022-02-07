# Inputter - Just getting input
___
A small library to get user input in a quick and easy way.

Feel free to submit pull requests.

#Usage
___
### Use Inputter in your code
Clone or download the Inputter.py file.

```python
# Inputter.get_input(prompt, f_constraint: callable = not_empty, f_additional_params=None, max_tries: int = -1) -> Optional:
in_str = Inputter.get_input("Prompt: ", constraint_function, [additional, parameters], max_tries=5)

# prompt: The prompt which is shown when input is required.
# f_constraint: Constraint function to check the input against,
#               this function is also allowed to transform the output.
# f_additional_params: List of parameters to supply to the constraint function.
# max_tries: Negative for no limit, otherwise cancel after x and show error.
```

### Creating new constraint functions
To create a custom constraint function, your function should follow some simple rules
1. Accept str as first parameter, this will be the user input
2. To generate warnings without crashes your function should supply parameter types
3. The function should return an Optional type and return None if checking was not successful

Example:
```python
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
```
As shown in the example to keep the look of printed text the same,
you should use the print_error and print_warning function of Inputter
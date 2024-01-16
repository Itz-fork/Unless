# Unless
**Unless** is a lightweight python library designed to simplify error handling. It introduces the `Result` class that encapsulates the result of a function call, which can be either the return value, an error, or both.


# Install
```sh
pip3 install unless-handler
```


# Usage
> **💡 Remember**
>
>`Result` class has 2 properties and 1 method,
>  - Properties
>    - `value` - The return value of the function
>    - `error` - Information about the error if there was any
>        - It can be either a tuple of the exception type and traceback string, or just the traceback string
>
>  - Methods
>    - `unless` - Handle errors and return the `value`


- **Import the `Result` class and `traceback.format_exc` for tracebacks**
    ```py
    from unless import Result

    from traceback import format_exc # Optional
    ```


- **Integrate `Result` into your function**
    - Initialize the `Result` class (specify the return type for type hints)
        ```py
        def cool():
            to_return = Result[list]()
                                ^
                            Return type
        ```
        > `[list]` is the return type of the function and is there so we can have type hints. It is OPTIONAL and `Result()` works too.


    - Set the return value
        - Use `value` property of the `Result` class to set return value
        ```py
        # <initialized>.value = <value to return>
        to_return.value = [1, 2, 3]
        ```

    - Catch and set errors
        - Use `error` property of the `Result` class to set errors
        - You have the freedom to set any value you like; however, it is **recommended** to follow the given syntax of `<type>, <traceback>` as it gives the ability to have caused exception type and the traceback for better error handling
        ```py
        try:
            ...
        except Exception as e:
            # <initialized>.error = <exception type>, <traceback.format_exc()>
            to_return.error = type(e), format_exc()
        ```

    - Return the result
        ```py
        return to_return
        ```

- **Calling your function**
    - See result using the `value` property
        ```py
        called = my_function()

        called.value
        ```
    
    - See error using the `error` property
        ```py
        called.error
        ```
    
    - Or better yet, use the `unless` method
        ```py
        called = my_function().unless()

        # called is now called.value and errors are handled using handler function
        # for more info check "Examples"
        ```


# Examples
- [Basic usage](#basic-usage)
- [Custom error handler](#custom-error-handling)
- [Integrate with existing functions](#integrate-with-existing-functions)


### Basic usage
```py
def cool():
    to_return = Result[list]()
    try:
        to_return.value = [1, 2, 3]
        raise ValueError("Annoying error...")
    except Exception as e:
        to_return.error = type(e), traceback.format_exc()
    return to_return

# Calling the function
x = cool().unless()
print(x)
```

### Custom error handling
You can call functions with custom error handling logic using `Result.unless` method that your function returns.

- You can pass **any python function** to the `unless` method
- Your handler function _must_ accept at least 1 argument
    - If you're using `Result.from_func` or following the recommended syntax, the 1st argument will be a tuple consist of `<type of exception>, <traceback string>`
- Handler function _can have_ keyword arguments (`x.unless(func, arg1="first", arg2="second")`)

```py
def custom_handler(e, notes):
    _, fmt_traceback = e
    logging.warn(f"{fmt_traceback} \n\nNotes: {notes}")

x = cool().unless(
        custom_handler,
        notes="Probably happend because the function was hot"
    )
print(x)
```

### Integrate with existing functions
You can use `Result.from_func` method to integrate this with existing functions.

- As a decorator,
    ```py
    @Result.from_func
    def older(n) -> list:
        return [1, 2, 3, n]
    ```
- As a function,
    ```py
    def older(n) -> list:
        return [1, 2, 3, n]

    x = Result.from_func(older, list, n=2)

    # Important:
    #  if your function doesn't accept arguments, use "()" at the end to call it properly
    
    # Example:
    x = Result.from_func(no_args)()
                                  ^
                          Call the function
    ```
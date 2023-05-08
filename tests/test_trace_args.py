from llamatry.trace import simple_args_to_dict


def test_case_1():
    def func(a, b, c=3, d=4):
        pass

    args = (1, 2)
    kwargs = {"c": 5}
    arg_dict = simple_args_to_dict(func, *args, **kwargs)
    assert arg_dict == {"a": 1, "b": 2, "c": 5}


def test_case_2():
    def func(x, y=True, z="hello"):
        pass

    args = (3.5,)
    kwargs = {"z": "world"}
    arg_dict = simple_args_to_dict(func, *args, **kwargs)
    assert arg_dict == {"x": 3.5, "z": "world"}


def test_case_3():
    def func(w, x, y, z):
        pass

    args = (10, 20, 30)
    kwargs = {"z": 40}
    arg_dict = simple_args_to_dict(func, *args, **kwargs)
    assert arg_dict == {"w": 10, "x": 20, "y": 30, "z": 40}

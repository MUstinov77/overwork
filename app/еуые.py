def test_func(
        action,
        some,
        other,
        *args,
        **kwargs
):
    print(action)
    print(some)
    print(other)

values = {
    "action": "create",
    "some": 1,
    "other": 2,
    "depr": 3
}

test_func(**values)


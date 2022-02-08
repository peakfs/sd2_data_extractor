def strtobool(value: str) -> bool:
    v = value.lower()

    truthy_values = (
        'y',
        'yes',
        't',
        'true',
        'on',
        '1'
    )

    falsy_values = (
        'n',
        'no',
        'f',
        'false',
        'off',
        '0'
    )

    if v in truthy_values:
        return True
    elif v in falsy_values:
        return False
    else:
        raise ValueError(f'Value "{v}" cannot be converted to boolean.')

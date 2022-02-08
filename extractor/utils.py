from typing import Any


def strtobool(value: Any) -> bool:
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

    if value in truthy_values:
        return True
    elif value in falsy_values:
        return False
    else:
        raise ValueError(f'Value "{value}" cannot be converted to boolean.')

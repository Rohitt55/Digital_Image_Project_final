"""Register operation names and parameter fields for the app."""

OPERATIONS = {}


def field(key, label, default, low, high, step=1):
    return dict(key=key, label=label, default=default, min=low, max=high, step=step, type='number')


def choice(key, label, default, options):
    return dict(key=key, label=label, default=default, options=options, type='select')


def operation(key, name, group, explanation, formula, source, fields=(), requires_reference=False):

    def register(function):
        OPERATIONS[key] = dict(
            id=key,
            name=name,
            group=group,
            explanation=explanation,
            formula=formula,
            source=source,
            fields=list(fields),
            function=function,
            requires_reference=requires_reference
        )
        return function
    return register

from yunapp.app_tasks.cel_app import cel_app


@cel_app.task
def add(x, y):
    return x + y


@cel_app.task
def mul(x, y):
    return x * y


@cel_app.task
def xsum(numbers):
    return sum(numbers)
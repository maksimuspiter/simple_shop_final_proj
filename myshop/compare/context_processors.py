from .compare import Compare


def compare(request):
    return {"compare": Compare(request)}

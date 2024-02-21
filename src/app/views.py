from app.models import MyModel


def func(af):
    users = MyModel.objects.all()
    return {'users': users}

from django.utils import timezone

def my_cp(request):
    ctx = {
        'now': timezone.now(),
        'version': '1.01'
    }
    return ctx

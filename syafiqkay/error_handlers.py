from django.shortcuts import render


def custom_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    return render(request, 'errors/500.html', status=500)


def custom_501(request):
    return render(request, 'errors/501.html', status=501)


def custom_502(request):
    return render(request, 'errors/502.html', status=502)


def custom_503(request):
    return render(request, 'errors/503.html', status=503)


def custom_504(request):
    return render(request, 'errors/504.html', status=504)


def custom_505(request):
    return render(request, 'errors/505.html', status=505)


def custom_401(request):
    return render(request, 'errors/401.html', status=401)


def custom_402(request):
    return render(request, 'errors/402.html', status=402)


def custom_405(request):
    return render(request, 'errors/405.html', status=405)


def custom_406(request):
    return render(request, 'errors/406.html', status=406)


def custom_407(request):
    return render(request, 'errors/407.html', status=407)


def custom_408(request):
    return render(request, 'errors/408.html', status=408)


def custom_409(request):
    return render(request, 'errors/409.html', status=409)


def custom_410(request):
    return render(request, 'errors/410.html', status=410)

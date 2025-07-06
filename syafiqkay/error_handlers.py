from django.shortcuts import render


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


def custom_501(request):
    return render(request, '501.html', status=501)


def custom_502(request):
    return render(request, '502.html', status=502)


def custom_503(request):
    return render(request, '503.html', status=503)


def custom_504(request):
    return render(request, '504.html', status=504)


def custom_505(request):
    return render(request, '505.html', status=505)


def custom_401(request):
    return render(request, '401.html', status=401)


def custom_402(request):
    return render(request, '402.html', status=402)


def custom_405(request):
    return render(request, '405.html', status=405)


def custom_406(request):
    return render(request, '406.html', status=406)


def custom_407(request):
    return render(request, '407.html', status=407)


def custom_408(request):
    return render(request, '408.html', status=408)


def custom_409(request):
    return render(request, '409.html', status=409)


def custom_410(request):
    return render(request, '410.html', status=410)

from django.shortcuts import render

def index(request):
    request.session['login_referer'] = request.get_full_path()
    return render(request, 'index.html')

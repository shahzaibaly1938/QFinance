from django.shortcuts import render

# Create your views here.

def login(request):
    if request.method == 'POST':
        pass


    return render(request, 'user/login.html')
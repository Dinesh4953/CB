from django.shortcuts import redirect

def starting_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    return redirect('login')
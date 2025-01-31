from django.shortcuts import render #type: ignore

# Create your views here.
def Index(request):
    return render(request, 'client/index.html')
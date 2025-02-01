from django.shortcuts import render #type: ignore

# Create your views here.
def Index(request):
    return render(request, 'client/index.html')

def About(request):
    return render(request, 'client/about.html')

def Article(request):
    return render(request, 'client/article.html')

def Category(request):
    return render(request, 'client/category.html')
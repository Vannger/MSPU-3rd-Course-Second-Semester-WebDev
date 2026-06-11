from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'The definitive DnD collection of spells',
        'welcome_text': 'Hello and Welcome, ladies and gentleman, to, well, THIS'
    }
    return render(request, 'pages/index.html', context)

def about(request):
    context = {
        'title': 'The definitive DnD collection of spells',
        'text': 'Text that i would like'
    }
    return render(request, 'pages/about.html', context)
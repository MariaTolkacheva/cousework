from django.shortcuts import render
from .models import Member

def members(request):
    mymembers = Member.objects.all()
    return render(request, 'all_members.html', {'mymembers': mymembers})

def details(request, id):
    mymember = Member.objects.get(id=id)
    return render(request, 'details.html', {'mymember': mymember})

def main(request):
    return render(request, 'myfirst.html')

def survey(request):
    return render(request, 'survey.html')

def myfirst(request):
    return render(request, 'myfirst.html')

def testing(request):
    return render(request, 'testing.html', {'fruits': ['Apple', 'Banana', 'Cherry']})

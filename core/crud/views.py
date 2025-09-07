from django.shortcuts import render , redirect , get_object_or_404 , HttpResponse
from .models import Recipe



def main_page(request):
    
    all_reciptes = Recipe.objects.filter(user=request.user)

    if request.method == 'POST':
        if request.POST.get('search'):
            search_item = request.POST.get('search')
            print(f"the search item is : {search_item}")
            all_reciptes = Recipe.objects.filter(recipe_name__icontains=search_item)

    
    context = {
        'all_reciptes' : all_reciptes
    }
    
    return render(request , 'main_page_reciptes.html' , context)


    







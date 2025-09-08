from django.shortcuts import render , redirect , get_object_or_404 , HttpResponse
from .models import Recipe
from django.contrib import messages


# TODO : adding a reipe 
# TODO : deleting a recipe 
# TODO : updating a recipe







def main_page(request):

    all_reciptes = Recipe.objects.filter(user=request.user)
    
    try : 
        if request.method == 'POST':
            if request.POST.get('recipe_name') and request.POST.get('recipe_description') and request.POST.get('image') : 
                recipe_name = request.POST.get('recipe_name') 
                recipe_description = request.POST.get('recipe_desciption')
                image = request.POST.get('image')
                user = request.user

                recipe_obj = Recipe.objects.create( user=user , 
                                                    recipe_name = recipe_name ,
                                                    recipe_description = recipe_description , 
                                                    recipe_image = image)
                recipe_obj.save()
                messages.success(request , f'the recipe saved !')

            if request.POST.get('search'):
                search_item = request.POST.get('search')
                print(f"the search item is : {search_item}")
                all_reciptes = Recipe.objects.filter(recipe_name__icontains=search_item)

    except Exception as e: 
        messages.error(request , f"some error happend  : {e}")
        print(f"the error is : {e}")



    context = {
        'all_reciptes' : all_reciptes
    }
    
    return render(request , 'main_page_reciptes.html' , context)








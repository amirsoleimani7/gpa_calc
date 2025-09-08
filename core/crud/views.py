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
            print(f" user is : {request.user}")
            print(f"recipe name is : {request.POST.get('recipe_name')}")
            print(f"recipe_description is : {request.POST.get("recipe_description")}")
            if request.FILES.get('image'):
                print("file exits")
            else : 
                print(f"file is not there !")


            if request.POST.get('recipe_name') and request.POST.get('recipe_description') and request.FILES.get('image') : 
                recipe_name = request.POST.get('recipe_name') 
                recipe_description = request.POST.get('recipe_description')
                image = request.FILES['image']
                user = request.user

                recipe_obj = Recipe.objects.create( user=user , 
                                                    recipe_name = recipe_name ,
                                                    recipe_description = recipe_description , 
                                                    recipe_image = image)
                recipe_obj.save()
                messages.success(request , f'the recipe saved !')
                return redirect('main_page')

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

def update_recipe(request , pk):

    recipe_obj = Recipe.objects.get(pk=pk)   # better than filter()[0]

    if request.method == 'POST':

        if request.POST.get('new_name') : 
           recipe_obj.recipe_name = request.POST.get('new_name')
        if request.POST.get('new_description') : 
            recipe_obj.recipe_description = request.POST.get('new_description')
        if request.FILES.get('new_image') : 
            recipe_obj.recipe_image = request.FILES['new_image']

        recipe_obj.save()
        messages.success(request , f'recipe updated !')

    return render(request , 'update_page.html')


def delete_recipe(request , pk):
    query_recipe = get_object_or_404(Recipe , pk=pk)
    query_recipe.delete()

    return redirect('main_page')


import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from posts.forms import PostForm
from posts.models import Author, Category, Post
from main.functions import generate_form_error, paginate_instances
from main.decorators import allow_self


@login_required(login_url="/users/login/")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            tags = form.cleaned_data['tags']

            if not Author.objects.filter(user=request.user).exists():
                author = Author.objects.create(user=request.user, name=request.user.username)
            else:
                author = request.user.author


            instance = form.save(commit=False)
            instance.published_date = datetime.date.today()
            instance.author = author
            instance.save()

            tags_list = tags.split(",")
            for tag in tags_list:
                category, created = Category.objects.get_or_create(title=tag.strip())
                instance.category.add(category)

            response_data ={
                "title" : "Succefully created",
                "message" : "Succefully Created",
                "status" : "success",
                "redirect" : "yes",
                "redirect_url" : "/"

            }

        else:
            error_message = generate_form_error(form)
            response_data = {
                "title" : "From validation error",
                "message" : str(error_message),
                "status" : "error",
                "stable" : "yes",

            }
        return HttpResponse(json.dumps(response_data), content_type="application/json")   

    else:
        form = PostForm()
        context = {
            "title" : "Create new Post",
            "form" : form,
        }
        return render(request, "posts/create.html", context=context)


@login_required(login_url="/users/login/")
def my_posts(request):
    posts = Post.objects.filter(author__user=request.user, is_deleted=False)
    instances = paginate_instances(request, posts, per_page=1)
    context = {
        "title" : "Blog | My Post",
        "instances" : instances
    }
    return render(request, "posts/my-posts.html", context=context)


@login_required(login_url="/users/login/")
@allow_self
def delete_post(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.is_deleted = True
    instance.save()

    reponse_data = {
        "title" : "Succefully deleted",
        "message" : "Post Deleted successfully",
        "status" : "success",
    }

    return HttpResponse(json.dumps(reponse_data), content_type="application/json")


@login_required(login_url="/users/login/")
@allow_self
def draft_post(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.is_draft = not instance.is_draft
    instance.save()

    reponse_data = {
        "title" : "Succefully Changed",
        "message" : "Post Updated successfully",
        "status" : "success",
    }

    return HttpResponse(json.dumps(reponse_data), content_type="application/json")

 
@login_required(login_url="/users/login/")
@allow_self
def edit_post(request, id):
    instance = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():

            tags = form.cleaned_data['tags']

            instance = form.save(commit=False)
            instance.save()

            instance.category.clear()

            tags_list = tags.split(",")
            for tag in tags_list:
                category, created = Category.objects.get_or_create(title=tag.strip())
                instance.category.add(category)

            response_data ={
                "title" : "Succefully created",
                "message" : "Succefully Created",
                "status" : "success",
                "redirect" : "yes",
                "redirect_url" : "/"

            }  

        else:
            error_message = generate_form_error(form)
            response_data = {
                "title" : "From validation error",
                "message" : str(error_message),
                "status" : "error",
                "stable" : "yes",

            }
        return HttpResponse(json.dumps(response_data), content_type="application/json")     

    else:
        category_string = ""
        for category in instance.category.all():
            category_string += f"{category.title},"

        form = PostForm(instance=instance, initial={"tags" : category_string[:-1]})
        context = {
            "title" : "Create new Post",
            "form" : form,
        }
        return render(request, "posts/create.html", context=context)

from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': "input"}), label="Tags (Comma separated)")

    class Meta:
        model = Post
        exclude = ('author', 'published_date', 'is_deleted', 'category')

        widgets = {
            "time_to_read" : forms.TextInput(attrs={'class': "input"}),
            "title" : forms.TextInput(attrs={'class': "input"}),
            "short_description" : forms.Textarea(attrs={'class': "input"})
        }

        error_messages = {
            "time_to_read" : {
                "required": "Time to read field is required"
            },
            "title" : {
                "required": "Title field is required"
            },
            "description" : {
                "required": "Description field is required"
            },
            "short_description" : {
                "required": "Short description field is required"
            },
            "tags" : {
                "required": "Tag field is required"
            },
            "featured_image" : {
                "required": "Featured image field is required"
            },
            "is_draft" : {
                "required": "Draft field is required"
            },
            "categories" : {
                "required": "Draft field is required"
            },
            "author" : {
                "required": "author field is required"
            },
            "published_date" : {
                "required": "published_date field is required"
            }, 
            "is_deleted" : {
                "required": "is_deleted field is required"
            },
        }
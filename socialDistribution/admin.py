from django.contrib import admin

from socialDistribution.models import Author, Post

admin.site.site_header = 'Social Distribution Admin'
admin.site.site_title = 'Social Distribution Admin Portal'
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'github', 'host', 'id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username',)

admin.site.register(Author, AuthorAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'origin', 'description', 'contentType', 'visibility', 
                    'unlisted', 'content', 'published', 'author', 'categories', 'imageOnlyPost', 'count')
    search_fields = ('title', 'host', 'description',)
    class Meta:
        model = Post
admin.site.register(Post, PostAdmin)
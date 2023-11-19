from rest_framework import permissions

class IsSharedWithFriends(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.shared_with_friends and user.is_authenticated:
            # Check if the user is a friend/follower of the author
            return user.author.followers.filter(id=obj.owner.id).exists()
        return not obj.shared_with_friends
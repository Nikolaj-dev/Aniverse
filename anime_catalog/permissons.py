from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class IsRatingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.for_user.user == request.user


class IsCollectionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.user == request.user


class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.user == request.user

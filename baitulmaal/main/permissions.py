from rest_framework import permissions

class IsPrivateAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        # return True if allowed else False
        # 'username' is the request url kwarg eg. bobby, jonhdoe
        return view.kwargs.get('email', 'admin@gmail.com') == request.user.email
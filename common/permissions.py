from rest_framework.permissions import BasePermission, SAFE_METHODS

# Only allow the book's uploader.
class IsUploader(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user

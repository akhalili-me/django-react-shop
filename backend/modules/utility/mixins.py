from django.shortcuts import get_object_or_404

# class MultipleFieldLookupMixin:
#     """
#     Apply this mixin to any view or viewset to get multiple field filtering
#     based on a `lookup_fields` attribute, instead of the default single field filtering.
#     """
#     def get_object(self):
#         queryset = self.get_queryset()             # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             if self.kwargs.get(field): # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         obj = get_object_or_404(queryset, **filter)  # Lookup the object
#         self.check_object_permissions(self.request, obj)
#         return obj


class SingleFieldUrlGetObjectMixin:
    def get_object(self):
        field = getattr(self, "filter_field", "id")
        url_keyword = getattr(self, "url_keyword", "pk")
        return get_object_or_404(self.model, **{field: self.kwargs.get(url_keyword)})

from django.shortcuts import get_object_or_404

def get_obj_with_pk(model_class, pk):
    return get_object_or_404(model_class, pk=pk)

def update_model_attrs(instance, **attrs):
    for attr, val in attrs.items():
        setattr(instance, attr, val)
    return instance

def get_all_objects(model_class):
    return model_class.objects.all()

def get_filtered_objects(model_class, filters):
    return model_class.objects.filter(**filters)

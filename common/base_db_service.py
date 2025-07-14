from django.shortcuts import get_object_or_404

def get_object_or_404_by_pk(model_class, pk):
    return get_object_or_404(model_class, pk=pk)

def update_instance_attributes(instance, **attrs):
    for attr, val in attrs.items():
        setattr(instance, attr, val)
    return instance

def get_all_instances(model_class):
    return model_class.objects.all()

def get_instances_by_filters(model_class, filters):
    return model_class.objects.filter(**filters)

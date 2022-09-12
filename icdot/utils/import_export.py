import tablib
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from import_export import fields, instance_loaders, resources


class ValidatingModelInstanceLoader(instance_loaders.ModelInstanceLoader):
    """
    Instance loader for Django model.

    Lookup for model instance by `import_id_fields`.
    """

    def _get_params(self, row):
        params = {}
        errors = {}

        for key in self.resource.get_import_id_fields():
            field = self.resource.fields[key]
            try:
                params[field.attribute] = field.clean(row)
            except ValueError as e:
                errors[field.attribute] = ValidationError(force_str(e), code="invalid")

        if errors:
            raise ValidationError(errors)

        return params

    def _get_instance(self, params, raise_on_does_not_exist=False):
        try:
            return self.get_queryset().get(**params)
        except self.resource._meta.model.MultipleObjectsReturned:
            raise ValidationError(
                f"More than one {self.resource._meta.model.__name__} match this row."
            )
        except self.resource._meta.model.DoesNotExist:
            if not raise_on_does_not_exist:
                return None
            raise ValidationError(
                f"No {self.resource._meta.model.__name__} matched this row."
                f" We searched using {params}."
            )

    def get_instance(self, row, raise_on_does_not_exist=False):
        """Return a mathing instance or None."""
        params = self._get_params(row)
        return self._get_instance(
            params, raise_on_does_not_exist=raise_on_does_not_exist
        )


class MultiFieldImportField(fields.Field):
    def __init__(self, resource_class, attribute=None, attribute_prefix=None, **kwargs):
        self.resource_class = resource_class
        if attribute_prefix is not None:
            self.attribute_prefix = attribute_prefix
        elif attribute is not None:
            self.attribute_prefix = attribute + "__"
        else:
            self.attribute_prefix = ""
        super().__init__(attribute=attribute, **kwargs)

    def clean(self, data, **kwargs):
        resource = self.resource_class()
        instance_loader = resource._meta.instance_loader_class(resource, dataset=None)
        if isinstance(resource, ModelResourceWithMultiFieldImport):
            return resource.get_instance(
                instance_loader, row=data, raise_on_does_not_exist=True
            )
        else:
            return resource.get_instance(instance_loader, row=data)

    def get_id_field(self, field_name):
        resource_field = self.resource_class.fields.get(field_name, None)
        if isinstance(resource_field, MultiFieldImportField):
            return MultiFieldImportField(
                resource_class=resource_field.resource_class,
                attribute_prefix=self.attribute_prefix
                + resource_field.attribute
                + "__",
                readonly=True,
            )
        else:
            return fields.Field(
                attribute=self.attribute_prefix + field_name,
                readonly=True,
            )

    def get_id_fields(self):
        return (
            self.get_id_field(field_name)
            for field_name in self.resource_class.Meta.import_id_fields
        )


class ModelResourceSanityCheck(resources.ModelDeclarativeMetaclass):
    def __new__(cls, clsname, bases, attrs):
        def meta_with_default_attributes(base, defaults):
            return type(
                "Meta",
                (base,),
                {
                    attribute: value
                    for attribute, value in defaults.items()
                    if not hasattr(base, attribute)
                },
            )

        attrs["Meta"] = meta_with_default_attributes(
            base=attrs.get("Meta", object),
            defaults={"instance_loader_class": ValidatingModelInstanceLoader},
        )

        return super().__new__(cls, clsname, bases, attrs)


class ModelResourceWithMultiFieldImport(
    resources.ModelResource, metaclass=ModelResourceSanityCheck
):
    """This ignores MultiFieldImportField in some of ModelResource's methods."""

    @staticmethod
    def _skip_multi_fields(fields):
        return [f for f in fields if not isinstance(f, MultiFieldImportField)]

    def get_export_fields(self):
        return self._skip_multi_fields(super().get_export_fields())

    def get_user_visible_fields(self):
        return self._skip_multi_fields(super().get_user_visible_fields())

    def import_data(self, dataset, **kwargs):
        clean_dataset = tablib.Dataset(
            headers=dataset.headers,
            *[
                [v if v is not None else "" for v in row.values()]
                for row in dataset.dict
                if any(v is not None and v != "" for v in row.values())
            ],
        )
        return super().import_data(dataset=clean_dataset, **kwargs)

    def import_field(self, field, obj, data, is_m2m=False, **kwargs):
        if not field.attribute:
            return  # Nowhere to save the data to.
        if field.column_name not in data and not isinstance(
            field, MultiFieldImportField
        ):
            return  # Nowhere to get the data from.
        field.save(obj, data, is_m2m, **kwargs)

    def get_instance(self, instance_loader, row, raise_on_does_not_exist=False):
        import_id_fields = [self.fields[f] for f in self.get_import_id_fields()]
        for field in self._skip_multi_fields(import_id_fields):
            if field.column_name not in row:
                raise ValueError(f"Missing identifying field {field.column_name}")

        if isinstance(instance_loader, ValidatingModelInstanceLoader):
            return instance_loader.get_instance(
                row, raise_on_does_not_exist=raise_on_does_not_exist
            )
        else:
            return instance_loader.get_instance(row)

from django.db.models.signals import post_migrate


def ensure_group_creation(app_config):

    # It is important this callback is different each
    # time we connect it to a signal below.
    def make_group_for_app(sender, **kwargs):
        # We can not import those models before this function
        # is called because apps won't have finished loading.
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        group, _ = Group.objects.get_or_create(name=f"Full access to {sender.label}")
        group.permissions.add(
            *Permission.objects.filter(
                content_type__in=ContentType.objects.filter(app_label=sender.label)
            )
        )

    post_migrate.connect(make_group_for_app, sender=app_config)

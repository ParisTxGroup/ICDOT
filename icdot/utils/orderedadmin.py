import django.contrib


class OrderedAdminSite(django.contrib.admin.AdminSite):

    models_should_be_sorted = True

    def __init__(self, *args, sort_apps=True, sort_models=True, **kwargs):
        super().__init__(*args, **kwargs)

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        app_list = app_dict.values()

        # Sort the apps alphabetically.
        app_list = sorted(app_list, key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        if self.models_should_be_sorted:
            for app in app_list:
                app['models'].sort(key=lambda x: x['name'])

        return app_list

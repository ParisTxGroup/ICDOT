from icdot.utils.orderedadmin import OrderedAdminSite


class AdminSite(OrderedAdminSite):
    site_title = "ICDOT"
    site_header = "ICDOT"

    # This allows us to order by the order in which things are
    # defined in the source code. It's implementation dependent,
    # but it should keep working fairly robustly.
    models_should_be_sorted = False

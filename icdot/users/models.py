from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_scopes import ScopedManager

from icdot.utils.threadlocal import get_current_user


class User(AbstractUser):
    """Default user for icdot."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Full Name"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserRecordingModel(models.Model):
    created_by = models.ForeignKey(
        User,
        null=True,
        editable=False,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
    )
    modified_by = models.ForeignKey(
        User,
        null=True,
        editable=False,
        related_name="%(class)s_modified",
        on_delete=models.SET_NULL,
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated:
            self.modified_by = user
            if self._state.adding:
                self.created_by = user
        super(UserRecordingModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class UserScopedModel(UserRecordingModel):
    objects = ScopedManager(user="modified_by")

    class Meta:
        abstract = True

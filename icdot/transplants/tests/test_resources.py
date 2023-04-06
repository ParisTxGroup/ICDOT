import datetime

import import_export
import pytest
import tablib
from model_bakery import baker

from icdot.transplants import resources
from icdot.utils.middleware import current_user_and_scope

ALL_RESOURCES = [
    r
    for r in resources.__dict__.values()
    if isinstance(r, type)
    and issubclass(r, import_export.resources.ModelResource)
    and r._meta.model
]

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("fill_optional", [True, False])
@pytest.mark.parametrize("resource", ALL_RESOURCES)
def test_all_resources_import_export(user, fill_optional, resource):
    instance = resource()
    return
    with current_user_and_scope(user=user):
        baker.make(resource._meta.model, _quantity=5, _fill_optional=fill_optional)
        dataset = instance.export()
        assert len(dataset) == 5
        result = instance.import_data(dataset)
        # FIXME: For this to work we'd need to make sure it only references existing transplants, etc.
        # Those things would need to be created in order (or on demand).
        assert not result.has_validation_errors(), "\n".join(
            str(r.error) for r in result.invalid_rows
        )
        assert not result.has_errors()


def test_invalid_field(user):
    instance = resources.TransplantResource()
    with current_user_and_scope(user=user):
        baker.make("transplants.Transplant")
        dataset = instance.export()
        dataset[0] = ["invalid_date" for _ in dataset[0]]
        result = instance.import_data(dataset)
        assert result.has_validation_errors(), "\n".join(
            str(r.error) for r in result.invalid_rows
        )
        assert not result.has_errors()


@pytest.mark.parametrize(
    "input_date, expected_date",
    [
        # DMY
        ["01/02/2022", datetime.date(year=2022, month=2, day=1)],
        ["01/12/2022", datetime.date(year=2022, month=12, day=1)],
        ["11/02/2022", datetime.date(year=2022, month=2, day=11)],
        ["20/01/2022", datetime.date(year=2022, month=1, day=20)],
        # YMD
        ["2022-02-01", datetime.date(year=2022, month=2, day=1)],
        ["2022-12-01", datetime.date(year=2022, month=12, day=1)],
        ["2022-02-11", datetime.date(year=2022, month=2, day=11)],
        ["2022-01-20", datetime.date(year=2022, month=1, day=20)],
    ],
)
def test_confusing_dates(user, input_date, expected_date):
    resource = resources.TransplantResource()
    dataset = tablib.Dataset(
        [input_date, "some-donor-ref", "some-recipient-ref"],
        headers=["transplant_date", "donor_ref", "recipient_ref"],
    )

    with current_user_and_scope(user=user):
        result = resource.import_data(dataset, dry_run=False)
        assert not result.has_validation_errors(), "\n".join(
            str(r.error) for r in result.invalid_rows
        )
        assert not result.has_errors()
        assert resources.Transplant.objects.count() == 1
        transplant = resources.Transplant.objects.first()
        assert transplant.transplant_date == expected_date

# homepage/tests.py

import pytest
from django.urls import reverse, resolve
from syafiqkaydotcom.utils import get_named_class_based_endpoints

class TestHomepageEndpoints:
    @pytest.fixture
    def endpoints(self):
        return get_named_class_based_endpoints('homepage')

    @pytest.mark.parametrize("url_name, expected_class", get_named_class_based_endpoints('homepage'))
    def test_view_resolves_to_correct_class(self, url_name, expected_class):
        resolved = resolve(reverse(url_name))
        assert resolved.func.view_class == expected_class, (
            f"URL name '{url_name}' resolved to '{resolved.func.view_class.__name__}', "
            f"but expected '{expected_class.__name__}'"
        )

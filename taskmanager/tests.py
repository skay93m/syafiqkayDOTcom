# taskmanager/tests.py

import pytest
from django.urls import reverse, resolve
from syafiqkaydotcom.tests.utils import get_named_class_based_endpoints

class TestTaskmanagerEndpoints:
    ENDPOINTS = get_named_class_based_endpoints('taskmanager')
    ENDPOINT_URL_NAMES = [name for name, _ in ENDPOINTS]
    
    @pytest.mark.parametrize("url_name, expected_class", ENDPOINTS)
    def test_view_resolves_to_correct_class(self, url_name, expected_class):
        resolved = resolve(reverse(url_name))
        assert resolved.func.view_class == expected_class

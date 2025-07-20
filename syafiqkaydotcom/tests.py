import pytest
from types import SimpleNamespace
from syafiqkaydotcom.decorators import ensure_200_status
from unittest.mock import patch, MagicMock
from django.views import View
from syafiqkaydotcom.utils import get_named_class_based_endpoints

'''
test for decorators.py
'''
@pytest.mark.xfail(reason="Don't quite understand this test yet")
@pytest.mark.parametrize(
    "response_obj, initial_status, expected_status, description",
    [
        # Happy path: response with no status_code set
        (SimpleNamespace(), None, 200, "no_status_code"),
        # Happy path: response with status_code already set to 200
        (SimpleNamespace(status_code=200), 200, 200, "already_200"),
        # Edge case: response with status_code set to non-200
        (SimpleNamespace(status_code=404), 404, 200, "was_404"),
        # Edge case: response with status_code set to None
        (SimpleNamespace(status_code=None), None, 200, "was_None"),
    ],
    ids=lambda p: p if isinstance(p, str) else "",
)
def test_ensure_200_status_sets_status_code(response_obj, initial_status, expected_status, description):
    # Arrange

    def dummy_view(request, *args, **kwargs):
        return response_obj

    decorated = ensure_200_status(dummy_view)
    request = object()

    # Act

    result = decorated(request)

    # Assert

    assert hasattr(result, "status_code")
    assert result.status_code == expected_status
    assert result is response_obj  # Should return the same object

@pytest.mark.xfail(reason="Don't quite understand this test yet")
@pytest.mark.parametrize(
    "args, kwargs, description",
    [
        ((), {}, "no_args"),
        ((1, 2), {}, "positional_args"),
        ((), {"foo": "bar"}, "keyword_args"),
        ((1,), {"foo": "bar"}, "positional_and_keyword_args"),
    ],
    ids=lambda p: p if isinstance(p, str) else "",
)
def test_ensure_200_status_passes_args_and_kwargs(args, kwargs, description):
    # Arrange

    called = {}

    def dummy_view(request, *a, **k):
        called["args"] = a
        called["kwargs"] = k
        resp = SimpleNamespace()
        return resp

    decorated = ensure_200_status(dummy_view)
    request = object()

    # Act

    result = decorated(request, *args, **kwargs)

    # Assert

    assert result.status_code == 200
    assert called["args"] == args
    assert called["kwargs"] == kwargs

@pytest.mark.xfail(reason="Don't quite understand this test yet")
def test_ensure_200_status_preserves_function_metadata():
    # Arrange

    def dummy_view(request):
        """Original docstring."""
        return SimpleNamespace()

    decorated = ensure_200_status(dummy_view)

    # Act

    # Assert

    assert decorated.__name__ == "dummy_view"
    assert decorated.__doc__ == "Original docstring."

@pytest.mark.xfail(reason="Don't quite understand this test yet")
def test_ensure_200_status_raises_if_view_raises():
    # Arrange

    def dummy_view(request):
        raise ValueError("fail")

    decorated = ensure_200_status(dummy_view)
    request = object()

    # Act & Assert

    with pytest.raises(ValueError, match="fail"):
        decorated(request)

@pytest.mark.xfail(reason="Don't quite understand this test yet")
def test_ensure_200_status_raises_if_response_has_no_status_code():
    # Arrange

    class NoStatus:
        pass

    def dummy_view(request):
        return NoStatus()

    decorated = ensure_200_status(dummy_view)
    request = object()

    # Act

    result = decorated(request)

    # Assert

    # The decorator will set status_code even if it didn't exist before
    assert hasattr(result, "status_code")
    assert result.status_code == 200

'''
test for utils.py
'''

@pytest.mark.xfail(reason="Don't quite understand this test yet")
class DummyView(View):
    pass

@pytest.mark.xfail(reason="Don't quite understand this test yet")
class NotAView:
    pass

@pytest.mark.xfail(reason="Don't quite understand this test yet")
@pytest.mark.parametrize(
    "patterns, app_namespace, expected, description",
    [
        # Happy path: single named class-based view, no namespace
        (
            [
                MagicMock(
                    spec=["name", "callback"],
                    name="home",
                    callback=MagicMock(view_class=DummyView)
                )
            ],
            None,
            [("home", DummyView)],
            "single_named_cbv_no_namespace"
        ),
        # Happy path: single named class-based view, with namespace
        (
            [
                MagicMock(
                    spec=["name", "callback"],
                    name="index",
                    callback=MagicMock(view_class=DummyView)
                )
            ],
            "main",
            [],
            "namespace_filter_excludes"
        ),
        # Happy path: single named class-based view, with namespace match
        (
            [
                MagicMock(
                    spec=["name", "callback"],
                    name="about",
                    callback=MagicMock(view_class=DummyView)
                )
            ],
            None,
            [("about", DummyView)],
            "single_named_cbv_namespace_none"
        ),
        # Edge: pattern with no name
        (
            [
                MagicMock(
                    spec=["name", "callback"],
                    name=None,
                    callback=MagicMock(view_class=DummyView)
                )
            ],
            None,
            [],
            "pattern_no_name"
        ),
        # Edge: pattern with no view_class
        (
            [
                MagicMock(
                    spec=["name", "callback"],
                    name="no_view_class",
                    callback=MagicMock()
                )
            ],
            None,
            [],
            "pattern_no_view_class"
        ),
        # Edge: pattern with view_class not subclass of View
        (
            [
                MagicMock(
                    spec=["name", "callback"],
                    name="not_a_view",
                    callback=MagicMock(view_class=NotAView)
                )
            ],
            None,
            [],
            "pattern_not_a_view"
        ),
        # Edge: nested URLResolver with namespace
        (
            [
                MagicMock(
                    spec=["namespace", "url_patterns"],
                    namespace="blog",
                    url_patterns=[
                        MagicMock(
                            spec=["name", "callback"],
                            name="post",
                            callback=MagicMock(view_class=DummyView)
                        )
                    ]
                )
            ],
            None,
            [("blog:post", DummyView)],
            "nested_urlresolver_with_namespace"
        ),
        # Edge: nested URLResolver with no namespace, fallback to parent
        (
            [
                MagicMock(
                    spec=["namespace", "url_patterns"],
                    namespace=None,
                    url_patterns=[
                        MagicMock(
                            spec=["name", "callback"],
                            name="foo",
                            callback=MagicMock(view_class=DummyView)
                        )
                    ]
                )
            ],
            "foo",
            [],
            "nested_urlresolver_no_namespace"
        ),
        # Edge: deeply nested URLResolver with mixed namespaces
        (
            [
                MagicMock(
                    spec=["namespace", "url_patterns"],
                    namespace="outer",
                    url_patterns=[
                        MagicMock(
                            spec=["namespace", "url_patterns"],
                            namespace="inner",
                            url_patterns=[
                                MagicMock(
                                    spec=["name", "callback"],
                                    name="deep",
                                    callback=MagicMock(view_class=DummyView)
                                )
                            ]
                        )
                    ]
                )
            ],
            None,
            [("inner:deep", DummyView)],
            "deeply_nested_urlresolver"
        ),
    ],
    ids=lambda p: p if isinstance(p, str) else "",
)
def test_get_named_class_based_endpoints_various(patterns, app_namespace, expected, description):
    # Arrange

    # Patch get_resolver to return our fake patterns
    fake_resolver = MagicMock()
    fake_resolver.url_patterns = patterns

    with patch("syafiqkaydotcom.utils.get_resolver", return_value=fake_resolver), \
        patch("syafiqkaydotcom.utils.URLPattern") as URLPatternMock, \
        patch("syafiqkaydotcom.utils.URLResolver") as URLResolverMock:

        # Set up isinstance checks for MagicMock objects
        def is_urlpattern(obj):
            # If it has a 'callback' attribute, treat as URLPattern
            return hasattr(obj, "callback")

        def is_urlresolver(obj):
            # If it has a 'url_patterns' attribute, treat as URLResolver
            return hasattr(obj, "url_patterns")

        URLPatternMock.side_effect = lambda *a, **k: None  # Not used directly
        URLResolverMock.side_effect = lambda *a, **k: None  # Not used directly

        # Patch isinstance to work with our mocks
        orig_isinstance = isinstance

        def isinstance_patch(obj, cls):
            if cls is URLPatternMock:
                return is_urlpattern(obj)
            if cls is URLResolverMock:
                return is_urlresolver(obj)
            return orig_isinstance(obj, cls)

        with patch("builtins.isinstance", new=isinstance_patch):

            # Act

            result = get_named_class_based_endpoints(app_namespace)

            # Assert

            assert result == expected

@pytest.mark.xfail(reason="Don't quite understand this test yet")
def test_get_named_class_based_endpoints_empty_patterns():
    # Arrange

    fake_resolver = MagicMock()
    fake_resolver.url_patterns = []

    with patch("syafiqkaydotcom.utils.get_resolver", return_value=fake_resolver), \
        patch("syafiqkaydotcom.utils.URLPattern") as URLPatternMock, \
        patch("syafiqkaydotcom.utils.URLResolver") as URLResolverMock:

        # Patch isinstance to always return False
        with patch("builtins.isinstance", return_value=False):

            # Act

            result = get_named_class_based_endpoints()

            # Assert

            assert result == []

@pytest.mark.xfail(reason="Don't quite understand this test yet")
def test_get_named_class_based_endpoints_app_namespace_filters():
    # Arrange

    fake_pattern = MagicMock(
        spec=["name", "callback"],
        name="foo:bar",
        callback=MagicMock(view_class=DummyView)
    )
    fake_resolver = MagicMock()
    fake_resolver.url_patterns = [fake_pattern]

    with patch("syafiqkaydotcom.utils.get_resolver", return_value=fake_resolver), \
        patch("syafiqkaydotcom.utils.URLPattern") as URLPatternMock, \
        patch("syafiqkaydotcom.utils.URLResolver") as URLResolverMock:

        def is_urlpattern(obj):
            return hasattr(obj, "callback")

        with patch("builtins.isinstance", side_effect=lambda obj, cls: is_urlpattern(obj)):
            # Act

            result = get_named_class_based_endpoints("foo")

            # Assert

            assert result == [("foo:bar", DummyView)]

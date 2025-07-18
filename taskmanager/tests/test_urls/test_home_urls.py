# taskmanager/tests/test_urls/test_home_urls.py

def test_home_url(client):
    """
    Test that the home URL ('/') returns a 200 status code and uses the correct template.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert 'templates/taskmanager.html' in [t.name for t in response.templates]
def test_home_url(client):
    response = client.get('/')
def test_help_url(client):
    """
    Test that the help page URL returns a 200 status and uses the correct template.
    """
    response = client.get('/help/')
    assert response.status_code == 200
    assert 'templates/help.html' in [t.name for t in response.templates]
    response = client.get('/help/')
    assert response.status_code == 200
    assert 'templates/help.html' in [t.name for t in response.templates]

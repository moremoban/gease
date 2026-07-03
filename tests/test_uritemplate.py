from gease.uritemplate import UriTemplate, is_partial, extract_variables


def test_extract_variables():
    url = "{/abc}{/dde}"
    variables = extract_variables(url)
    assert variables == ["abc", "dde"]


def test_extract_variables_got_empty():
    url = ""
    variables = extract_variables(url)
    assert variables == []


def test_uri_template_variable():
    template = UriTemplate("http://abc{/cute}")
    assert template.cute is None


def test_uri_template_template():
    template = UriTemplate("http://abc{/cute}")
    template.cute = "world"
    assert str(template) == "http://abc/world"


def test_uri_template_template2():
    template = UriTemplate("http://abc{/cute}")
    assert template(cute="world") == "http://abc/world"


def test_uri_template_partial_apply():
    template = UriTemplate("http://abc{/cute}{/left}")
    assert template(cute="world") == "http://abc/world{/left}"


def test_is_partial():
    url = "{/abc}"
    assert is_partial(url) is True


def test_is_partial_2():
    url = UriTemplate("{/abc}")
    assert url.is_partial() is True


def test_get_original_template():
    original = "{/abc}"
    url = UriTemplate("{/abc}")
    assert url.get_template_string() is original

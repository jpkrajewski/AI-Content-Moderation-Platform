import pytest
from connexion.exceptions import Unauthorized
from moderation.auth.common import check_scopes


@pytest.mark.parametrize(
    "scopes, required_scopes, should_raise",
    [
        (None, None, False),
        ([], [], False),
        ([], ["scope1"], True),
        (["scope1"], [], False),
        (["scope1", "scope2"], ["scope1"], False),
        (["scope1"], ["scope2"], True),
    ],
)
def test_check_scopes(scopes, required_scopes, should_raise):
    if should_raise:
        with pytest.raises(Unauthorized):
            check_scopes(scopes, required_scopes)
    else:
        assert check_scopes(scopes, required_scopes) is None

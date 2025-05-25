def test_create_api_key(client_api_key_service):
    client_id = "client123"
    scope = ["read", "write"]
    source = "unit-test"

    api_key_obj = client_api_key_service.create_api_key(client_id=client_id, current_scope=scope, source=source)

    assert api_key_obj is not None
    assert api_key_obj.client_id == client_id
    assert api_key_obj.current_scope == scope
    assert api_key_obj.source == source
    assert api_key_obj.is_active


def test_get_api_key(client_api_key_service):
    client_id = "client456"
    scope = ["read"]
    source = "unit-test-2"

    created_key = client_api_key_service.create_api_key(client_id=client_id, current_scope=scope, source=source)

    fetched_key = client_api_key_service.get_api_key(created_key.id)
    assert fetched_key is not None
    assert fetched_key.id == created_key.id


def test_update_api_key(client_api_key_service):
    client_id = "client789"
    scope = ["read"]
    source = "unit-test-3"

    api_key_obj = client_api_key_service.create_api_key(client_id=client_id, current_scope=scope, source=source)

    update_data = {"is_active": False}
    updated_key = client_api_key_service.update_api_key(api_key_obj.id, update_data)

    assert updated_key is not None
    assert updated_key.is_active is False


def test_deactivate_and_reactivate_api_key(client_api_key_service):
    client_id = "client999"
    scope = ["read"]
    source = "unit-test-4"

    api_key_obj = client_api_key_service.create_api_key(client_id=client_id, current_scope=scope, source=source)

    deactivated = client_api_key_service.deactivate_api_key(api_key_obj.id)
    assert deactivated is not None
    assert deactivated.is_active is False

    reactivated = client_api_key_service.reactivate_api_key(api_key_obj.id)
    assert reactivated is not None
    assert reactivated.is_active is True


def test_list_api_keys(client_api_key_service):
    # Just test it returns a list
    keys = client_api_key_service.list_api_keys()
    assert isinstance(keys, list)

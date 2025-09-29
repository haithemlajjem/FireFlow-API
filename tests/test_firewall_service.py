import pytest

from app.models.firewall import Firewall
from app.services.firewall import (
    create_firewall,
    delete_firewall,
    get_firewall,
    list_firewalls,
    update_firewall,
)


@pytest.mark.parametrize(
    "name,description",
    [
        ("fw1", "First firewall"),
        ("fw2", None),
    ],
)
def test_create_firewall(db_session, name, description):
    """
    Test creating firewalls with different names and optional descriptions.
    Ensures a firewall is created, has an ID, and matches the given name and description.
    """
    fw = create_firewall(db_session, name, description)
    assert fw.id is not None
    assert fw.name == name
    assert fw.description == description


def test_create_firewall_duplicate_name(db_session):
    """
    Test creating two firewalls with the same name.
    The second creation should raise a ValueError due to unique constraint.
    """
    create_firewall(db_session, "fw_unique", "desc")
    with pytest.raises(ValueError):
        create_firewall(db_session, "fw_unique", "another desc")


def test_update_firewall(db_session):
    """
    Test updating a firewall's name and description.
    Ensures the updated firewall has new values and retains the same ID.
    """
    fw = create_firewall(db_session, "fw_update", "desc")
    updated_fw = update_firewall(db_session, fw.id, "fw_new", "new desc")
    assert updated_fw.id == fw.id
    assert updated_fw.name == "fw_new"
    assert updated_fw.description == "new desc"


def test_update_nonexistent_firewall(db_session):
    """
    Test updating a firewall that does not exist.
    Should return None without raising an exception.
    """
    result = update_firewall(db_session, 9999, "no_fw", "desc")
    assert result is None


def test_get_firewall(db_session):
    """
    Test retrieving a firewall by ID.
    Ensures the correct firewall is returned with the expected name.
    """
    fw = create_firewall(db_session, "fw_get", "desc")
    fetched = get_firewall(db_session, fw.id)
    assert fetched.id == fw.id
    assert fetched.name == "fw_get"


def test_get_nonexistent_firewall(db_session):
    """
    Test retrieving a firewall that does not exist.
    Should return None.
    """
    fetched = get_firewall(db_session, 9999)
    assert fetched is None


def test_delete_firewall(db_session):
    """
    Test deleting an existing firewall.
    After deletion, the firewall should no longer be retrievable.
    """
    fw = create_firewall(db_session, "fw_del", "desc")
    result = delete_firewall(db_session, fw.id)
    assert result is True
    assert get_firewall(db_session, fw.id) is None


def test_delete_nonexistent_firewall(db_session):
    """
    Test deleting a firewall that does not exist.
    Should return False without raising an exception.
    """
    result = delete_firewall(db_session, 9999)
    assert result is False


def test_list_firewalls(db_session):
    """
    Test listing all firewalls.
    Ensures that all created firewalls appear in the list.
    """
    # Clear session for consistent test
    db_session.query(Firewall).delete()
    db_session.commit()

    fw1 = create_firewall(db_session, "fw_list1", "desc1")
    fw2 = create_firewall(db_session, "fw_list2", "desc2")
    firewalls = list_firewalls(db_session)
    assert len(firewalls) == 2
    ids = [fw.id for fw in firewalls]
    assert fw1.id in ids
    assert fw2.id in ids

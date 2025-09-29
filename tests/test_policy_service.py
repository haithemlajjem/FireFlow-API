import pytest

from app.models.firewall import Firewall
from app.models.policy import FilteringPolicy
from app.services.policy import add_policy, delete_policy, list_policies


@pytest.mark.parametrize("fw_name", ["fw1", "fw2"])
def test_add_policy(db_session, fw_name):
    """Test adding a policy with optional rules to a firewall."""
    fw = Firewall(name=fw_name)
    db_session.add(fw)
    db_session.commit()
    db_session.refresh(fw)

    policy = add_policy(db_session, fw.id, "policy1", [])
    assert policy.id is not None
    assert policy.name == "policy1"
    assert policy.rules == []


def test_add_policy_invalid_firewall(db_session):
    """Adding a policy to a non-existent firewall should raise ValueError."""
    with pytest.raises(ValueError):
        add_policy(db_session, 9999, "policy_fail", [])


def test_list_policies(db_session):
    """List all policies for a given firewall."""
    fw = Firewall(name="fw_list")
    db_session.add(fw)
    db_session.commit()
    db_session.refresh(fw)

    add_policy(db_session, fw.id, "p1", [])
    add_policy(db_session, fw.id, "p2", [])
    policies = list_policies(db_session, fw.id)
    assert len(policies) == 2
    names = [p.name for p in policies]
    assert "p1" in names and "p2" in names


def test_list_policies_invalid_firewall(db_session):
    """Listing policies for a non-existent firewall should raise ValueError."""
    with pytest.raises(ValueError):
        list_policies(db_session, 9999)


def test_delete_policy(db_session):
    """Delete an existing policy."""
    fw = Firewall(name="fw_del_policy")
    db_session.add(fw)
    db_session.commit()
    db_session.refresh(fw)

    policy = add_policy(db_session, fw.id, "to_delete", [])
    result = delete_policy(db_session, policy.id)
    assert result is True
    assert db_session.get(FilteringPolicy, policy.id) is None


def test_delete_nonexistent_policy(db_session):
    """Deleting a non-existent policy should return False."""
    result = delete_policy(db_session, 9999)
    assert result is False

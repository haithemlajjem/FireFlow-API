import pytest

from app.models.firewall import Firewall
from app.models.rule import Rule
from app.services.policy import add_policy
from app.services.rule import add_rule, delete_rule, list_rules


@pytest.mark.parametrize("action", ["allow", "deny"])
def test_add_rule(db_session, action, request):
    """Add a rule to a policy with different actions."""
    # Make the firewall name unique per test iteration
    fw_name = f"fw_rule_{action}"
    fw = Firewall(name=fw_name)
    db_session.add(fw)
    db_session.commit()
    db_session.refresh(fw)

    policy = add_policy(db_session, fw.id, f"policy_{action}", [])
    rule = add_rule(db_session, policy.id, action, "1.1.1.1", "2.2.2.2", "tcp")

    assert rule.id is not None
    assert rule.action == action
    assert rule.src == "1.1.1.1"
    assert rule.dst == "2.2.2.2"
    assert rule.protocol == "tcp"


def test_add_rule_invalid_policy(db_session):
    """Adding a rule to a non-existent policy should raise ValueError."""
    with pytest.raises(ValueError):
        add_rule(db_session, 9999, "allow")


def test_list_rules(db_session):
    """List all rules for a given policy."""
    fw = Firewall(name="fw_list_rules")
    db_session.add(fw)
    db_session.commit()
    db_session.refresh(fw)

    policy = add_policy(db_session, fw.id, "policy_rules", [])
    add_rule(db_session, policy.id, "allow")
    add_rule(db_session, policy.id, "deny")
    rules = list_rules(db_session, policy.id)
    assert len(rules) == 2
    actions = [r.action for r in rules]
    assert "allow" in actions and "deny" in actions


def test_list_rules_invalid_policy(db_session):
    """Listing rules for a non-existent policy should raise ValueError."""
    with pytest.raises(ValueError):
        list_rules(db_session, 9999)


def test_delete_rule(db_session):
    """Delete an existing rule."""
    fw = Firewall(name="fw_del_rule")
    db_session.add(fw)
    db_session.commit()
    db_session.refresh(fw)

    policy = add_policy(db_session, fw.id, "policy_del_rule", [])
    rule = add_rule(db_session, policy.id, "allow")
    result = delete_rule(db_session, rule.id)
    assert result is True
    assert db_session.get(Rule, rule.id) is None


def test_delete_nonexistent_rule(db_session):
    """Deleting a non-existent rule should return False."""
    result = delete_rule(db_session, 9999)
    assert result is False

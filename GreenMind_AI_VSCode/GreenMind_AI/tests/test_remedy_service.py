from app.database.remedy_service import get_remedy, prettify


def test_known_disease_has_facts():
    facts = get_remedy("Tomato___Late_blight")
    assert facts["plant"] == "Tomato"
    assert facts["symptoms"]
    assert facts["prevention"]


def test_label_is_presentable():
    assert prettify("Apple___Apple_scab") == "Apple — Apple scab"

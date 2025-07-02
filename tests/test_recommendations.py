def test_recommendations_for_consent_processing(client, db_session, tenant):
    # given
    processing = Processing(
        name="Newsletter",
        purpose="Marketing",
        legal_basis=LegalBasisEnum.CONSENT,
        data_subjects=["Prospects"],
        data_categories=["Email"],
        tenant_id=tenant.id,
    )
    db_session.add(processing); db_session.commit(); db_session.refresh(processing)

    # when
    r = client.get(f"/api/rgpd/processings/{processing.id}/actions")
    # then
    assert r.status_code == 200
    labels = [a["label"] for a in r.json()]
    assert any("Collecte du consentement" in lbl for lbl in labels)

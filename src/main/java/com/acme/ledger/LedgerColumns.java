package com.acme.ledger;

import java.sql.ResultSet;
import java.sql.SQLException;

public final class LedgerColumns {

    static final String COL_EMAIL = "email_address";
    static final String COL_TAX_ID = "taxpayer_id";
    static final String CSS_EMAIL = "email_address";
    static final String DEFAULT_SENDER = "maria@example.com";
    static final String METRIC_NAME = "phone_number";

    public Contact read(ResultSet rs) throws SQLException {
        Contact contact = new Contact();
        contact.setEmail(rs.getString(COL_EMAIL));
        contact.setTaxId(rs.getString(COL_TAX_ID));
        return contact;
    }

    public void style(Element el) {
        el.addClass(CSS_EMAIL);
    }

    public void record(Metrics metrics) {
        metrics.increment(METRIC_NAME);
    }
}

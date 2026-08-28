package com.acme.ledger;

public class ContactMapping extends BaseMapping {

    public ContactMapping(QueryBuilder queryBuilder) {
        this.addMapping("meta.createdBy.firstName", "createdBy");
        this.addMapping("meta.createdBy.lastName", "createdBy");
        this.addMapping("meta.updated", "lastUpdatedTimestamp");
        this.addMapping("workflowPhase", "phase");

        queryBuilder.select("home_address").from("residents");
        queryBuilder.select("date_of_birth").from("residents");
        queryBuilder.select("unit_count").from("buildings");
    }
}

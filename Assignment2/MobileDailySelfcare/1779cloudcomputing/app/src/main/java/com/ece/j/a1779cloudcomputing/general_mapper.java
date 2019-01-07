package com.ece.j.a1779cloudcomputing;

import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBAttribute;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBTable;

@DynamoDBTable(tableName = "questionaire")
public class general_mapper {

    public general_mapper(){

    }

    private String userdate1;

    @DynamoDBHashKey(attributeName = "user-date")
    public String getUsername() {
        return userdate1;
    }
    public void setUsername(String u) {
        this.userdate1 = u;
    }


}

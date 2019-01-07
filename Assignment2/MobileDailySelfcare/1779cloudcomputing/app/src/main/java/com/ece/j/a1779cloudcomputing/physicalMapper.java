package com.ece.j.a1779cloudcomputing;

import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBAttribute;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBTable;

/**
 * Created by J on 4/15/2017.
 */


@DynamoDBTable(tableName = "physical")
public class physicalMapper {

    public physicalMapper(){

    }

    private int number;
    private String content;

    @DynamoDBHashKey(attributeName = "number")
    public int getNumber() {
        return number;
    }
    public void setNumber(int u) {
        this.number = u;
    }

    @DynamoDBAttribute( attributeName = "content")
    public String getContent() {
        return content;
    }
    public void setContent (String p) {
        this.content = p;
    }
}

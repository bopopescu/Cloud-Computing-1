package com.ece.j.a1779cloudcomputing;

import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBAttribute;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBIndexHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBTable;

/**
 * Created by J on 4/8/2017.
 */


@DynamoDBTable(tableName = "users")
public class UserMapper {

    public UserMapper(){

    }

    private String username;
    private String password;

    @DynamoDBHashKey(attributeName = "username")
    public String getUsername() {
        return username;
    }
    public void setUsername(String u) {
        this.username = u;
    }

    @DynamoDBAttribute( attributeName = "password")
    public String getPassword() {
        return password;
    }
    public void setPassword (String p) {
        this.password = p;
    }
}

package com.ece.j.a1779cloudcomputing;

import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBAttribute;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBIndexHashKey;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBTable;

/**
 * Created by J on 4/8/2017.
 */


@DynamoDBTable(tableName = "questionaire")
public class Ques_mapper {

    public Ques_mapper(){

    }

    private String user_date, date;
    private int day;
    private String q1,q2,q3,q4,q5;

    @DynamoDBHashKey(attributeName = "user-date")
    public String getUserdate() {
        return user_date;
    }
    public void setUsername(String u) {
        this.user_date = u;
    }

    @DynamoDBAttribute( attributeName = "day")
    public int getday() {
        return day;
    }
    public void setDay (int p) {
        this.day = p;
    }

    @DynamoDBAttribute( attributeName = "q1")
    public String getQ1() {
        return q1;
    }
    public void setQ1 (String p) {
        this.q1 = p;
    }
    @DynamoDBAttribute( attributeName = "q2")
    public String getQ2() {
        return q2;
    }
    public void setQ2 (String p) {
        this.q2 = p;
    }
    @DynamoDBAttribute( attributeName = "q3")
    public String getQ3() {
        return q3;
    }
    public void setQ3 (String p) {
        this.q3 = p;
    }
    @DynamoDBAttribute( attributeName = "q4")
    public String getQ4() {
        return q4;
    }
    public void setQ4 (String p) {
        this.q4 = p;
    }
    @DynamoDBAttribute( attributeName = "q5")
    public String getQ5() {
        return q5;
    }
    public void setQ5 (String p) {
        this.q5 = p;
    }

    @DynamoDBAttribute ( attributeName = "date")
    public String getDate() {
        return date;
    }
    public void setDate (String s) {
        this.date = s;
    }
}

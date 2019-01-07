package com.ece.j.a1779cloudcomputing;

import android.content.Context;
import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobileconnectors.cognito.CognitoSyncManager;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;
import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.dynamodbv2.*;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.*;
import com.amazonaws.services.dynamodbv2.model.*;

/**
 * Created by J on 4/8/2017.
 */

public class dynamotest {

    public dynamotest() {
    }

    public CognitoCachingCredentialsProvider get_cred(Context context){
        // Initialize the Amazon Cognito credentials provider
        CognitoCachingCredentialsProvider credentialsProvider = new CognitoCachingCredentialsProvider(
                context,
                "us-east-1:27e349b3-1832-4988-8a39-ee283c617a45", // Identity Pool ID
                Regions.US_EAST_1 // Region
        );


        return credentialsProvider;
    }


//    public getDB(){
//        CognitoSyncManager syncClient = new CognitoSyncManager(
//                getApplicationContext(),
//                Regions.US_EAST_1, // Region
//                credentialsProvider);
//    }


}




//// Initialize the Cognito Sync client
//        CognitoSyncManager syncClient = new CognitoSyncManager(
//        getApplicationContext(),
//        Regions.US_EAST_1, // Region
//        credentialsProvider);
//
//// Create a record in a dataset and synchronize with the server
//        Dataset dataset = syncClient.openOrCreateDataset("myDataset");
//        dataset.put("myKey", "myValue");
//        dataset.synchronize(new DefaultSyncCallback() {
//@Override
//public void onSuccess(Dataset dataset, List newRecords) {
//        //Your handler code here
//        }
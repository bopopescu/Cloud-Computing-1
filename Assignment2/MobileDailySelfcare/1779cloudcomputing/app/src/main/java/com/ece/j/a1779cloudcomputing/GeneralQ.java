package com.ece.j.a1779cloudcomputing;


import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.RadioGroup;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBMapper;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import static android.R.attr.fragment;
import static com.ece.j.a1779cloudcomputing.LoginActivity.username;


/**
 * A simple {@link Fragment} subclass.
 */
public class GeneralQ extends Fragment {


    public GeneralQ() {
        // Required empty public constructor
    }

        private int[] q_result = new int[7];
    private Button submit;
    private Spinner g1;
    private RadioGroup g2;
    private RadioGroup g3;
    private RadioGroup g4;
    private Spinner g5;
    boolean all_answered = false;
    UserSubmitTask mSubTask = null;
    checkCompletionTask checkTask = null;
    boolean completed = false;
    boolean prev = true;
    String tag;
    TextView comp = null;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        //check if entry exist
        checkTask = new checkCompletionTask();
        checkTask.execute((Void) null);

        tag = this.getTag();
        Log.v("testaaa", tag);


//         Inflate the layout for this fragment
        View v = inflater.inflate(R.layout.fragment_general_q, container, false);
        g1 = (Spinner) v.findViewById(R.id.g1spinner);
        g2 = (RadioGroup) v.findViewById(R.id.g2);
        g3 = (RadioGroup) v.findViewById(R.id.g3);
        g4 = (RadioGroup) v.findViewById(R.id.g4);
        g5 = (Spinner) v.findViewById(R.id.g5spinner);
        submit = (Button) v.findViewById(R.id.g_match_button);
        comp = (TextView) v.findViewById(R.id.completed);
        if (completed) {
            comp.setVisibility(View.VISIBLE);
        }

        List<String> list1 = Arrays.asList("0","1","2","3","4","5","6","7","8","9");


        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_spinner_item, list1);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        g1.setAdapter(dataAdapter);
        g5.setAdapter(dataAdapter);













        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                List<String> ans = Arrays.asList(String.valueOf(g1.getSelectedItem()),
                        get_radio_id(g2),get_radio_id(g3),get_radio_id(g4),String.valueOf(g5.getSelectedItem()));
                if (ans.contains("-1")){
                    Toast.makeText(getActivity(), "Please answer all fields!",
                            Toast.LENGTH_LONG).show();
                } else {
                    Log.v("testaaa",ans.toString());
                    //upload an entry to dynamo

                    mSubTask = new UserSubmitTask(ans);
                    mSubTask.execute((Void) null);

                }

            }
        });



        return v;
    }

    public class UserSubmitTask extends AsyncTask<Void, Void, Boolean> {

        private final List<String> ans;

        UserSubmitTask(List<String> answ) {
            ans = answ;
        }

        @Override
        protected Boolean doInBackground(Void... params) {

            try {
                // Simulate network access.
                dynamotest dn = new dynamotest();
                CognitoCachingCredentialsProvider credentialsProvider = dn.get_cred(getContext());
                AmazonDynamoDBClient ddbClient = new AmazonDynamoDBClient(credentialsProvider);
                DynamoDBMapper mapper = new DynamoDBMapper(ddbClient);


                Ques_mapper quesMapper = new Ques_mapper();
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd");
                String date = sdf.format(new Date());

                Calendar calendar = Calendar.getInstance();
                int dayOfYear = calendar.get(Calendar.DAY_OF_YEAR);
                quesMapper.setUsername(username+"-"+date);
                quesMapper.setQ1(ans.get(0));
                quesMapper.setQ2(ans.get(1));
                quesMapper.setQ3(ans.get(2));
                quesMapper.setQ4(ans.get(3));
                quesMapper.setQ5(ans.get(4));
                quesMapper.setDay(dayOfYear);
                quesMapper.setDate(date);
                Log.v("testaaa",ans.toString()+"--"+username+date+"--"+String.valueOf(dayOfYear));
                mapper.save(quesMapper);
            } catch (Exception e) {
                return false;
            }
            return true;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            if (success) {
                Toast.makeText(getActivity(), "Submission Complete!",
                        Toast.LENGTH_LONG).show();
                Log.v("testaaa", "success submit");
                completed = true;
                prev = completed;
                comp.setVisibility(View.VISIBLE);
                Fragment currentFragment = getFragmentManager().findFragmentByTag(tag);
                FragmentTransaction fragTransaction = getFragmentManager().beginTransaction();
                fragTransaction.detach(currentFragment);
                fragTransaction.attach(currentFragment);
                fragTransaction.commit();
            } else {
                Toast.makeText(getActivity(), "Submission Failed! Please try again!",
                        Toast.LENGTH_LONG).show();
            }
            mSubTask = null;
        }

        @Override
        protected void onCancelled() {
            mSubTask = null;
        }
    }

    private String get_radio_id(RadioGroup radioGroup){
        int radioID = radioGroup.getCheckedRadioButtonId();
        View rButton = radioGroup.findViewById(radioID);
        int index = radioGroup.indexOfChild(rButton);
        return String.valueOf(index);
    }


    public class checkCompletionTask extends AsyncTask<Void, Void, Boolean> {


        checkCompletionTask() {

        }

        @Override
        protected Boolean doInBackground(Void... params) {

            try {
                // Simulate network access.
                dynamotest dn = new dynamotest();
                CognitoCachingCredentialsProvider credentialsProvider = dn.get_cred(getContext());
                AmazonDynamoDBClient ddbClient = new AmazonDynamoDBClient(credentialsProvider);
                DynamoDBMapper mapper = new DynamoDBMapper(ddbClient);


                SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd");
                String date = sdf.format(new Date());
                String userdate = username+"-"+date;

                //find userdate in db;
                Log.v("testaaa", userdate);

                general_mapper gen = mapper.load(general_mapper.class, userdate);
                if (gen == null ){
                    return false;
                }
            } catch (Exception e) {
                return false;
            }
            return true;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            if (success) {
                Log.v("testaaa", "found entry");
                if (completed != prev){
                    prev = true;
                    completed = true;
                    comp.setVisibility(View.VISIBLE);
                    Fragment currentFragment = getFragmentManager().findFragmentByTag(tag);
                    FragmentTransaction fragTransaction = getFragmentManager().beginTransaction();
                    fragTransaction.detach(currentFragment);
                    fragTransaction.attach(currentFragment);
                    fragTransaction.commit();
                }
            } else {
                Log.v("testaaa", "not found entry");
                if(completed != prev){
                    prev = false;
                    completed = false;
                    comp.setVisibility(View.INVISIBLE);
                    Fragment currentFragment = getFragmentManager().findFragmentByTag(tag);
                    FragmentTransaction fragTransaction = getFragmentManager().beginTransaction();
                    fragTransaction.detach(currentFragment);
                    fragTransaction.attach(currentFragment);
                    fragTransaction.commit();
                }
            }
            checkTask = null;
        }

        @Override
        protected void onCancelled() {
            checkTask = null;
        }
    }


}

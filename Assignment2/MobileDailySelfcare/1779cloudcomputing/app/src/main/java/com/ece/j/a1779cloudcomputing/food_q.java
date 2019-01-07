package com.ece.j.a1779cloudcomputing;


import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.RadioGroup;

import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBMapper;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;

import java.util.ArrayList;


/**
 * A simple {@link Fragment} subclass.
 */
public class food_q extends Fragment {


    public food_q() {
        // Required empty public constructor
    }

    private GetTipTask mGetTipTask = null;
    RadioGroup g1;
    int answer;
    int[] selected_list;
    ArrayList<String> tip_list = new ArrayList<>();
    Button sub;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View v = inflater.inflate(R.layout.fragment_food_q, container, false);
        g1 = (RadioGroup) v.findViewById(R.id.f2);
        sub = (Button) v.findViewById(R.id.f_sub);

        sub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(g1.getCheckedRadioButtonId() == -1) return;
                answer = g1.indexOfChild(g1.findViewById(g1.getCheckedRadioButtonId()));
                Log.v("testaaa",String.valueOf(answer));
                mGetTipTask = new GetTipTask();
                switch(answer) {
                    case 0:
                        mGetTipTask.execute(1,6,7,9,14,15);
                        break;
                    case 1:
                        mGetTipTask.execute(6,7);
                        break;
                    case 2:
                        mGetTipTask.execute(1,14,15,16);
                        break;
                    case 3:
                        mGetTipTask.execute(2,3,4,5,8,10,11,12,13);
                        break;
                    default:
                        mGetTipTask.execute(1);
                        break;

                }
            }
        });

        return v;
    }


    public class GetTipTask extends AsyncTask<Integer, Void, Boolean> {

        GetTipTask() {

        }

        @Override
        protected Boolean doInBackground(Integer... params) {

            try {
                // Simulate network access.
                dynamotest dn = new dynamotest();
                CognitoCachingCredentialsProvider credentialsProvider = dn.get_cred(getContext());
                AmazonDynamoDBClient ddbClient = new AmazonDynamoDBClient(credentialsProvider);
                DynamoDBMapper mapper = new DynamoDBMapper(ddbClient);
                for (int i : params){
                    foodMapper map = mapper.load(foodMapper.class, i);
                    if(map != null && map.getContent() != null) {
                        tip_list.add(map.getContent());
                    }

                }

            } catch (Exception e) {
                return false;
            }
            return true;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            mGetTipTask = null;
//            showProgress(false);
            if (success) {
                Intent intent = new Intent(getContext(), TipsActivity.class);
                Bundle b = new Bundle();
                b.putStringArrayList("tips",tip_list);
                b.putString("tit","Food tips");
                intent.putExtras(b);
                //goto q
                startActivity(intent);
                tip_list.clear();
            } else {
            }
        }

        @Override
        protected void onCancelled() {
            mGetTipTask = null;
//            showProgress(false);
        }
    }
}

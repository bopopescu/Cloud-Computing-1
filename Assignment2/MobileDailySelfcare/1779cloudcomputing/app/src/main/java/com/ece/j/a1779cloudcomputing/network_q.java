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
public class network_q extends Fragment {


    public network_q() {
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
        View v = inflater.inflate(R.layout.fragment_network_q, container, false);
        g1 = (RadioGroup) v.findViewById(R.id.n2);
        sub = (Button) v.findViewById(R.id.n_sub);

        sub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(g1.getCheckedRadioButtonId() == -1) return;
                answer = g1.indexOfChild(g1.findViewById(g1.getCheckedRadioButtonId()));
                Log.v("testaaa",String.valueOf(answer));
                mGetTipTask = new GetTipTask();
                switch(answer) {
                    case 2:
                        mGetTipTask.execute(3);
                        break;
                    case 3:
                        mGetTipTask.execute(3);
                        break;
                    default:
                        mGetTipTask.execute(1,2);
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
                    networkMapper map = mapper.load(networkMapper.class, i);
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
                b.putString("tit","Network tips");
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

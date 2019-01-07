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
public class Physical_q extends Fragment {


    public Physical_q() {
        // Required empty public constructor
    }

    private GetTipTask mGetTipTask = null;
    RadioGroup g1,g2,g3;
    int[] answer_list = new int[3];
    int[] selected_list;
    ArrayList<String> tip_list = new ArrayList<>();
    Button sub;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_physical_q, container, false);
        g1 = (RadioGroup) v.findViewById(R.id.p2);
        g2 = (RadioGroup) v.findViewById(R.id.p3);
        g3 = (RadioGroup) v.findViewById(R.id.p4);

        sub = (Button) v.findViewById(R.id.p_sub);

        sub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(g1.getCheckedRadioButtonId() == -1 ||g2.getCheckedRadioButtonId() == -1 ||g3.getCheckedRadioButtonId() == -1) return;
                answer_list[0] = g1.indexOfChild(g1.findViewById(g1.getCheckedRadioButtonId()));
                answer_list[1] = g2.indexOfChild(g2.findViewById(g2.getCheckedRadioButtonId()));
                answer_list[2] = g3.indexOfChild(g3.findViewById(g3.getCheckedRadioButtonId()));
                mGetTipTask = new GetTipTask();
                mGetTipTask.execute(1,2,3,4,5,6,7,8,9);

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
                    physicalMapper aca = mapper.load(physicalMapper.class, i);
                    if(aca != null && aca.getContent() != null) {
                        tip_list.add(aca.getContent());
                        Log.v("testaaa",aca.getContent());

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
                b.putString("tit","Physical tips");
                intent.putExtras(b);
                //goto q
                startActivity(intent);
                tip_list.clear();
                Log.v("testaaa", "success login");
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

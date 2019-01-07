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
import android.widget.SeekBar;

import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobileconnectors.dynamodbv2.dynamodbmapper.DynamoDBMapper;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;

import java.lang.reflect.Array;
import java.util.ArrayList;


/**
 * A simple {@link Fragment} subclass.
 */
public class AcadQ extends Fragment {


    public AcadQ() {
        // Required empty public constructor
    }

    private GetTipTask mGetTipTask = null;
    RadioGroup g1, g2, g3;
    int[] answer_list = new int[3];
    int[] selected_list = new int[3];
    ArrayList<String> tip_list = new ArrayList<>();
    Button sub;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
//         Inflate the layout for this fragment
        View v = inflater.inflate(R.layout.fragment_acad_q, container, false);
        g1 = (RadioGroup) v.findViewById(R.id.a1);
        g2 = (RadioGroup) v.findViewById(R.id.a2);
        g3 = (RadioGroup) v.findViewById(R.id.a3);
        sub = (Button) v.findViewById(R.id.a_sub);


        sub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (g1.getCheckedRadioButtonId() == -1 || g2.getCheckedRadioButtonId() == -1 || g3.getCheckedRadioButtonId() == -1 )
                answer_list[0] = g1.indexOfChild(g1.findViewById(g1.getCheckedRadioButtonId()));
                answer_list[1] = g2.indexOfChild(g2.findViewById(g2.getCheckedRadioButtonId()));
                answer_list[2] = g3.indexOfChild(g3.findViewById(g3.getCheckedRadioButtonId()));
                Log.v("testaaa","button clicked"+String.valueOf(answer_list[2]));

                if(answer_list[2] == 1 && answer_list[1] == 1) {
                    //get dynamo db, pull tips 1 2 3
                    mGetTipTask = new GetTipTask("aca");
                    mGetTipTask.execute(1,2,3);
                } else {
                    tip_list.add("Keep up the great work!");
                    Intent intent = new Intent(getContext(), TipsActivity.class);
                    Bundle b = new Bundle();
                    b.putStringArrayList("tips",tip_list);
                    b.putString("tit","Academics");
                    intent.putExtras(b);
                    //goto q
                    startActivity(intent);
                    tip_list.clear();
                }

                //invoke tip activity with answer list
            }
        });

        return v;
    }


    public class GetTipTask extends AsyncTask<Integer, Void, Boolean> {

        private final String mtable;
        GetTipTask(String mtable) {
            this.mtable = mtable;
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
                    acaMapper aca = mapper.load(acaMapper.class, i);
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
                b.putString("tit","Academics tips");
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

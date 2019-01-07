package com.ece.j.a1779cloudcomputing;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

public class TipsActivity extends AppCompatActivity {

    TextView title;
    ListView tiplist;
    ArrayList<String> tips = new ArrayList<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tips);
        Intent intent = getIntent();
        Bundle b = intent.getExtras();
        tips = b.getStringArrayList("tips");
        if (tips.isEmpty()) {
            tips.add("You are doing great!");
        }

        title = (TextView) findViewById(R.id.tiptitle);
        tiplist = (ListView) findViewById(R.id.tiplist);
        tiplist.setAdapter(new ArrayAdapter(this, R.layout.list_item, tips));
        title.setText(b.getString("tit"));
    }


    @Override
    protected void onStop() {
        super.onStop();
        tips.clear();
    }
}

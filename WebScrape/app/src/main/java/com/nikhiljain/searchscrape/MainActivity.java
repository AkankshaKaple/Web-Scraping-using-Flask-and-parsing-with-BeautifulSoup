package com.nikhiljain.searchscrape;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.localbroadcastmanager.content.LocalBroadcastManager;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.helper.HttpConnection;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.lang.ref.WeakReference;

import butterknife.BindView;

public class MainActivity extends AppCompatActivity {

    // https://angel.co/company/niyo-sol
    // https://www.crunchbase.com/organization/think-analytics-india
    // https://www.crunchbase.com/organization/loyalty
//    https://www.linkedin.com/company/hashtag-loyalty/
    // https://www.crunchbase.com/organization/niyo-solutions

    static final String SEARCH_URL = "https://www.crunchbase.com/organization/niyo-solutions";
//            + "#section-lists-featuring-this-company";
    private static final String TAG = "MainActivity";
    private Button btnShowData;
    private Button btnLinkedInActivity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findViews();
        setClickListeners();
    }

    private void setClickListeners() {
        btnShowData.setOnClickListener(this::onShowDataButtonClicked);
        btnLinkedInActivity.setOnClickListener(this::onLinkedInBtnClick);
    }

    private void findViews() {
        btnShowData = findViewById(R.id.btn_loadData);
        btnLinkedInActivity = findViewById(R.id.btn_nextActivity);
    }

    private void onShowDataButtonClicked(View view) {
        new NetworkOperationTask(this).execute();
    }

    private void onLinkedInBtnClick(View view) {
        Intent linkedInActivityIntent = new Intent(this, LinkedInActivity.class);
        startActivity(linkedInActivityIntent);
    }

    @Override
    protected void onResume() {
        registerBroadcastReceiver();
        super.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterBroadcastReceiver();
    }

    private void registerBroadcastReceiver() {
        LocalBroadcastManager.getInstance(this).registerReceiver(dataBroadcastReceiver,
                new IntentFilter(NetworkOperationTask.ACTION_DATA));
    }

    private BroadcastReceiver dataBroadcastReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (isResultIntentDataValid(intent)) {
                String result = intent.getStringExtra(NetworkOperationTask.INTENT_RESULT_KEY);
//                Log.e(TAG, "onReceive: " + result);
                TextView tvShowData = findViewById(R.id.tv_showData);
                tvShowData.setText(result);
            }
        }
    };

    // checks for intent result if valid or not
    private boolean isResultIntentDataValid(Intent intent) {
        return intent.hasExtra(NetworkOperationTask.INTENT_RESULT_KEY)
                && (intent.getStringExtra(NetworkOperationTask.INTENT_RESULT_KEY) != null);
    }

    private void unregisterBroadcastReceiver() {
        LocalBroadcastManager.getInstance(this).unregisterReceiver(dataBroadcastReceiver);
    }
}

class NetworkOperationTask extends AsyncTask<Void, Void, String> {
    private static final String TAG = "NetworkOperationTask";
    static final String ACTION_DATA = "com.nikhiljain.ACTION_DATA";
    static final String INTENT_RESULT_KEY = "result";
    private WeakReference<Context> mWeakContext;

    NetworkOperationTask(Context context) {
        mWeakContext = new WeakReference<>(context);
    }

    @Override
    protected String doInBackground(Void... voids) {
        String result1 = getDataFromUrl1();
        String result2 = getDataFromUrl2();
        String result3 = getDataFromUrl3();

        return result3;
    }

    private String getDataFromUrl3() {
        Connection.Response res = null;
        try {
            res = Jsoup.connect("http://linkedin.com/login?event=Next")
                    .execute();

            Document doc = Jsoup.connect("http://linkedin.com/login?event=Next")
                    .cookies(res.cookies())
                    .data("email", "my@email")
                    .data("password", "mypass")
                    .post();

            writeToFile(doc.outerHtml(), mWeakContext.get());
            Log.e(TAG, "getDataFromUrl3: " + doc.outerHtml());
        } catch (IOException e) {
            e.printStackTrace();
        }



        return "";
    }

    private String getDataFromUrl2() {
        String result = "";
        try {

            String url = "https://www.linkedin.com/uas/login?goback=&trk=hb_signin";
            Connection.Response response = Jsoup
                    .connect(url)
                    .method(Connection.Method.GET)
                    .execute();

            Document responseDocument = response.parse();



            Element loginCsrfParam = responseDocument
                    .select("input[name=loginCsrfParam]")
                    .first();

            response = Jsoup.connect("https://www.linkedin.com/uas/login-submit")
                    .cookies(response.cookies())
                    .data("loginCsrfParam", loginCsrfParam.attr("value"))
//                    .data("session_key", "@gmail.com")
//                    .data("session_password", "")
                    .method(Connection.Method.POST)

                    .followRedirects(true)
                    .execute();

            Document document = response.parse();
            result = document.outerHtml();
                        System.out.println(document);

            System.out.println("Welcome "
                    + document.select(".act-set-name-split-link").html());

        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    @Override
    protected void onPostExecute(String result) {
        super.onPostExecute(result);
        Intent dataIntent = new Intent(ACTION_DATA);
        dataIntent.putExtra(INTENT_RESULT_KEY, result);
        LocalBroadcastManager.getInstance(mWeakContext.get()).sendBroadcast(dataIntent);
        mWeakContext = null;
    }



    private String getDataFromUrl1() {
        String result = "";
        try {
//            Jsoup.


            final String USER_AGENT = "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; " +
                    "SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) " +
                    "Version/4.0 Mobile Safari/534.30";
//
//            final Document doc = Jsoup.connect("https://google.com/search?q=apple")
//                    .userAgent(USER_AGENT)
//                    .get();

//            Connection connection = new HttpConnection();
//            connection = connection.header("User-Agent", "Mozilla/5.0 (Macintosh;" +
//                    " Intel Mac OS X 10_9_3)");
//            connection = connection.url(MainActivity.SEARCH_URL);
//Jsoup.connect(MainActivity.SEARCH_URL)

            Document document = Jsoup.connect(MainActivity.SEARCH_URL)
//                    .userAgent(USER_AGENT)
//                    .referrer("http://www.google.com")
//                    .timeout(30000)
                    .get();

            result = document.outerHtml();


            Elements arrayOfFieldCard = document.getElementsByTag("image-with-fields-card");
            Elements arrayOfBigValues = document.getElementsByTag("big-values-card");
            Elements arrayOfNGInserted = document.getElementsByClass("ng-star-inserted");
            Elements arrayOfElements = document.getElementsByAttributeValue("contexttype", "profile");
//            Log.e(TAG, "doInBackground: res : " + res.get(0).text());

            for (Element element : arrayOfElements) {
                result += element.text() + "\n";
                Log.e(TAG, element.attributes() + " - " + element.text());
            }

//            Log.e(TAG,"The size of element array is " + document.outerHtml());
//            Log.e(TAG, "doInBackground: " + result);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }

    private void writeToFile(String data, Context context) {
        try {
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(context.openFileOutput(
                    "newfile.html", Context.MODE_PRIVATE));
            outputStreamWriter.write(data);
            outputStreamWriter.close();
        } catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }

}
package com.nikhiljain.searchscrape;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.Window;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

import static com.nikhiljain.searchscrape.Util.checkExternalMedia;
import static com.nikhiljain.searchscrape.Util.isReadStoragePermissionGranted;
import static com.nikhiljain.searchscrape.Util.isWriteStoragePermissionGranted;
import static com.nikhiljain.searchscrape.Util.writeToSDFile;

public class LinkedInActivity extends AppCompatActivity {
    /***
     * change below fields only to get the data from websites in your external directory
     * folder WebScrapeFiles
     * ***/

    private static final String SEARCH_URL = "https://www.crunchbase.com/organization/niyo-solutions";
    private static final String FILE_NAME = "crunchbase-niyo-sol";
    private static final String TAG = "Main";

    // Search urls ::

    // https://www.linkedin.com/company/hashtag-loyalty/about/
    // https://www.crunchbase.com/organization/niyo-solutions
    // https://www.linkedin.com/company/niyo-solutions-inc/
    // https://angel.co/company/niyo-sol
    // https://angel.co/company/niyo-sol/people
    // https://angel.co/company/niyo-sol/funding

    private WebView webview;
    private SwipeRefreshLayout refreshLayout;
    private ProgressDialog progressBar;
//    private static final String BASE_URL = "https://www.linkedin.com/company/hashtag-loyalty/";
//    private static final String URL_FOLDER = "about/";

    private String globalData;

    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);

        setContentView(R.layout.activity_linked_in);
        findViews();

        // asking permission at the time user open the app
        requestPermissionsFromUser();
        setupWebView();
        setClickListeners();
    }

    private void requestPermissionsFromUser() {
        isReadStoragePermissionGranted(this);
        isWriteStoragePermissionGranted(this);
    }

    private void findViews() {
        this.webview = findViewById(R.id.wv_loadLinkedIn);
        this.refreshLayout = findViewById(R.id.swipe_refresh_layout);
    }

    private void setClickListeners() {
        refreshLayout.setOnRefreshListener(() -> {
            if (refreshLayout.isRefreshing()) {
                webview.reload();
                refreshLayout.setRefreshing(false);
            }
        });
    }

    @SuppressLint({"JavascriptInterface", "SetJavaScriptEnabled"})
    private void setupWebView() {

        WebSettings settings = webview.getSettings();
        settings.setJavaScriptEnabled(true);
        webview.setScrollBarStyle(WebView.SCROLLBARS_OUTSIDE_OVERLAY);

        final AlertDialog alertDialog = new AlertDialog.Builder(this).create();

        progressBar = ProgressDialog.show(this, "WebView Example", "Loading...");
        webview.loadData("", "text/html", null);
        webview.addJavascriptInterface(new MyJavaScriptInterface(this), "HTMLOUT");
        webview.setWebViewClient(new WebViewClient() {

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {

                return super.shouldInterceptRequest(view, request);
            }

            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                Log.e(TAG, "Processing webview url click...");
                view.loadUrl(url);
                return true;
            }

            public void onPageFinished(WebView view, String url) {
                Log.i(TAG, "Finished loading URL: " + url);
                if (url.equalsIgnoreCase(SEARCH_URL)) {
                    webview.loadUrl("javascript:window.HTMLOUT.showHTML" +
                            "('<html>'+document.getElementsByTagName('html')[0].innerHTML+'</html>');");
                }

                if (progressBar.isShowing()) {
                    progressBar.dismiss();
                }
            }

            public void onReceivedError(WebView view, int errorCode, String description,
                                        String failingUrl) {
                Log.e(TAG, "Error: " + description);
                Toast.makeText(LinkedInActivity.this, "Oh no! " + description,
                        Toast.LENGTH_SHORT).show();
                alertDialog.setTitle("Error");
                alertDialog.setMessage(description);
                alertDialog.setButton("OK", (dialog, which) -> {
                    alertDialog.dismiss();
                });
                alertDialog.show();
            }
        });
        webview.loadUrl(SEARCH_URL);
    }

    class MyJavaScriptInterface {

        private Context ctx;

        MyJavaScriptInterface(Context ctx) {
            this.ctx = ctx;
        }

        @JavascriptInterface
        public void showHTML(String data) {

            globalData = data;
            Log.e(TAG, "showHTML:  method called:" + data);
            if (Util.isWriteStoragePermissionGranted(LinkedInActivity.this)
                    && Util.isReadStoragePermissionGranted(LinkedInActivity.this)) {
                checkExternalMedia();
                Util.writeToSDFile(data, FILE_NAME);
            }
        }
    }

    @Override
    public void onBackPressed() {
        if (webview.canGoBack()) {
            webview.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case Util.REQUEST_CODE_FILE_WRITE:
                Log.d(TAG, "External storage2");
                if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Log.e(TAG, "onRequestPermissionsResult: write permission granted ");
//                    Log.v(TAG, "Permission: " + permissions[0] + " was " + grantResults[0]);
                    //resume tasks needing the write permission
                    writeToSDFile(globalData, FILE_NAME);

                } else {
                    Log.e(TAG, "onRequestPermissionsResult: permission denied");
                }
                break;

            case Util.REQUEST_CODE_FILE_READ:
                Log.d(TAG, "External storage1");
                if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Log.e(TAG, "onRequestPermissionsResult: read permission granted ");
//                    Log.v(TAG, "Permission: " + permissions[0] + " was " + grantResults[0]);
                    //resume tasks needing the read permission

                } else {
                    Log.e(TAG, "onRequestPermissionsResult: permission denied for read");
                }
                break;
        }
    }
}


/*

 private void setWebView() {
        webViewLinkedIn.setWebViewClient(new WebViewClient());
        webViewLinkedIn.loadUrl("https://www.linkedin.com/uas/login?goback=&trk=hb_signin");
    }

    private void findViews() {
        webViewLinkedIn = findViewById(R.id.wv_loadLinkedIn);
    }


    class MyJavaScriptInterface {

    private Context ctx;

    MyJavaScriptInterface(Context ctx) {
        this.ctx = ctx;
    }

    public void showHTML(String html) {
        Log.e(TAG, "showHTML: method called");
        new AlertDialog.Builder(ctx).setTitle("HTML").setMessage(html)
                .setPositiveButton(android.R.string.ok, null).setCancelable(false).create().show();
    }
 */
//
//    private AsyncTask myTask = new AsyncTask() {
//        @Override
//        protected Object doInBackground(Object[] objects) {
//            getDownloadBtnOnly();
//            return null;
//        }
//    };


//    private void getDownloadBtnOnly() {
//        try {
//            URL url = new URL("https://www.google.com");
//            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
//            urlConnection.setRequestMethod("GET");
//
//            BufferedReader br = new BufferedReader(new InputStreamReader(urlConnection
//                    .getInputStream()));
//            String line;
//            StringBuffer sb = new StringBuffer();
//
//            // read contents line by line and store in the string
//            while ((line =
//                    br.readLine()) != null) {
//                sb.append(line);
//            }
//            br.close();
//            Log.e(TAG, "getDownloadBtnOnly: " + "\n" + sb.toString());
//
//        } catch (MalformedURLException e) {
//            e.printStackTrace();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//
//    }



/*
private String getDownloadButtonOnly(String url){
        HttpGet pageGet = new HttpGet(url);


        ResponseHandler<String> handler = new ResponseHandler<String>() {
            public String handleResponse(HttpResponse response) throws ClientProtocolException, IOException {
                HttpEntity entity = response.getEntity();
                String html;

                if (entity != null) {
                    html = EntityUtils.toString(entity);
                    return html;
                } else {
                    return null;
                }
            }
        };

        pageHTML = null;
        try {
            while (pageHTML==null){
                pageHTML = client.execute(pageGet, handler);
            }
        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        Pattern pattern = Pattern.compile("<h2>Direct Down.+?</h2>(</div>)*(.+?)<.+?>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(pageHTML);
        String displayHTML = null;
        while(matcher.find()){
            displayHTML = matcher.group();
        }

        return displayHTML;
    }

    @Override
    public void customizeWebView(final ServiceCommunicableActivity activity, final WebView webview, final SearchResult mRom) {
        mRom.setFileSize(getFileSize(mRom.getURLSuffix()));
        webview.getSettings().setJavaScriptEnabled(true);
        WebViewClient anchorWebViewClient = new WebViewClient() {

            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                String downloadButtonHTML = getDownloadButtonOnly(url);
                if (downloadButtonHTML != null && !url.equals(lastLoadedURL)) {
                    lastLoadedURL = url;
                    webview.loadDataWithBaseURL(url, downloadButtonHTML, null, "utf-8", url);
                }
            }
        }
    }
 */


//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.activity_linked_in);
//        findViews();
//        setWebView();
//
//    }


//                if (url.compareToIgnoreCase(SEARCH_URL) == 0) {
//                    new NetAsyncTask().execute(url);
//                }
////                webview.loadUrl("javascript:window.HtmlViewer.showHTML" +
//                        "('<html>'+document.getElementsByTagName('html')[0].innerHTML+'</html>');");

//new AlertDialog.Builder(ctx).setTitle("HTML").setMessage(html)
//      .setPositiveButton(android.R.string.ok, null).setCancelable(false).create().show();


//private class NetAsyncTask extends AsyncTask<String, Void, Void> {
//
//    @Override
//    protected Void doInBackground(String... strings) {
//        getData(strings[0]);
//        return null;
//    }
//}

//            Log.e(TAG, "getData: " + "\n" + sb.toString());
//            writeToFile(sb.toString(), LinkedInActivity.this);

//                .data("session_key", "@gmail.com")
//                    .data("session_password", "")

//            Log.e(TAG, "shouldInterceptRequest: " + request.getUrl().toString() );


// javascript:window.HTMLOUT.showHTML" +
//                            "('<html>'+document.getElementsByTagName('html')[0].innerHTML+'</html>');


//    private void getData(String urlPath) {
//        StringBuilder sb = new StringBuilder();
//        String line;
//        try {
//            URL url = new URL(urlPath);
//
//            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
//            urlConnection.setRequestMethod("GET");
//            InputStream inputStream = urlConnection.getInputStream();
//
//            BufferedReader br = new BufferedReader(new InputStreamReader(inputStream));
//
//
//            // read contents line by line and store in the string
//            while ((line =
//                    br.readLine()) != null) {
//                sb.append(line);
//            }
//            br.close();
//
//        } catch (MalformedURLException e) {
//            e.printStackTrace();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//    }

//                Log.e(TAG, "shouldInterceptRequest: " + request.getUrl().toString());

//            writeToFile(data, "angelco-niyo-solutions-people" ,ctx);
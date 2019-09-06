package com.nikhiljain.searchscrape;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Environment;
import android.util.Log;

import androidx.core.app.ActivityCompat;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

public class Util {

    public static final int REQUEST_CODE_FILE_READ = 1;
    public static final int REQUEST_CODE_FILE_WRITE = 2;
    private static final String TAG = "Util";

    public static void writeToFile(String data, String fileName, Context context) {
        try {
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(context.openFileOutput(
                    fileName + ".html", Context.MODE_PRIVATE));
            outputStreamWriter.write(data);
            outputStreamWriter.close();
        } catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }

    /**
     * Method to check whether external media available and writable. This is adapted from
     * http://developer.android.com/guide/topics/data/data-storage.html#filesExternal
     */

    public static void checkExternalMedia() {
        boolean mExternalStorageAvailable;
        boolean mExternalStorageWritable;
        String state = Environment.getExternalStorageState();

        if (Environment.MEDIA_MOUNTED.equals(state)) {
            // Can read and write the media
            mExternalStorageAvailable = mExternalStorageWritable = true;
        } else if (Environment.MEDIA_MOUNTED_READ_ONLY.equals(state)) {
            // Can only read the media
            mExternalStorageAvailable = true;
            mExternalStorageWritable = false;
        } else {
            // Can't read or write
            mExternalStorageAvailable = mExternalStorageWritable = false;
        }
        Log.e(TAG, "checkExternalMedia: " + "External Media: readable = "
                + mExternalStorageAvailable + " & writable = " + mExternalStorageWritable);
//        tv.append("\n\nExternal Media: readable="
//                +mExternalStorageAvailable+" writable="+mExternalStorageWritable);
    }

    /**
     * Method to write ascii text characters to file on SD card. Note that you must add a
     * WRITE_EXTERNAL_STORAGE permission to the manifest file or this method will throw
     * a FileNotFound Exception because you won't have write permission.
     */

    public static void writeToSDFile(String data, String fileName) {

        // Find the root of the external storage.
        // See http://developer.android.com/guide/topics/data/data-  storage.html#filesExternal

        File root = android.os.Environment.getExternalStorageDirectory();
//        tv.append("\nExternal file system root: "+root);

        // See http://stackoverflow.com/questions/3551821/android-write-to-sd-card-folder

        File dir = new File(root.getAbsolutePath() + "/WebScrapeFiles");

        if (!dir.exists()) {
            boolean isDirectoryCreated = dir.mkdirs();
            Log.e(TAG, "writeToSDFile: Directory doesn't exist.. creating new");
            Log.e(TAG, "writeToSDFile: directory is created " + dir.getAbsolutePath() + " : " + isDirectoryCreated);
        }
        File file = new File(dir, fileName + ".html");

        try {
            FileOutputStream f = new FileOutputStream(file);
            PrintWriter pw = new PrintWriter(f);
            pw.println(data);
            pw.flush();
            pw.close();
            f.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            Log.i(TAG, "******* File not found. Did you" +
                    " add a WRITE_EXTERNAL_STORAGE permission to the   manifest?");
        } catch (IOException e) {
            e.printStackTrace();
        }
        Log.e(TAG, "writeToSDFile: File written");
//        tv.append("\n\nFile written to "+file);
    }

    // checks read permission
    public static boolean isReadStoragePermissionGranted(Context mContext) {
        if (Build.VERSION.SDK_INT >= 23) {
            if (mContext.checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE)
                    == PackageManager.PERMISSION_GRANTED) {
                Log.v(TAG, "Permission is granted1");
                return true;
            } else {

                Log.v(TAG, "Permission is revoked1");
                ActivityCompat.requestPermissions((Activity) mContext,
                        new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, REQUEST_CODE_FILE_READ);
                return false;
            }
        } else { //permission is automatically granted on sdk<23 upon installation
            Log.v(TAG, "Permission is granted1");
            return true;
        }
    }

    // checks write permission
    public static boolean isWriteStoragePermissionGranted(Context mContext) {
        if (Build.VERSION.SDK_INT >= 23) {
            if (mContext.checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    == PackageManager.PERMISSION_GRANTED) {
                Log.v(TAG, "Permission is granted2");
                return true;
            } else {

                Log.v(TAG, "Permission is revoked2");
                ActivityCompat.requestPermissions((Activity) mContext, new String[]
                                {Manifest.permission.WRITE_EXTERNAL_STORAGE},
                        REQUEST_CODE_FILE_WRITE);
                return false;
            }
        } else { //permission is automatically granted on sdk<23 upon installation
            Log.v(TAG, "Permission is granted2");
            return true;
        }
    }
}

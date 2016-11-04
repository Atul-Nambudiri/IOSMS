package com.atulnambudiri.iosms;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.provider.MediaStore;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.CursorLoader;
import android.support.v7.app.AppCompatActivity;
import android.telephony.SmsManager;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * A placeholder fragment containing a simple view.
 */
public class MainActivityFragment extends Fragment {
    final int SELECT_IMAGE = 12;
    TextView textToDisplay;
    static String phoneNumber = "6304513493";
    static String numberBufferStart = "$$-";
    static String numberBufferEnd = "-$$";
    static int numberBufferLength = 10;
    static int smsLength = 160;
    private boolean canSendMessages;

    public MainActivityFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_main, container, false);
        textToDisplay = (TextView) rootView.findViewById(R.id.image_text);
        canSendMessages = ContextCompat.checkSelfPermission(getActivity(), Manifest.permission.SEND_SMS) == PackageManager.PERMISSION_GRANTED;
        if(!canSendMessages) {
            ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.SEND_SMS}, 1);
        }
        return rootView;
    }

    public void openGallery(View v) {
        Intent imageChoose = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        startActivityForResult(imageChoose, SELECT_IMAGE);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == SELECT_IMAGE) {
            if (resultCode == Activity.RESULT_OK) {
                Uri chosenImage = data.getData();
                String imageName = getFileNameFromURI(getActivity(), chosenImage);
                Bitmap chosenBitmap;
                try {
                    chosenBitmap = MediaStore.Images.Media.getBitmap(getActivity().getContentResolver(), chosenImage);
                } catch (IOException e) {
                    e.printStackTrace();
                    return;
                }
                String imageText = bitmapToString(chosenBitmap);
                //imageText = encodeTest("This is a test string. Lets see what happens.");
                Log.d("ImageText", imageText);
                if(imageText.length() > 18000) {
                    textToDisplay.setText("Image " + imageName + " is too large to send as text. Image length is: " + Integer.toString(imageText.length()));
                }
                else {
                    textToDisplay.setText("Sending Image " + imageName + ". Image length is: " + Integer.toString(imageText.length()));
                    new SendSMSTask().execute(imageText, imageName);
                }
            }
        }
    }

    public String getFileNameFromURI(Context context, Uri uri) {
        String[] proj = { MediaStore.Images.Media.DATA };
        CursorLoader loader = new CursorLoader(context, uri, proj, null, null, null);
        Cursor cursor = loader.loadInBackground();
        int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
        cursor.moveToFirst();
        String result = cursor.getString(column_index);
        cursor.close();

        Pattern pattern = Pattern.compile(".*\\/(.*)");
        Matcher matcher = pattern.matcher(result);
        if(matcher.find()) {
            return matcher.group(1);
        }
        return result;
    }

    public String encodeTest(String str) {
        String encoded = Base64.encodeToString(str .getBytes(), Base64.DEFAULT);
        return encoded;
    }

    public String bitmapToString(Bitmap bm) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bm.compress(Bitmap.CompressFormat.JPEG, 25, baos);
        byte[] b = baos.toByteArray();
        String imageText = Base64.encodeToString(b, Base64.DEFAULT);
        return imageText;
    }

    private class SendSMSTask extends AsyncTask<String, Void, String> {

        @Override
        protected String doInBackground(String... params) {
            String imageText = params[0];
            String imageName = params[1];
            String sentMessages = sendImage(imageText, imageName);
            return sentMessages;
        }

        protected void onPostExecute(String result) {
            textToDisplay.setText("Image has been sent. " + result + " messages were sent");
        }

        public String sendImage(String imageText, String imageName) {
            int sentCounter = 0;
            sendText("Start Image. Image Name: " + imageName);
            try {
                Thread.sleep(1000); //Sleep for a bit so that the initial message has some time to be sent
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            for(int i = 0; i < imageText.length(); i += smsLength - numberBufferLength) {
                int end = i + smsLength - numberBufferLength > imageText.length() ? imageText.length() : i + smsLength - numberBufferLength;
                String number = String.format("%04d", sentCounter);
                String beginning = numberBufferStart + number + numberBufferEnd;
                String imagePortion = beginning + imageText.substring(i, end);
                sendText(imagePortion);
                Log.d("Text Sending", "Sent Part of the image");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                sentCounter ++;
            }
            sendText(Integer.toString(sentCounter) + " texts were sent");
            sentCounter += 2;
            Log.d("Sent Counter", "Sent Counter: " + Integer.toString(sentCounter));
            return Integer.toString(sentCounter);
        }

        public void sendText(String message) {
            Log.d("Can Send Messages", Boolean.toString(canSendMessages));
            if(canSendMessages) {
                SmsManager smsManager = SmsManager.getDefault();
                smsManager.sendTextMessage(phoneNumber, null, message, null, null);
            }
        }
    }

    public void onRequestPermissionResult(int requstCode, String[] permissions, int[] grantResults) {
        switch (requstCode) {
            case PackageManager.PERMISSION_GRANTED: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    canSendMessages = true;
                }
            }
        }
    }


}

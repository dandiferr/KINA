package com.example.richard.kina;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.getpebble.android.kit.PebbleKit;
import com.getpebble.android.kit.util.PebbleDictionary;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Set;
import java.util.UUID;


public class MainActivity extends Activity {

    private static final UUID PEBBLE_APP_UUID = UUID.fromString("0e7b49ba-28af-4021-9a0f-f8db083ee11a");

    TextView mPebbleText;
    BluetoothAdapter mBluetoothAdapter;
    BluetoothDevice mDevice;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        Button edisonButton = (Button) findViewById(R.id.buttonEdison);
        Button sendButton = (Button) findViewById(R.id.buttonSend);

        edisonButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                initEdison();
            }
        });

        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                EditText textData = (EditText) findViewById(R.id.textData);
                passData(textData.getText().toString());
            }
        });

        mPebbleText = (TextView) findViewById(R.id.textPebble);

        if(!PebbleKit.isWatchConnected(getApplicationContext())) {
            PebbleKit.startAppOnPebble(getApplicationContext(), PEBBLE_APP_UUID);
        }

        PebbleKit.registerPebbleConnectedReceiver(getApplicationContext(), new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                mPebbleText.setText("Pebble Connected");
                PebbleKit.startAppOnPebble(getApplicationContext(), PEBBLE_APP_UUID);
            }
        });

        PebbleKit.registerPebbleDisconnectedReceiver(getApplicationContext(), new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                mPebbleText.setText("Pebble Disconnected");
            }
        });
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void initEdison() {
        if (!mBluetoothAdapter.isEnabled()) {
            Intent enableBluetooth = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBluetooth, 0);
        }

        Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
        if (pairedDevices.size() > 0) {
            for (BluetoothDevice device : pairedDevices) {
                if (device.getName().equals("BlueZ 5.18")) {
                    mDevice = device;
                    break;
                }
            }
        }

        if (mDevice != null) {
            UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805f9b34fb");
            try {
                BluetoothSocket socket = mDevice.createRfcommSocketToServiceRecord(uuid);
                InputStream inputStream = socket.getInputStream();
                Toast.makeText(getApplicationContext(), "Bluetooth connection to Edison success", Toast.LENGTH_SHORT).show();
            } catch (IOException e) {
                Toast.makeText(getApplicationContext(), "Bluetooth not available", Toast.LENGTH_SHORT).show();
            }
        }
        else {
            Toast.makeText(getApplicationContext(), "Bluetooth connection to Edison failed.", Toast.LENGTH_SHORT).show();
        }

    }

    private void passData(String text) {
        if(!PebbleKit.isWatchConnected(getApplicationContext()))
        {
            Toast.makeText(getApplicationContext(), "Pebble is not connected. Please check connection.", Toast.LENGTH_SHORT).show();
        }
        else {

            PebbleDictionary dict = new PebbleDictionary();
            PebbleKit.startAppOnPebble(getApplicationContext(), PEBBLE_APP_UUID);
            dict.addString(0, text);
            PebbleKit.sendDataToPebble(getApplicationContext(), PEBBLE_APP_UUID, dict);

        }



    }
}

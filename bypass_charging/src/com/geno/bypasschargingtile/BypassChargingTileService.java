package com.geno.bypasschargingtile;

import android.graphics.drawable.Icon;
import android.service.quicksettings.Tile;
import android.service.quicksettings.TileService;
import android.util.Log;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class BypassChargingTileService extends TileService {

    private static final String TAG = "BypassChargingTile";
    private static final String CHARGING_CONTROL_PATH =
            "/sys/class/oplus_chg/battery/mmi_charging_enable";

    private static final String CHARGING_ENABLED = "1";
    private static final String CHARGING_DISABLED = "0";

    @Override
    public void onStartListening() {
        super.onStartListening();
        updateTile();
    }

    @Override
    public void onClick() {
        super.onClick();
        toggleBypassCharging();
        updateTile();
    }

    private boolean isChargingEnabled() {
        try (BufferedReader br = new BufferedReader(new FileReader(CHARGING_CONTROL_PATH))) {
            String value = br.readLine();
            if (value != null) {
                return value.trim().equals(CHARGING_ENABLED);
            }
        } catch (IOException e) {
            Log.e(TAG, "Failed to read charging control node", e);
        }
        return true;
    }

    private void toggleBypassCharging() {
        boolean chargingCurrentlyEnabled = isChargingEnabled();
        String newValue = chargingCurrentlyEnabled ? CHARGING_DISABLED : CHARGING_ENABLED;
        try (FileWriter fw = new FileWriter(CHARGING_CONTROL_PATH)) {
            fw.write(newValue);
            fw.flush();
        } catch (IOException e) {
            Log.e(TAG, "Failed to write charging control node", e);
        }
    }

    private void updateTile() {
        Tile tile = getQsTile();
        if (tile == null) return;

        boolean chargingEnabled = isChargingEnabled();
        boolean bypassActive = !chargingEnabled;

        tile.setIcon(Icon.createWithResource(this, R.drawable.ic_bypass_charging));

        if (bypassActive) {
            tile.setState(Tile.STATE_ACTIVE);
            tile.setLabel(getString(R.string.bypass_charging_tile_label));
            tile.setSubtitle(getString(R.string.bypass_charging_tile_subtitle_on));
        } else {
            tile.setState(Tile.STATE_INACTIVE);
            tile.setLabel(getString(R.string.bypass_charging_tile_label));
            tile.setSubtitle(getString(R.string.bypass_charging_tile_subtitle_off));
        }

        tile.updateTile();
    }
}

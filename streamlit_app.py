{
  "IP_ASSET": "3D_Vocal_Visual_Control_Matrix",
  "VERSION": {
    "V1_0": {<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#0A0A0A"
    android:fillViewport="true">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="20dp"
        android:gravity="center_horizontal">

        <TextView
            android:text="S.S.S Music"
            android:textColor="#FF0000"
            android:textSize="35sp"
            android:textStyle="bold" />
            
        <TextView
            android:text="&quot;อยู่นิ้งๆ ไม่เจ็บตัว&quot;"
            android:textColor="#FFD700"
            android:textSize="16sp"
            android:layout_marginBottom="20dp" />

        <ImageView
            android:id="@+id/albumCover"
            android:layout_width="220dp"
            android:layout_height="220dp"
            android:src="@drawable/logo_world" 
            android:scaleType="centerCrop"/>
            
        <EditText
            android:id="@+id/shortNote"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="ใจความสั้นๆ ที่จะให้ AI ขยี้..."
            android:textColor="#FFFFFF"
            android:layout_marginTop="20dp" />

        <Button
            android:id="@+id/btnGenerate"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:text="ขยี้ใจความ (GENERATE)"
            android:backgroundTint="#FF0000"
            android:layout_marginTop="20dp"/>

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center"
            android:layout_marginTop="15dp">
            <Button android:id="@+id/btnSave" android:text="SAVE" android:layout_margin="5dp" android:backgroundTint="#00FF00"/>
            <Button android:id="@+id/btnShare" android:text="SHARE" android:layout_margin="5dp" android:backgroundTint="#00f2fe"/>
            <Button android:id="@+id/btnTurbo" android:text="TURBO" android:layout_margin="5dp" android:backgroundTint="#FFD700" android:textColor="#000"/>
        </LinearLayout>

        <TextView
            android:id="@+id/resultLyrics"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:textColor="#E0E0E0"
            android:layout_marginTop="20dp"
            android:padding="10dp"/>
    </LinearLayout>
</ScrollView>

      "NAME": "Vocal_Blueprint_40K_USD",
      "CORE_LOGIC": "Valence/Arousal to F0_Vibrato Mapping",
      "MAPPING_EXAMPLES": {
        "JOY_EXCITEMENT": {
          "F0_Scalar": 0.8,
          "Vibrato_Rate": 0.9
        },
        "SADNESS_BOREDOM": {
          "F0_Scalar": 0.3,
          "Vibrato_Rate": 0.2
        }
      }
    },
    "V2_0": {
      "NAME": "Visual_Blueprint_100M_THB_Potential",
      "CORE_LOGIC": "Valence/Arousal to 6_Visual_Parameters",
      "MAPPING_EXAMPLES": {
        "JOY_EXCITEMENT": {
          "SATURATION": 0.6,
          "KEY_LIGHTING": 0.8,
          "CONTRAST": 0.7,
          "DEPTH_OF_FIELD": 0.3,
          "TEXTURE_DETAIL": 0.7,
          "COMPOSITION_FOCUS": 0.9
        },
        "SADNESS_BOREDOM": {
          "SATURATION": 0.2,
          "KEY_LIGHTING": 0.3,
          "CONTRAST": 0.4,
          "DEPTH_OF_FIELD": 0.8,
          "TEXTURE_DETAIL": 0.8,
          "COMPOSITION_FOCUS": 0.3
        }
      }
    }
  }
}


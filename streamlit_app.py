<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#050505"
    android:padding="15dp">

    <LinearLayout
        android:id="@+id/matrixDisplay"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:background="#1A0000"
        android:padding="10dp"
        android:layout_alignParentTop="true"
        android:elevation="5dp">
        
        <TextView
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="V1: VOCAL ACTIVE"
            android:textColor="#FFD700"
            android:textSize="10sp"
            android:textStyle="bold" />
            
        <TextView
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="V2: VISUAL 6D ON"
            android:textColor="#00F2FE"
            android:textSize="10sp"
            android:textStyle="bold"
            android:gravity="end" />
    </LinearLayout>

    <FrameLayout
        android:id="@+id/coverContainer"
        android:layout_width="280dp"
        android:layout_height="280dp"
        android:layout_centerHorizontal="true"
        android:layout_below="@id/matrixDisplay"
        android:layout_marginTop="30dp">

        <ImageView
            android:id="@+id/mainLogo"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:src="@drawable/logo_world"
            android:scaleType="centerCrop"
            android:alpha="0.8" />
            
        <View
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:background="@drawable/neon_ring_red" />
    </FrameLayout>

    <TextView
        android:id="@+id/songTitle"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_below="@id/coverContainer"
        android:layout_centerHorizontal="true"
        android:layout_marginTop="20dp"
        android:text="SYNAPSE PRO: ENERGY 6D"
        android:textColor="#FFFFFF"
        android:textSize="22sp"
        android:textStyle="bold" />

    <LinearLayout
        android:id="@+id/controls"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_below="@id/songTitle"
        android:gravity="center"
        android:layout_marginTop="30dp">

        <ImageButton
            android:layout_width="50dp"
            android:layout_height="50dp"
            android:src="@android:drawable/ic_media_previous"
            android:background="?attr/selectableItemBackgroundBorderless"
            android:tint="#FF0000" />

        <Button
            android:id="@+id/btnPlay"
            android:layout_width="80dp"
            android:layout_height="80dp"
            android:text="▶"
            android:textSize="30sp"
            android:textColor="#000"
            android:backgroundTint="#FFD700"
            android:layout_marginHorizontal="20dp"
            android:elevation="10dp" />

        <ImageButton
            android:layout_width="50dp"
            android:layout_height="50dp"
            android:src="@android:drawable/ic_media_next"
            android:background="?attr/selectableItemBackgroundBorderless"
            android:tint="#FF0000" />
    </LinearLayout>

    <Button
        android:id="@+id/btnTurbo"
        android:layout_width="match_parent"
        android:layout_height="65dp"
        android:layout_alignParentBottom="true"
        android:layout_marginBottom="10dp"
        android:text="ACTIVATE TURBO MATRIX"
        android:backgroundTint="#FF0000"
        android:textColor="#FFF"
        android:textStyle="bold"
        android:textSize="18sp"
        android:elevation="15dp" />

</RelativeLayout>

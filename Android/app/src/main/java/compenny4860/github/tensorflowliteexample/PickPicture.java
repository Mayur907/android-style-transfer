package compenny4860.github.tensorflowliteexample;

import android.content.Intent;

public class PickPicture {


    /////////////////////////////////////////////////////////////////////////////////////////////////
    public static final int PICK_IMAGE = 100;
    public Intent getPickIntent() {
        Intent gallery =
                new Intent(Intent.ACTION_PICK,
                        android.provider.MediaStore.Images.Media.INTERNAL_CONTENT_URI);
        return gallery;
    }
    /////////////////////////////////////////////////////////////////////////////////////////////////


}

import os
import sys
import pydicom
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# ==== CONFIG: Path to a test DICOM ====
SAMPLE_DICOM_PATH = "sample_data/synthetic_xray.dcm"   # <-- Change this to your real sample!

def test_load_dicom(path):
    print(f"=== Loading DICOM: {path}")
    if not os.path.exists(path):
        print(f"  ✗ File not found: {path}")
        return False
    try:
        ds = pydicom.dcmread(path)
        arr = ds.pixel_array
        print(f"  ✓ DICOM loaded. Shape: {arr.shape}, dtype: {arr.dtype}")
        # Show metadata sample
        print(f"  • Patient ID: {getattr(ds, 'PatientID', 'N/A')}")
        return arr, ds
    except Exception as e:
        print(f"  ✗ Error loading DICOM: {e}")
        return False

def test_plot(arr):
    print("=== Plotting image with matplotlib ===")
    try:
        plt.imshow(arr, cmap="gray")
        plt.title("Test X-ray")
        plt.axis('off')
        plt.show()
        print("  ✓ Image displayed with matplotlib.")
        return True
    except Exception as e:
        print(f"  ✗ Plotting failed: {e}")
        return False

def test_convert_to_png(arr, out_path="test_export.png"):
    print(f"=== Converting image to PNG: {out_path}")
    try:
        # Rescale if not uint8
        arr_norm = (arr - arr.min()) / (arr.max() - arr.min()) * 255
        arr_uint8 = arr_norm.astype(np.uint8)
        img = Image.fromarray(arr_uint8)
        img.save(out_path)
        print(f"  ✓ PNG saved to {out_path}")
        return True
    except Exception as e:
        print(f"  ✗ PNG conversion failed: {e}")
        return False

def main():
    print("\n\n====== Synthetic Ascension Medical Imaging MVP Test ======\n")
    # Step 1: DICOM test
    result = test_load_dicom(SAMPLE_DICOM_PATH)
    if not result:
        print("  ✗ Imaging test failed (DICOM load failed or file missing).")
        sys.exit(1)
    arr, ds = result

    # Step 2: Matplotlib plot test
    test_plot(arr)

    # Step 3: Convert to PNG
    test_convert_to_png(arr)

    print("\n✅ Medical imaging MVP test complete.\n")

if __name__ == "__main__":
    main()

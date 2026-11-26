import os
import shutil

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_img = os.path.join(script_dir, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    dst_img = os.path.join(output_dir, "entry.png")
    if not os.path.exists(src_img):
        raise FileNotFoundError(f"Source image {src_img} not found. Run draw.py first.")
    with open(src_img, "rb") as f_src, open(dst_img, "wb") as f_dst:
        f_dst.write(f_src.read())
    print(f"Successfully copied {src_img} to {dst_img}")

if __name__ == "__main__":
    main()

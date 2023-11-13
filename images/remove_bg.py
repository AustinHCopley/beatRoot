import cv2
import numpy as np

def remove_bg(in_path, out_path):
    img = cv2.imread(in_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # select region of interest over background to get average bg color in roi
    cv2.imshow("Select Background Area", img_rgb)
    rect_roi = cv2.selectROI("Select Background Area", img_rgb, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()
    bg_roi = img_rgb[int(rect_roi[1]):int(rect_roi[1] + rect_roi[3]),
                             int(rect_roi[0]):int(rect_roi[0] + rect_roi[2])]
    avg_color = np.mean(bg_roi, axis=(0, 1), keepdims=True)

    # set a range of colors to remove +/- 10 from average
    r = 10
    lower_bound = avg_color - np.array([r, r, r])
    upper_bound = avg_color + np.array([r, r, r])

    mask = cv2.inRange(img_rgb, lower_bound, upper_bound)

    img_copy = img.copy()
    img_copy[mask != 0] = [0, 0, 0, 0]

    cv2.imwrite(out_path, img_copy)

if __name__ == "__main__":
    logo = "beatroot.png"
    logo_out = "beatrootfg.png"
    play = "play.png"
    play_out = "playfg.png"
    skip = "skip.png"
    skip_out = "skipfg.png"
    rewind = "rewind.png"
    rewind_out = "rewindfg.png"

    remove_bg(logo, logo_out)
    remove_bg(play, play_out)
    remove_bg(skip, skip_out)
    remove_bg(rewind, rewind_out)
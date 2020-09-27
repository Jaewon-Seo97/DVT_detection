import cv2
import numpy as np


def showImage(img, title='image', t=0, esc=False):
    cv2.imshow(title, img)
    if esc:
        while cv2.waitKey(0) != 27:
            if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE)<=0:
                break
    else:
        cv2.waitKey(t)
    cv2.destroyWindow(title)


def class_colors(num_colors):
    class_colors = []
    for i in range(0, num_colors):
        hue = 255 * i / num_colors
        col = np.zeros((1, 1, 3)).astype("uint8")
        col[0][0][0] = hue
        col[0][0][1] = 128  # Saturation
        col[0][0][2] = 255  # Value
        cvcol = cv2.cvtColor(col, cv2.COLOR_HSV2BGR)
        col = (int(cvcol[0][0][0]), int(cvcol[0][0][1]), int(cvcol[0][0][2]))
        class_colors.append(col)

    return class_colors


def roi2rect(img_name, img_np, img_data, label_list):
    colors = class_colors(len(label_list))
    for rect in img_data:
        bounding_box = [rect[0], rect[1], rect[2], rect[3]]
        xmin = int(bounding_box[0])
        ymin = int(bounding_box[1])
        xmax = int(bounding_box[2])
        ymax = int(bounding_box[3])
        pmin = (xmin, ymin)
        pmax = (xmax, ymax)

        label_array = rect[4:]
        index = int(np.where(label_array == np.float(1))[0])
        label = label_list[index]

        # color = tuple(map(int, np.uint8(np.random.uniform(0, 255, 3))))
        color = colors[index]
        cv2.rectangle(img_np, pmin, pmax, color, 2)

        text_top = (xmin, ymin - 10)
        text_bot = (xmin + 80, ymin + 5)
        text_pos = (xmin + 5, ymin)
        cv2.rectangle(img_np, text_top, text_bot, colors[index], -1)
        cv2.putText(img_np, label, text_pos, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_PLAIN, 1, 1, 2)

    # cv2.imshow(img_name, img_np)
    # cv2.waitKey()
    # # return img_name, img_np
    # while cv2.waitKey(100) != 27:
    #     if cv2.getWindowProperty(img_name, cv2.WND_PROP_VISIBLE) <= 0:
    #         break
    # cv2.destroyWindow(img_name)

    showImage(img=img_np, title=img_name)
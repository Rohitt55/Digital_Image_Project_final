import cv2


def bounded(image, maximum=512):
    # Keep the aspect ratio when reducing a large image.
    h, w = image.shape[:2]
    if max(h, w) <= maximum:
        return image.copy()

    scale = maximum / max(h, w)
    new_width = max(1, round(w * scale))
    new_height = max(1, round(h * scale))
    small = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return small

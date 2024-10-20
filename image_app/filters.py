from PIL import Image, ImageOps, ImageFilter

def apply_gray_filter(image):
    return image.convert('L')

def apply_sepia_filter(image):
    sepia_image = ImageOps.colorize(image.convert("L"), "#704214", "#C0A080")
    return sepia_image

def apply_blur_filter(image):
    return image.filter(ImageFilter.BLUR)

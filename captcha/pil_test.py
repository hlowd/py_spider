# coding:utf-8

from PIL import Image

im=Image.open("d:\\my\\py_spider\\1.jpg")
fmt=im.format
sz=im.size
mod=im.mode
inf=im.info

def show_attr():
    print(fmt,sz,mod,inf)

def cut_img():
    """裁剪图像"""
    im.crop((0,0,120,120)).show()

def split_bands():
    """分割通道"""
    r,g,b = im.split()
    r.show()
    g.show()
    b.show()
    im3=Image.merge("RGB", (b, g, r))
    im3.show()

def bin():
    """图像二值化,第二行为二值化函数"""
    im2=im.convert('L')
    mask=im2.point( lambda i:i < 127 and 255)
    mask.show()

def use_mask():
    """白的部分，用mask覆盖，黑的保留原样"""
    im2 = im.convert('L')
    mask = im2.point(lambda i: i < 127 and 255)
    im.paste(mask,(0,0,sz[0],sz[1]),mask=mask)
    im.show()

def change():
    # im.resize((128,128)).show()
    # im.rotate(45).show() #逆时针45度，背景黑
    # im.transpose(Image.FLIP_LEFT_RIGHT).show() # 左右翻转
    # im.transpose(Image.FLIP_TOP_BOTTOM).show() # 上下翻转
    # im.transpose(Image.ROTATE_90).show() # 逆时针90度
    # im.transpose(Image.ROTATE_180).show()
    im.transpose(Image.ROTATE_270).show()


if __name__ == "__main__":
    split_bands()


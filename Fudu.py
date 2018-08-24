from PIL import Image
import os
import imageio
import easygui
import sys

path = ''
path = easygui.fileopenbox(msg = "选择要复读的图片", filetypes = ["*.gif", "*.jpg", "*.png"])
if path == '':
    sys.exit()

#判断输入文件类型
shot, ext = os.path.splitext(path)
while ext != '.jpg' and ext != '.jpeg' and ext != '.png' and ext != '.gif':
    easygui.msgbox("图片格式不支持", title = '复读失败')
    path = ''
    path = easygui.fileopenbox(msg = "选择图片", filetypes = ["*.gif", "*.jpg", "*.png"])
    if path == '':
        sys.exit()
    shot, ext = os.path.splitext(path)


#处理输入图片
im = Image.open(path)
width, height = im.size
name = easygui.enterbox(msg = "输入要保存的文件名", title = '正在复读')
name = name + '.gif'
if im.format == 'PNG': #背景透明图片的处理
    p = Image.new('RGBA', im.size, (255,255,255))
    p.paste(im, (0, 0, width, height), im)
    im = p

#制作用于粘贴的底板
pastewid = width * 4
pastehi = height * 2
pasteIm = Image.new('RGB', (pastewid, pastehi), 'white')
copyIm = im.copy()
count = 1
images = []


#创建8个粘贴而得的帧
for top in range(0, pastehi, height):
    for left in range(0, pastewid, width):
        pasteIm = pasteIm.copy()
        pasteIm.paste(im, (left, top))
        pasteIm.save('paste%d.png'%(count))
        count = count + 1
        images.append(pasteIm)


#拼合各帧生成gif
filenames = ['paste1.png', 'paste2.png', 'paste3.png', 'paste4.png', 'paste5.png', 'paste6.png', 'paste7.png', 'paste8.png']
frames = []
for image in filenames:
    frames.append(imageio.imread(image))
imageio.mimsave(name, frames, 'GIF', duration = 0.25)
for image in filenames:
    os.remove(image)

easygui.msgbox("复读完成，可至程序根目录下提取", title = '复读完成')

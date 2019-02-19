import utils
from scipy.misc import imsave
import numpy as np
import platform,os
import cv2
import pylab as plt
import ezdxf
import parseDxf as dxf
from color_index import color_index





if __name__ == '__main__':
    fname = '0011'
    # img = cv2.imread(f'{fname}_aft.jpg', 0)  # 直接读为灰度图像
    crude_name=f'{fname}_aft.jpg'
    # crude_name='test.jpg'
    inName='in.bmp'
    outName='out.dxf'
    utils.jpg_to_bmp(crude_name,inName)
    img = plt.imread(crude_name)
    cmd=utils.merge_cmd(f'potrace-{platform.system()}/potrace',inName,'-o',outName,'-b','dxf')
    print(cmd)
    os.system(cmd)
    dwg = ezdxf.readfile("out.dxf")
    msp = dwg.modelspace()
    for i, polyline in enumerate(msp):
        line_set=dxf.Polygon(polyline)
        # print('fuck',len(line_set))
        shape=(500,500,3)
        canvas = np.ones(shape, np.uint8) * 255

        # ans=line_set.fun()
        line_set.display(canvas)
        ans=line_set.extractMidLine()


        ans.display(canvas, (0, 255, 0))
        # pl=line_set.extractMidLine()
        # pl.display(canvas)
        # r=20
        # pts=line_set.test(r)
        # dxf.display_points(canvas,pts)

        plt.imshow(canvas)
        plt.show()
        # if i >=3:
        #     break

# if __name__ == '__test__':
#     crude_name='img/multi_标注.jpg'
#     canvas_name='img/multi.jpg'
#     # crude_name='img/0597_标注.jpg'
#     # canvas_name='img/0597.jpg'
#     inName='in.bmp'
#     outName='out.dxf'
#     img=plt.imread(crude_name)
#     if len(img.shape)>2:
#         img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img=utils.reverse_gray(img)
#     canvas=plt.imread(canvas_name)[:,:,:3].copy()
#     imsave(inName,img)
#     # utils.jpg_to_bmp(crude_name,inName)
#
#     cmd=utils.merge_cmd(f'potrace-{platform.system()}\\potrace',inName,'-o',outName,'-b','dxf')
#     print(cmd)
#     os.system(cmd)
#     dwg = ezdxf.readfile("out.dxf")
#     msp = dwg.modelspace()
#     size = canvas.shape
#     sum_long=0;sum_max_width=0;sum_area=0;sum_width=0;sum_pt=0
#     n=0
#     for i, polyline in enumerate(msp):
#         n+=1
#         line_set = dxf.LineSet(polyline)
#         line_set.reverse(size)
#         line_set.color = color_index[i % 12]
#         # ans,_=line_set.growth(line_set.startL)
#         line_set.paint_polygon(size,canvas,n)
#         long, max_width, mean_width,area,t_sum_width,t_sum_pt = line_set.form_report()
#         # return long, max_width, mean_width, area, mean_width, sum_width, ptn
#         sum_long+=long;sum_max_width=max(sum_max_width,max_width);sum_area+=area;sum_width+=t_sum_width;sum_pt+=t_sum_pt
#         print('颜色,',line_set.color)
#         print('裂缝编号, %02d' % i)
#         print('长度, %.4f'%long)
#         print('最大宽度, %.4f'%max_width)
#         print('平均宽度, %.4f'%mean_width)
#         print('面积, %.4f'%area)
#     sum_mean_width=sum_width/sum_pt
#     print('汇总:')
#     print('总长度, %.4f' % sum_long)
#     print('最大宽度, %.4f' % sum_max_width)
#     print('平均宽度, %.4f' % sum_mean_width)
#     print('总面积, %.4f' % sum_area)
#     imsave('ans.jpg',canvas)
#     plt.imshow(canvas)
#     plt.show()

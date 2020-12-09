import numpy as np

def load_yuv(filename,height,width,num_frame):
    fp = open(filename, 'rb')
    fp.seek(0, 0)
    d1=height//2
    d2=width//2
    result=[]
    print("Loading frames!")
    for i in range(num_frame):
        Y = np.zeros((height, width), dtype='uint8')
        U = np.zeros((d1,d2), dtype='uint8')
        V = np.zeros((d1,d2), dtype='uint8')
        for m in range(height):
            for n in range(width):
                Y[m, n] = ord(fp.read(1))
        for m in range(d1):
            for n in range(d2):
                U[m, n] = ord(fp.read(1))
        for m in range(d1):
            for n in range(d2):
                V[m, n] = ord(fp.read(1))
        img=(Y,U,V)
        result.append(img)
        print(i+1,"/",num_frame)
    fp.close()
    print("Done!")
    return result

height=360
width=640
num_frame=617
video_frame=load_yuv("yourname.yuv",height,width,num_frame)

#分离奇场和偶场
odd_field=[]
even_field=[]
print("Parsing odd and even fileds!")
for i in range(num_frame):
    if (i+1)%2!=0:
        odd_img=video_frame[i]
        for m in range(height):
            if (m+1)%2==0:
                for n in range(width):
                    odd_img[0][m][n]=0
        odd_field.append(odd_img)
    else:
        even_img=video_frame[i]
        for m in range(height):
            if (m+1)%2!=0:
                for n in range(width):
                    even_img[0][m][n]=0
        even_field.append(even_img)
    print(i+1,"/",num_frame)
print("Done!")

#Bob滤波
def Bob_filter():
    print("Bob滤波")
    print("对奇场的偶数行插值")
    for i in range(len(odd_field)):
        for m in range(height):
            if (m+1)%2==0 and m+1!=height:  #忽略奇场最后一行
                for n in range(width):
                    odd_field[i][0][m][n] = (odd_field[i][0][m-1][n]+odd_field[i][0][m+1][n])//2
        print(i+1,"/",len(odd_field))
    print("对偶场的奇数行插值")
    for i in range(len(even_field)):
        for m in range(height):
            if (m+1)%2!=0 and m+1!=1:   #忽略偶场第一行
                for n in range(width):
                    even_field[i][0][m][n] = (even_field[i][0][m-1][n]+even_field[i][0][m+1][n])//2
        print(i+1,"/",len(even_field))
    print("生成全尺度帧并保存为文件")
    f=open("bob.yuv",'wb')
    d1 = height // 2
    d2 = width // 2
    for i in range(num_frame//2):
        #奇场
        for m in range(height):
            for n in range(width):
                f.write(odd_field[i][0][m][n])
        for m in range(d1):
            for n in range(d2):
                f.write(odd_field[i][1][m][n])
        for m in range(d1):
            for n in range(d2):
                f.write(odd_field[i][2][m][n])
        #偶场
        for m in range(height):
            for n in range(width):
                f.write(even_field[i][0][m][n])
        for m in range(d1):
            for n in range(d2):
                f.write(even_field[i][1][m][n])
        for m in range(d1):
            for n in range(d2):
                f.write(even_field[i][2][m][n])
        print(i+1,"/",num_frame//2)
    f.close()
    print("Done!")

#Weave滤波
def Weave_filter():
    print("Weave滤波")
    for i in range(num_frame // 2):
        for m in range(height):
            if (m+1)%2==0:
                for n in range(width):
                    odd_field[i][0][m][n] = even_field[i][0][m][n]
        print(i+1,"/",num_frame//2)
    print("生成全尺度帧并保存为文件")
    f = open("weave.yuv", 'wb')
    d1 = height // 2
    d2 = width // 2
    for i in range(num_frame // 2):
        for _ in range(2):
            for m in range(height):
                for n in range(width):
                    f.write(odd_field[i][0][m][n])
            for m in range(d1):
                for n in range(d2):
                    f.write(odd_field[i][1][m][n])
            for m in range(d1):
                for n in range(d2):
                    f.write(odd_field[i][2][m][n])
        print(i+1,"/",num_frame//2)
    f.close()
    print("Done!")

#Bob_filter()
Weave_filter()
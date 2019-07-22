from wand.image import Image as Img
from os import listdir
from os.path import isfile, join


def pdf_to_img(filename,index):
#     num = filename.split('/')      This commented code 
#     num = num[2]                      places same file name of the pdf to img
#     num = num.split('.')
#     num = num[0]
#     print("data from split",num)
    with Img(filename=filename, resolution=300) as img:
        img.compression_quality = 50
        #Below specify the output folder 
        img.save(filename='./new_data/5/{}.jpg'.format(str(index)))

# Input folder path
mypath = './1003-final/5/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i,item in enumerate(onlyfiles):
    # Input folder path    
    file_path = mypath+item
    print(file_path)
    pdf_to_img(file_path,i)


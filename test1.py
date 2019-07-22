import re
import shutil
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./loan-classifier-781576a111b2.json"

# output = 'results2/output-1-to-1.json'
# for_pg_num = output.split('/')
# input = for_pg_num[1]
# number = re.findall('\d+',input) 
# # numbers = map(int,numbers)
# number = int(number[0])
# print(number)

import os 
  
# Function to rename multiple files 
def main(): 

    i = 0
      
    for filename in os.listdir("./new_data_1003/"): 
        dst =str(i) + ".jpg"
        src ='./new_data_1003/'+ filename 
        dst ='./new/'+ dst 
          
        # rename() function will 
        # rename all the files 
        os.rename(src, dst) 
        i += 1


def main1(): 
    i = 0
    j=0
    k=0
    l=0
    for filename in os.listdir("./pdfToImg/"): 
        

        num = filename.split('-')
        num = num[1]
        num = num.split('.')[0]
        print(num)
        if num == '0':
                dst1 =str(i) + ".jpg"
                dst ='./pdftoimg-structured/0/'+ dst1
                i += 1
        # elif num == '1':
        #         dst1 =str(j) + ".jpg"
        #         dst ='./pdftoimg-structured/1/'+ dst1   
        #         j += 1
        # elif num == '2':
        #         dst1 =str(k) + ".jpg"
        #         dst ='./pdftoimg-structured/2/'+ dst1
        #         k += 1
        # elif num == '3':
        #         dst1 =str(l) + ".jpg"
        #         dst ='./pdftoimg-structured/3/'+ dst1
        #         l += 1

        

        src ='./pdfToImg/'+ filename 
         
        # rename() function will 
        # rename all the files 
        os.rename(src, dst) 

def main2():
        for filename in os.listdir("./example_conversion/"):
                print(filename)
                file_path =  './example_conversion/'+filename
                from PIL import Image
                from io import BytesIO

                im = Image.open(file_path)
                width, height = im.size
                print("height =",height)
                print("width =",width)
                i = im.resize((1000,1000)).convert('LA')
                # img = Image.open('image.png').convert('LA')
                i.save('grey {}.png'.format(filename))
                print(i)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
        from google.cloud import vision
        from google.cloud import storage    
        """Uploads a file to the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
                source_file_name,
                destination_blob_name))

def upload_to_storage():
        bucket_name = 'loan-submissions'
        
        for filename in os.listdir("./remaining_conversions/"):
                destination_blob_name = "note2/"+ filename
                source_file_name = "./remaining_conversions/"+filename
                upload_blob(bucket_name, source_file_name, destination_blob_name)
                print("Following file uploaded ",filename)

def list_files():
        from google.cloud import vision
        from google.cloud import storage
        from google.protobuf import json_format
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('loan-submissions')

        # List objects with the given prefix.
        blob_list = list(bucket.list_blobs(prefix='note-fixed/'))
        print('Output files:')
        for blob in blob_list:
                name  = str(blob.name).split('/')[1]
                print(name)

def read_csv():
        import csv
        with open('pg4.csv') as f:
                reader = csv.reader(f)
                your_list = list(reader)

        
        print(your_list[1][0].replace('\n',' '))  # So there are 136 data points in pg1



def imgprocess():
        i = 0
        input_path = './note_1003_img_dataset/test/note/'
        output_path = './note_1003_img_dataset/new/test/note/'

        for filename in os.listdir(input_path): 
                from PIL import Image,ImageFile
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                img = Image.open(input_path+filename)
                img = img.resize((240,240), Image.ANTIALIAS)
                img.save(output_path+str(i)+'.png',optimize=True,quality=20)
                i = i+1
                print('It is done ',i)


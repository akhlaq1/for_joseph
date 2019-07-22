import os
import re
import csv
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./loan-classifier-781576a111b2.json"
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format



def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 1

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    pg_1 = []
    pg_2 = []
    pg_3 = []
    pg_4 = []
    pg_5 = []
    
    for i,item in enumerate(blob_list):
        if i==0:
            pass
        else:
            output = blob_list[i]
            str_output = str(blob_list[i])
            
            print("This is output ",str_output)
            num = str_output.split('/')
            
            num = num[1]
            num  = num.split('.')
            num = num[0]
            number = re.findall(r'\d+', num)[0]
            print("This is number ",number)
            print("this is type of number ",type(number))
            json_string = output.download_as_string()
            response = json_format.Parse(
                json_string, vision.types.AnnotateFileResponse())

            # The actual response for the first page of the input file.
            first_page_response = response.responses[0]
            annotation = first_page_response.full_text_annotation
            text = annotation.text
            if number == '1':
                pg_1.append(text)
            elif number == '2':
                pg_2.append(text)
            elif number == '3':
                pg_3.append(text)
            elif number == '4':
                pg_4.append(text)
            else:
                pg_5.append(text)

            output.delete()


            # Here we print the full text from the first page.
            # The response contains more information:
            # annotation/pages/blocks/paragraphs/words/symbols
            # including confidence scores and bounding boxes




            print(u'Full text:\n{}'.format(
                annotation.text))
    myData1 = [
                pg_1
    ]
    myFile1 = open('./1003_full_text/pg1.csv', 'a')
    with myFile1:
        writer = csv.writer(myFile1)
        writer.writerows(myData1)

    
    myData2 = [
                pg_2
    ]
    myFile2 = open('./1003_full_text/pg2.csv', 'a')
    with myFile2:
        writer = csv.writer(myFile2)
        writer.writerows(myData2)
    
    
    myData3 = [
                pg_3
    ]
    myFile3 = open('./1003_full_text/pg3.csv', 'a')
    with myFile3:
        writer = csv.writer(myFile3)
        writer.writerows(myData3)

    
    myData4 = [
                pg_4
    ]
    myFile4 = open('./1003_full_text/pg4.csv', 'a')
    with myFile4:
        writer = csv.writer(myFile4)
        writer.writerows(myData4)

    
    
    myData5 = [
                pg_5
    ]
    myFile5 = open('./1003_full_text/pg5.csv', 'a')
    with myFile5:
        writer = csv.writer(myFile5)
        writer.writerows(myData5)

    print("Writing complete")           
    
def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix='loan_application/')


    for i,blob in enumerate(blobs):
        print(blob.name)
        if i==0:
            pass
        else:
            print("This is blob.name ", blob.name)
            gcs_source_uri = 'gs://loan-submissions/'+ blob.name
            gcs_destination_uri = 'gs://loan-submissions/results2/'    
            async_detect_document(gcs_source_uri, gcs_destination_uri)



list_blobs('loan-submissions')
import io
from datetime import datetime
from time import sleep

import boto3
from picamera import PiCamera
from PIL import Image, ImageDraw, ImageFont
import json


class Rekognizer():
    """Class to handle communication between Rasperry Pi camera and AWS Rekognizer.
    """
    def __init__(self, output_photo: str, sleep_time: int = 2):
        self.camera = PiCamera()
        self.sleep_time = sleep_time
        self.output_photo = output_photo
        
    def start(self):
        self.take_picture()
        photo = self.covert_img_to_bytes()
        results = self.add_boxes()
        # results = self.aws_rekognition_image(photo)
        # self.print_results(results)
                    
    def take_picture(self):
        self.camera.resolution = (1920, 1080)
        # self.camera.rotation = 180
        self.camera.start_preview()
        sleep(self.sleep_time)
        self.camera.capture(output=self.output_photo)
        self.camera.stop_preview()

    def stop_camera(self):
        self.camera.stop_recording()
        
    def aws_rekognition_image(self, photo):
        client = boto3.client('rekognition',
                              region_name='eu-central-1')
        return client.detect_labels(Image={'Bytes': photo})
    
    def covert_img_to_bytes(self):
        with open(self.output_photo, 'rb') as photo:
            return photo.read()
    
    def print_results(self, results):
        for each in results['Labels']:
            print(each['Name'] + ": " + str(each['Confidence']))

    def add_boxes(self):
        rek_client = boto3.client('rekognition')
        with open(self.output_photo, 'rb') as im:
            # Read image bytes
            im_bytes = im.read()
            # Upload image to AWS 
            response = rek_client.detect_faces(Image={'Bytes': im_bytes}, Attributes=['ALL'])
            # Get default font to draw texts
            image = Image.open(io.BytesIO(im_bytes))
            font = ImageFont.truetype('FreeSerif.ttf', size=60)
            draw = ImageDraw.Draw(image)
            # Get all labels
            w, h = image.size
            num_face = 1
            for face in response['FaceDetails']:
                # Draw all instancex box, if any
                bbox = face['BoundingBox']
                x0 = int(bbox['Left'] * w)
                y0 = int(bbox['Top'] * h)
                x1 = x0 + int(bbox['Width'] * w)
                y1 = y0 + int(bbox['Height'] * h)
                draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=10)
                draw.text((x0, y1), str(num_face), font=font, fill=(255, 0, 0))
                num_face = num_face + 1
                print("#######################################")
                print(f"Face {num_face}:")
                print(json.dumps(face['Emotions'], indent=4))
            image.save(self.output_photo)
            print(len(response['FaceDetails']))
            return response

def main():
    rekognizer = Rekognizer(
        output_photo='static/test.jpg',
        sleep_time=2
    )
    rekognizer.start()
    

if __name__ == "__main__":
    main()
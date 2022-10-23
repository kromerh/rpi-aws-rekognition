from picamera import PiCamera
from datetime import datetime
import boto3
from time import sleep
from PIL import Image, ImageDraw, ImageFont


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
        results = self.aws_rekognition_image(photo)
        self.print_results(results)
                    
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
        with open(self.source_photo, 'rb') as photo:
            return photo.read()
    
    def print_results(self, results):
        for each in results['Labels']:
            print(each['Name'] + ": " + str(each['Confidence']))
        

def main():
    rekognizer = Rekognizer(
        output_photo='test.jpg',
        sleep_time=2
    )
    rekognizer.start()
    

if __name__ == "__main__":
    main()
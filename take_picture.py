import io
from datetime import datetime
from time import sleep

import boto3
from picamera import PiCamera

s3 = boto3.client("s3")

class PiPicture():
    """Class to take a picture with the Pi camera.
    """
    def __init__(self):
        """Class init.
        """
        self.camera = PiCamera()
        self.output_photo = 'input.jpg'

    def take_picture(self):
        """Method to take a photo with the Pi camera.
        """
        self.camera.resolution = (1920, 1080)
        self.camera.start_preview()
        sleep(0.01)
        self.camera.capture(output=self.output_photo)
        self.camera.stop_preview()
        print(f"### Took photo {self.output_photo}")
    
    def upload_to_s3(self, bucket: str):
        """Method to upload the photo to s3.
        """
        
        _ = s3.upload_file(
          Body = self.output_photo,
          Bucket = bucket,
          Key = self.output_photo
        )
        print(f"### Uploaded to bucket {bucket}")
        
def main():
    pi_picture = PiPicture()
    pi_picture.take_picture()
    sleep(0.01)
    pi_picture.upload_to_s3(bucket="face-rekog-input-dev-20230201") 

if __name__ == "__main__":
    main()

import sys
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
        self.camera.close()
    
    def upload_to_s3(self, bucket: str):
        """Method to upload the photo to s3.
        """
        
        _ = s3.upload_file(
          self.output_photo,
          bucket,
          self.output_photo
        )
        print(f"### Uploaded to bucket {bucket}")

class LiveHandler():
    """Class to take pictures and upload to S3 live.
    """
    def __init__(
        self,
        sleep_time: float = 0.1,
        s3_bucket: str = "face-rekog-input-dev-20230201"
    ) -> None:
        self.sleep_time = sleep_time
        self.s3_bucket = s3_bucket
    
    def take_photo(self):
        """Method to take a photo and upload to s3."""
        pi_picture = PiPicture()
        pi_picture.take_picture()
        pi_picture.upload_to_s3(bucket=self.s3_bucket)
  
    def run(self):
        """Method to run endlessly."""
        try:
            while True:
                self.take_photo()
                sleep(self.sleep_time)

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    handler = LiveHandler(
        sleep_time=0.1,
        s3_bucket="face-rekog-input-dev-20230201"
    )
    handler.run()

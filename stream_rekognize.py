import os
import time

import bottle
from bottle import route, run, template, BaseTemplate, static_file

import numpy as np
from PIL import Image

from rekognizer import Rekognizer

app = bottle.default_app()
BaseTemplate.defaults['get_url'] = app.get_url

@route('/')
def index():
    return template('''<!DOCTYPE html>
<html>
<head>
    <title>HARTA</title>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
</head>
<body>
    <img id="map" src="{{ get_url('static', filename='map.png') }}" />
    <script>
      $(document).ready(function(){
        setInterval(refreshFunction, 3000);
      });

      function refreshFunction(){
        $.get('/refresh', function(){            
            d = new Date();
            $("#map").attr("src", "{{ get_url('static', filename='map.png') }}?"+d.getTime());            
            console.log($("#map").attr("src"));
        });
      }
    </script>
</body>
</html>''')

@route('/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root='static')

@route('/refresh')
def refresh():
    os.makedirs('static', exist_ok=True)
    rekognizer = Rekognizer(
        output_photo='static/test.jpg',
        sleep_time=2
    )
    rekognizer.start()
    return "OK" 
    
run(host='0.0.0.0', port=8080)
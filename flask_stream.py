import os
import time

import bottle
from bottle import route, run, template, BaseTemplate, static_file

import numpy as np
from PIL import Image

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
        setInterval(refreshFunction, 1000);
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
    newmapp = np.random.rand(100,100,3) * 255    
    data = Image.fromarray(newmapp.astype('uint8')).convert('RGBA')
    data.save('static/map.png')
    return "OK" 
    
run(host='0.0.0.0', port=8080)
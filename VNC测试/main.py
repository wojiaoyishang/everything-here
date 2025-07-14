from vncdotool import api

with api.connect("191.168.1.0::7900") as client:
    client.type("废物")
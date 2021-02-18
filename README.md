# Relassy Bluetooth Light Bridge
Connects to Relassy Aquarium Lights (https://www.amazon.de/-/en/gp/product/B07KKBNNS1/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) with Bluetooth and makes them automatable.


### Setup of Raspberry


```console
sudo apt install bluetooth libbluetooth-dev
sudo apt-get install libglib2.0-dev
pip3 install bluepy
```

Unfortunately, Alexa is not able to call local URLs. You can use Siri Shortcuts, though.
# py3-common

This is my own written python standard library which I use in multiple of my programming projects.

# Content
## Log
Provides a class `Logger` which is responsible for... logging messages. Surprise surprise.

## Monitoring
Provides a class `Monitoring` methods for Icinga2 Monitoring Checks

## FritzBox AHA
Provides a class `FritzBoxAHA` to interact with the FRITZ!Box SmartHome Automation API.

## VictoriaMetrics
Provides a class `VictoriaMetrics` to interact with the API of a VictoriaMetrics host.

## Utils
* Provides a class `HTTP` which is a gerneric "Adapter" for making http requests. It always returns
a predefined structure.
* `times` are handy utilities for doing heavy datetime shannanigans like formatting, timezone calculations and so on. Basically the annoying stuff.
* `files` is a toolbox for interacting with files like opening a yaml file, saving a file to a given path, join paths and so on.


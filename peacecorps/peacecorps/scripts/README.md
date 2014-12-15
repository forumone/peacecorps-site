# Scripts

## Crop Map

Wikipedia [provides](http://en.wikipedia.org/wiki/File:BlankMap-World6.svg) a
beautiful SVG map of the world, complete with well-labeled country boundaries.
This file is quite large, however, and we must manipulate it to highlight and
zoom to specific countries. Performing this in the browser is workable when
there is only one map, but when listing many images of countries, the DOM
quickly exceeds a reasonable amount of memory. This script, then, splits the
world map into component countries, providing context in the form of
surrounding countries and highlighting/zooming to the selected country.

To use the script, you must first install two python libraries: `lxml` and
[svg](https://github.com/cjlano/svg) from source. Clone the latter repository
within this `scripts` directory. Then run the script with the input SVG file
and the output directory:

```bash
pip install lxml
git clone https://github.com/cjlano/svg.git
python cropmap.py ../static/peacecorps/img/BlankMap-World6.svg ../static/peacecorps/img/countries/
```

You will see several debug messages which can be safely ignored. Execution
takes around 5 minutes to run on a decent machine.

TODO: It'd make sense to simplify the shapes/otherwise reduce the file size.
The script removes unseen countries, but it could definitely be improved.

## Crop To

Similar to the above script, but zooms in to a particular area instead of a
single country.

```bash
python croptoview.py ../static/peacecorps/img/BlankMap-World6.svg ../static/peacecorps/img/countries/esc.svg 725 550 125 125
```

<h1>Countries</h1>
In this section:

[TOC]

<hr>

The site pulls its knowledge of countries from an initial [fixture](https://github.com/Threespot/peacecorps-site/blob/master/peacecorps/peacecorps/fixtures/countries.yaml) that is a current representation of [ISO 3166-1](http://en.wikipedia.org/wiki/ISO_3166-1) as of March 27th, 2015.

## Adding a New Country
In the event a new country is added to ISO 3166-1, three changes should happen:

1. A developer should edit the [fixture](https://github.com/Threespot/peacecorps-site/blob/master/peacecorps/peacecorps/fixtures/countries.yaml)
2. In the admin panel, go to `Countries > Add Country +` and create a new country with the ISO 3166-1 Code and Name.
3. A developer should use the [Cron Map script](https://github.com/Threespot/peacecorps-site/tree/master/peacecorps/peacecorps/scripts) to generate a new set of map files. For more information, see [Generating Maps](#generating-maps).

### Generating Maps

For detailed information, see [the GitHub repository](https://github.com/Threespot/peacecorps-site/blob/master/peacecorps/peacecorps/scripts/README.md).

Wikipedia [provides](http://en.wikipedia.org/wiki/File:BlankMap-World6.svg) a
beautiful SVG map of the world, complete with well-labeled country boundaries.
This file is quite large, however, and we must manipulate it to highlight and
zoom to specific countries. Performing this in the browser is workable when
there is only one map, but when listing many images of countries, the DOM
quickly exceeds a reasonable amount of memory. We have created a script that
splits the world map into component countries, providing context in the form of
surrounding countries and highlighting/zooming to the selected country.

To use the script, you must first install two python libraries: `lxml` and
[svg](https://github.com/cjlano/svg) from source. Clone the latter repository
within the `peacecorps/peacecorps/scripts` directory. Then run the script with the input SVG file
and the output directory:

```bash
pip install lxml
git clone https://github.com/cjlano/svg.git
python cropmap.py ../static/peacecorps/img/BlankMap-World6.svg ../static/peacecorps/img/countries/
```

You will see several debug messages which can be safely ignored. Execution
takes around 5 minutes to run on a decent machine.

### Crop To

Similar to the above script, but zooms in to a particular area instead of a
single country. This is useful if the automatically generated map for a specific country does not provide 
sufficient detail or otherwise look very good.

```bash
python croptoview.py ../static/peacecorps/img/BlankMap-World6.svg ../static/peacecorps/img/countries/esc.svg 700 560 125 125
```
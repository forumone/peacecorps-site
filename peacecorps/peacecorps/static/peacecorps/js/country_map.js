'use strict';

/* @namespace */
var PC = PC || {};

(function() {

  /*
   * Country Map
   *
   * An SVG map which sets a class to style a certain country and then zooms
   * in on it.
   *
   * @constructor
   * @param {SVGObject} map - An svg DOM object to manipulate.
   * @param {string} selectedCountryCode - The country code used for selecting
   *  in the map document.
   */
  PC.CountryMap = function(map, selectedCountryCode) {
    this.map = map;
    this.selectedCountryCode = selectedCountryCode.toLowerCase();
  };

  /*
   * Initialize the CountryMap by highlighting the country and zooming in
   * to it.
   */
  PC.CountryMap.prototype.init = function() {
    var selectedCountry = this.map.querySelectorAll(
          '.' + this.selectedCountryCode)[0],
        coords = null;
    if (!selectedCountry) {
      // TODO handle error condition.
      return;
    }
    coords = this.calculateCountryCoords(selectedCountry);

    this.highLightCountry(this.selectedCountryCode);
    this.zoomToCountry(coords, selectedCountry.ownerSVGElement.getBBox());
  };

  /*
   * Account for SVG transformations when determining a bounding box
   */
  PC.CountryMap.prototype.calculateCountryCoords = function(element) {
    var bbox = element.getBBox(),
        svg = element.ownerSVGElement,
        transform = element.getTransformToElement(svg),
        ul = svg.createSVGPoint(),
        lr = svg.createSVGPoint();
    ul.x = bbox.x;
    ul.y = bbox.y;
    lr.x = bbox.x + bbox.width;
    lr.y = bbox.y + bbox.height;
    ul = ul.matrixTransform(transform);
    lr = lr.matrixTransform(transform);
    return {x: ul.x, y: ul.y, width: lr.x - ul.x, height: lr.y - ul.y};
  };

  /*
   * Highlight the country by setting a certain css class on it. This class
   * should be styled externally.
   *
   * @param {string} countryCode - The country code to select and style.
   */
  PC.CountryMap.prototype.highLightCountry = function(countryCode) {
    var countryPaths = [],
        path = {},
        i, ilen;

    countryPaths = this.map.querySelectorAll('.' + countryCode);
    for (i = 0, ilen = countryPaths.length; i < ilen; i++) {
      path = countryPaths[i];
      // TODO replace with class adding util.
      if (path.classList) {
        path.classList.add('world_map-is_selected');
      } else {
        path.className += ' ' + 'world_map-is_selected';
      }
    }
  };

  /*
   * Zoom to the country. Adds a margin of 80% the country size or 20% of the
   * whole map, whichever is smaller.
   *
   * @param {object} countryCoords - The coordinates to zoom to.
   */
  PC.CountryMap.prototype.zoomToCountry = function(countryCoords, mapBounds) {
    var margin = 0.9, /* as a percentage of the country size */
        coords = $.extend({}, countryCoords),
        factor = null,
        imgWidth = null,
        imgHeight = null,
        zoomLevel = null;

    if (coords.width * margin > mapBounds.width * 0.1) {
      margin = mapBounds.width * 0.1 / coords.width;
    }
    if (coords.height * margin > mapBounds.height * 0.1) {
      margin = mapBounds.height * 0.1 / coords.height;
    }

    factor = 1 + (2 * margin);
    imgWidth = factor * coords.width;
    imgHeight = factor * coords.height;
    if (imgWidth / mapBounds.width < 0.05) { zoomLevel = 'zoom4'; }
    else if (imgWidth / mapBounds.width < 0.1) { zoomLevel = 'zoom3'; }
    else if (imgWidth / mapBounds.width < 0.2) { zoomLevel = 'zoom2'; }
    else { zoomLevel = 'zoom1'; }
    // TODO replace with class adding util.
    if (this.map.classList) {
      this.map.classList.add(zoomLevel);
    } else {
      this.map.className += ' ' + zoomLevel;
    }

    this.map.setAttribute('viewBox',
      (coords.x - margin*coords.width) + ' ' +
      (coords.y - margin*coords.height) + ' ' +
      imgWidth + ' ' + imgHeight);

  };

  // main
  // Start when the svg map object is loaded.
  document.getElementById('js-worldMap').addEventListener('load',
      function(){
    var elMap,
        svg,
        countryMap,
        selectedCountryCode = '';

    elMap = document.getElementById('js-worldMap');
    svg = elMap.contentDocument.querySelectorAll('svg')[0];
    selectedCountryCode = elMap.getAttribute('data-country');

    countryMap = new PC.CountryMap(svg, selectedCountryCode);
    countryMap.init();
  });
})();

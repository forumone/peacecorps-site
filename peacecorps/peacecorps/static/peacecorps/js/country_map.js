
/* @namespace */
var PC = PC || {};

(function() {
  'use strict';

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
    var selectedCountry = this.map.getElementById(this.selectedCountryCode);
    if (!selectedCountry) {
      // TODO handle error condition.
      return;
    }
    this.selectedCountryCoords = selectedCountry.getBBox();

    this.highLightCountry(this.selectedCountryCode);
    this.zoomToCountry(this.selectedCountryCoords);
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
        el.className += ' ' + 'world_map-is_selected';
      }
    }
  };

  /*
   * Zoom to the country.
   *
   * @param {object} countryCoords - The coordinates to zoom to.
   */
  PC.CountryMap.prototype.zoomToCountry = function(countryCoords) {
    // TODO scaling factor is arbituary, have to check how well it works for
    // all countries.
    var factor = 80,
        coords = $.extend({}, countryCoords);

    coords.x = parseFloat(coords.x, 10) - factor;
    coords.y = parseFloat(coords.y, 10) - factor;
    coords.width = parseFloat(coords.width, 10) + factor;
    coords.height = parseFloat(coords.height, 10) + factor;
    this.map.setAttribute('viewBox',
      coords.x + ' ' +
      coords.y + ' ' +
      coords.width + ' ' +
      coords.height);

  };

  // main
  // Start when the svg map object is loaded.
  document.getElementById('js-worldMap').addEventListener('load',
      function(){
    var elMap,
        countryMap,
        selectedCountryCode = '';

    elMap = document.getElementById('js-worldMap')
      .contentDocument
      .querySelectorAll('svg')[0];
    selectedCountryCode = elMap.getAttribute('data-country');
    selectedCountryCode = 'br';

    countryMap = new PC.CountryMap(elMap, selectedCountryCode);
    countryMap.init();
  });
})();

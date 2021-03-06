v1.2.0
======
Added
-----
* The ``mapplot`` plotmethod now also supports unstructured data of any shape
  (see `issue#6 <https://github.com/Chilipp/psyplot/issues/6>`__)

Changed
-------
* The ``lonlatbox`` formatoption now selects a subset of the unstructured data
  to lower the size of the data array. Previously, data points outside the
  specified `lonlatbox` where simply set to NaN

v1.1.0
======
Added
-----
* Changelog
* ``stock_img`` formatoption for map plots (see the
  `docs <https://psyplot.readthedocs.io/projects/psy-maps/en/latest/api/psy_maps.plotters.html#psy_maps.plotters.FieldPlotter.stock_img>`__)
* Added ``'stereo'`` and ``'near'`` projections for the
  `projection <https://psyplot.readthedocs.io/projects/psy-maps/en/latest/api/psy_maps.plotters.html#psy_maps.plotters.FieldPlotter.projection>`__
  formatoption
* The ``lonlatbox`` and ``map_extent`` formatoption keywords now also accepts
  a combination of floats and strings
* When displaying all longitudes but not all latitudes, the
  ``map_extent`` keyword now adjusts the boundary of the map to keep it
  circular for Stereographic and Orthographic projections

Changed
-------
* Fixed bugs with displaying circumpolar data and stereographic and
  orthographic projections

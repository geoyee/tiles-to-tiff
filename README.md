# tiles2tiff
Python script for converting XYZ raster tiles for slippy maps to a georeferenced TIFF image. From [https://github.com/jimutt/tiles-to-tiff](https://github.com/jimutt/tiles-to-tiff). 

By the way:

> X goes from 0 (left edge is 180 °W) to 2^zoom − 1 (right edge is 180 °E)
> Y goes from 0 (top edge is 85.0511 °N) to 2^zoom − 1 (bottom edge is 85.0511 °S) in a Mercator projection
>
> For the curious, the number 85.0511 is the result of arctan(sinh(π)). By using this bound, the entire map becomes a (very large) square.

## Requirement:

- install GDAL.
- Add [Mapbox's token](https://account.mapbox.com/), create PATH named `Mapbox_token` and input your token.

## Usage:

```
python tiles_to_tiff.py
```

## Update:

Fix it as a function, and try to transplant it to our QGIS plugin [buildseg](https://github.com/deepbands/buildseg).


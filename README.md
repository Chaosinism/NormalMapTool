# NormalMapTool

## Script: Convert a Normal Map to a Height (Displacement) Map

**Dependencies:** Python3, Numpy, Scipy

**Usage:**

```
python N2H.py [Number of iterations] [NormalMapFile] [MaskFile (optional)]
```
*Number of iterations*: An integer, increasing the precision of generated height map, while requiring more execution time.

*NormalMapFile*: A PNG or JPG image

*MaskFile*: A PNG or JPG image, optional. If not provided, the script generates a mask based on the alpha channel of the normal map.

**Description:**

This is an unofficial implementation of the methods proposed in the following paper:

Hudon, Matis, et al. "[Augmenting Hand-Drawn Art with Global Illumination Effects through Surface Inflation."](https://v-sense.scss.tcd.ie/) European Conference on Visual Media Production. 2019.

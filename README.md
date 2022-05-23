## minicoco

This [script.py](https://github.com/tikitong/minicoco/blob/main/script.py) presents a quick alternative to [FiftyOne](https://voxel51.com/docs/fiftyone/#fiftyone-library) for creating a subset of the 2017 [coco dataset](https://cocodataset.org/#home). With the choice of classes, annotation file and number of images. It is inspired by the notebook [pycocoDemo](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoDemo.ipynb). 
 Its execution creates the following directory tree:
```
data/
  images/ *.jpg
  labels/ train.json
          val.json
```


## First time setup

The following steps are required in order to run the script, with conda and pip for example:
```
conda create -n myenv python=3.9
conda activate myenv
pip install pycocotools
pip install wget==3.0
pip install joblib
```
## Three changes to launch 

- [line 71](https://github.com/tikitong/minicoco/blob/7d43b9b2847fe021fe46d9c560c348c801c552ca/script.py#L53): download the annotations of [the 2017](http://images.cocodataset.org/annotations/annotations_trainval2017.zip) COCO dataset. Other annotation files can be found [here](https://cocodataset.org/#download). 

Customize your subset:

 - [line 74](https://github.com/tikitong/minicoco/blob/7d43b9b2847fe021fe46d9c560c348c801c552ca/script.py#L56): specify the list of category names of interest in the set of dataset classes. default: `["car", "airplane", "person"]`
 
- [line 96](https://github.com/tikitong/minicoco/blob/7d43b9b2847fe021fe46d9c560c348c801c552ca/script.py#L78): Choose the number of images for the training and validation set. default 30-10

run `python script.py`

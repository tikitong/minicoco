## minicoco

This script presents a quick alternative to [FiftyOne](https://voxel51.com/docs/fiftyone/#fiftyone-library) for creating a subset of the 2017 [coco dataset](https://cocodataset.org/#home). With the choice of categories and number of images. It is inspired by the notebook [pycocoDemo](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoDemo.ipynb) and help from [MMM](https://stackoverflow.com/a/73249837/14864907) answering concerning the small download method.

 Its execution creates the following directory tree:
```
data/
  images/ *.jpg
  labels/ train.json
          val.json
```


## Installation

The following steps are required in order to run the script, with conda and pip for example:
```
conda create -n minicoco python=3.9
conda activate minicoco
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip ./annotations_trainval2017.zip
pip install -r requirements.txt
```
## Usage

```
usage: script.py [-h] [-t TRAINNING] [-v VALIDATION] [-cat NARGS [NARGS ...]] annotation_file

positional arguments:
  annotation_file       annotations/instances_train2017.json path file.

optional arguments:
  -h, --help            show this help message and exit
  -t TRAINNING, --trainning TRAINNING
                        number of images in the trainning set.
  -v VALIDATION, --validation VALIDATION
                        number of images in the validation set.
  -cat NARGS [NARGS ...], --nargs NARGS [NARGS ...]
                        category names.
```
`python script.py annotations/instances_train2017.json -t 30 -v 10 -cat car airplane person`
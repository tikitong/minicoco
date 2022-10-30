## minicoco

This script presents a quick alternative to [FiftyOne](https://voxel51.com/docs/fiftyone/#fiftyone-library) to create a subset of the 2017 [coco](https://cocodataset.org/#home) dataset. It allows the generation of training and validation datasets. With a single *images* folder containing the images and a *labels* folder containing the image annotations for both datasets in COCO (JSON) format. It is inspired by the notebook [pycocoDemo](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoDemo.ipynb) and this [stackoverflow.](https://stackoverflow.com/a/73249837/14864907) solution. 

Its execution creates the following directory tree:
```
data/
    images/ *.jpg
    labels/ train.json
            val.json
```


### Installation

The following steps are required in order to run the script:
```
conda create -n minicoco python=3.9
conda activate minicoco
git clone https://github.com/tikitong/minicoco.git 
cd minicoco
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip ./annotations_trainval2017.zip
pip install -r requirements.txt
```
### Usage

```
usage: script.py [-h] [-t TRAINING] [-v VALIDATION] [-cat NARGS [NARGS ...]] annotation_file

positional arguments:
  annotation_file       annotations/instances_train2017.json path file.

optional arguments:
  -h, --help            show this help message and exit
  -t TRAINING, --training TRAINING
                        number of images in the training set.
  -v VALIDATION, --validation VALIDATION
                        number of images in the validation set.
  -cat NARGS [NARGS ...], --nargs NARGS [NARGS ...]
                        category names.
```
run `python script.py annotations/instances_train2017.json -t 30 -v 10 -cat car airplane person` 🚀
## minicoco

This script presents a quick alternative to [FiftyOne](https://voxel51.com/docs/fiftyone/#fiftyone-library) to create a subset of the 2017 [coco](https://cocodataset.org/#home) dataset. It allows the generation of training and validation datasets. With a single *images* folder containing the images and a *labels* folder containing the image annotations for both datasets in COCO (JSON) format. It is main inspired by the notebook [pycocoDemo](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoDemo.ipynb) and this [stackoverflow](https://stackoverflow.com/a/73249837/14864907) solution for the download method. 

Its execution creates the following directory tree:
```
data/
    images/ *.jpg
    labels/ train.json
            val.json
```


### Installation
The use of [conda](https://docs.conda.io/en/latest/miniconda.html) is recommended. 
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
The 80 categories that can be used with the `-cat` argument are the following: 
```
person bicycle car motorcycle airplane bus train truck boat traffic light fire hydrant stop sign parking meter bench bird cat dog horse sheep cow elephant bear zebra giraffe backpack umbrella handbag tie suitcase frisbee skis snowboard sports ball kite baseball bat baseball glove skateboard surfboard tennis racket bottle wine glass cup fork knife spoon bowl banana apple sandwich orange broccoli carrot hot dog pizza donut cake chair couch potted plant bed dining table toilet tv laptop mouse remote keyboard cell phone microwave oven toaster sink refrigerator book clock vase scissors teddy bear hair drier toothbrush
```
<details>
<summary>code</summary>

```python
#from https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocoDemo.ipynb
from pycocotools.coco import COCO
coco = COCO("annotations/instances_train2017.json")
cats = coco.loadCats(coco.getCatIds())
nms = [cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))
``` 

</details>

You can run for example: `python script.py annotations/instances_train2017.json -t 30 -v 10 -cat car airplane person`. 

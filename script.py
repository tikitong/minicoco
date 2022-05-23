# Fast script for the creation of a sub-set of the coco dataset in the form of a data folder.
#   data/
#     images/ *.jpg
#     labels/ train.json
#             val.json

import json
from pycocotools.coco import COCO
import wget
import numpy as np
from random import sample
from pathlib import Path
from joblib import delayed, Parallel

ANNOTATIONS = {"info": {
    "description": "my-project-name"
}
}


def myImages(images: list, train: int, val: int) -> tuple:

    myImagesTrain = images[:train]
    myImagesVal = images[train:train+val]

    return myImagesTrain, myImagesVal


def cocoJson(images: list) -> dict:

    arrayIds = np.array([k["id"] for k in images])

    annIds = coco.getAnnIds(imgIds=arrayIds, catIds=catIds, iscrowd=None)
    anns = coco.loadAnns(annIds)

    for k in anns:
        k["category_id"] = catIds.index(k["category_id"])+1

    catS = [{'id': int(value), 'name': key}
            for key, value in categories.items()]

    ANNOTATIONS["images"] = images
    ANNOTATIONS["annotations"] = anns
    ANNOTATIONS["categories"] = catS

    return ANNOTATIONS


def createJson(JsonFile: json, train: bool) -> None:

    name = "train"
    if not train:
        name = "val"

    Path("data/labels").mkdir(parents=True, exist_ok=True)

    with open(f"data/labels/{name}.json", "w") as outfile:
        json.dump(JsonFile, outfile)


def downloadImages(img: dict) -> None:

    link = (img['coco_url'])

    Path("data/images").mkdir(parents=True, exist_ok=True)

    wget.download(link, f"{'data/images/' + img['file_name']}")


# instantiate COCO specifying the annotations json path; download here: https://cocodataset.org/#download
coco = COCO('instances_train2017.json')

# Specify a list of category names of interest
catNms = ['car', 'airplane', 'person']

catIds = coco.getCatIds(catNms)

dictCOCO = {k: coco.getCatIds(k)[0] for k in catNms}
dictCOCOSorted = dict(sorted(dictCOCO.items(), key=lambda x: x[1]))

IdCategories = list(range(1, len(catNms)+1))
categories = dict(zip(list(dictCOCOSorted), IdCategories))

''''getCatIds return a sorted list of id. 
For the creation of the json file in coco format, the list of ids must be successive 1, 2, 3.. 
so we reorganize the ids. In the cocoJson method we modify the values of the category_id parameter '''

# Get the corresponding image ids and images using loadImgs
imgIds = coco.getImgIds(catIds=catIds)
imgOriginals = coco.loadImgs(imgIds)

# The images are selected randomly
imgShuffled = sample(imgOriginals, len(imgOriginals))

# Choose the number of images for the training and validation set. default 30-10
myImagesTrain, myImagesVal = myImages(imgShuffled, 30, 10)

trainSet = cocoJson(myImagesTrain)
createJson(trainSet, train=True)

valSet = cocoJson(myImagesVal)
createJson(valSet, train=False)

print("downloading training set...")
Parallel(
    n_jobs=-1, prefer="threads")([delayed(downloadImages)(img) for img in myImagesTrain])

print("\ndownloading validation set...")
Parallel(
    n_jobs=-1, prefer="threads")([delayed(downloadImages)(img) for img in myImagesVal])

print("\nfinish.")

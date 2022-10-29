# in case of use, please quote https://github.com/tikitong/minicoco repo and https://stackoverflow.com/a/73249837/14864907 solution. 

import os
import json
import argparse
import numpy as np
from pathlib import Path
from random import sample
from pycocotools.coco import COCO
from alive_progress import alive_bar

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

parser = argparse.ArgumentParser()

parser.add_argument("annotation_file", type=str,
                    help="annotations/instances_train2017.json path file.")

parser.add_argument("-t", "--trainning", type=int,
                    help="number of images in the trainning set.")

parser.add_argument("-v", "--validation", type=int,
                    help="number of images in the validation set.")

parser.add_argument("-cat", "--nargs", nargs='+',
                    help="category names.")

args = parser.parse_args()

Path("data/images").mkdir(parents=True, exist_ok=True)
Path("data/labels").mkdir(parents=True, exist_ok=True)

coco = COCO(args.annotation_file)
catNms = args.nargs
catIds = coco.getCatIds(catNms)
imgIds = coco.getImgIds(catIds=catIds)

imgOriginals = coco.loadImgs(imgIds)
imgShuffled = sample(imgOriginals, len(imgOriginals))

annotations = {"info": {
    "description": "my-project-name"
}
}


def myImages(images: list, train: int, val: int) -> tuple:
    myImagesTrain = images[:train]
    myImagesVal = images[train:train+val]
    return myImagesTrain, myImagesVal


def cocoJson(images: list) -> dict:
    '''getCatIds return a sorted list of id.
    for the creation of the json file in coco format, the list of ids must be successive 1, 2, 3..
    so we reorganize the ids. In the cocoJson method we modify the values of the category_id parameter.'''

    dictCOCO = {k: coco.getCatIds(k)[0] for k in catNms}
    dictCOCOSorted = dict(sorted(dictCOCO.items(), key=lambda x: x[1]))

    IdCategories = list(range(1, len(catNms)+1))
    categories = dict(zip(list(dictCOCOSorted), IdCategories))

    arrayIds = np.array([k["id"] for k in images])
    annIds = coco.getAnnIds(imgIds=arrayIds, catIds=catIds, iscrowd=None)
    anns = coco.loadAnns(annIds)
    for k in anns:
        k["category_id"] = catIds.index(k["category_id"])+1
    cats = [{'id': int(value), 'name': key}
            for key, value in categories.items()]
    annotations["images"] = images
    annotations["annotations"] = anns
    annotations["categories"] = cats

    return annotations


def createJson(jsonfile: json, train: bool) -> None:
    name = "train"
    if not train:
        name = "val"
    with open(f"data/labels/{name}.json", "w") as outfile:
        json.dump(jsonfile, outfile)


def downloadImages(img: list, title: str) -> None:
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    with alive_bar(len(img), title=title) as bar:
        for im in img:
            if not os.path.isfile(f"data/images/{im['file_name']}"):
                img_data = session.get(im['coco_url']).content
                with open('data/images/' + im['file_name'], 'wb') as handler:
                    handler.write(img_data)
            bar()


imagetrain, imageval = myImages(imgShuffled, args.trainning, args.validation)

trainset = cocoJson(imagetrain)
createJson(trainset, train=True)
downloadImages(imagetrain, title='Downloading images of the trainning set:')

valset = cocoJson(imageval)
createJson(valset, train=False)
downloadImages(imageval, title='Downloading images of the validation set:')


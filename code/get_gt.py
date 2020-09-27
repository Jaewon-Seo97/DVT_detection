from xml.etree import ElementTree
from utils import *


def get_gt(filename, num_class, normalize=False):
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    bounding_boxes = []
    one_hot_classes = []
    size_tree = root.find('size')
    width = float(size_tree.find('width').text)
    height = float(size_tree.find('height').text)
    for object_tree in root.findall('object'):
        for bounding_box in object_tree.iter('bndbox'):
            if normalize:
                xmin = float(bounding_box.find('xmin').text) / width
                ymin = float(bounding_box.find('ymin').text) / height
                xmax = float(bounding_box.find('xmax').text) / width
                ymax = float(bounding_box.find('ymax').text) / height
            else:
                xmin = float(bounding_box.find('xmin').text)
                ymin = float(bounding_box.find('ymin').text)
                xmax = float(bounding_box.find('xmax').text)
                ymax = float(bounding_box.find('ymax').text)
        bounding_box = [xmin, ymin, xmax, ymax]
        bounding_boxes.append(bounding_box)
        class_name = object_tree.find('name').text
        one_hot_class = _to_one_hot(class_name, num_class)
        one_hot_classes.append(one_hot_class)
    image_name = root.find('filename').text
    bounding_boxes = np.asarray(bounding_boxes)
    one_hot_classes = np.asarray(one_hot_classes)
    image_data = np.hstack((bounding_boxes, one_hot_classes))

    return image_name, image_data


def _to_one_hot(name, num_classes):
    one_hot_vector = [0] * num_classes
    if name == 'A':
        one_hot_vector[0] = 1
    elif name == 'B':
        one_hot_vector[1] = 1
    elif name == 'E':
        one_hot_vector[2] = 1
    elif name == 'G':
        one_hot_vector[3] = 1
    else:
        print('unknown label: %s' %name)

    return one_hot_vector
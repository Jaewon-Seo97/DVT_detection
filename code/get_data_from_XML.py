import numpy as np
import os
from xml.etree import ElementTree


def get_category(category_file):
    class_list = []
    with open(category_file, 'r') as f:
        for line in f.readlines():
            class_list.append(line.rstrip('\n'))

    return class_list


class XML_preprocessor(object):

    def __init__(self, data_path, num_classes, normalize=False):
        self.path_prefix = data_path
        self.num_classes = num_classes
        self.normalization = normalize
        self.data = dict()
        self._preprocess_XML()

    def _preprocess_XML(self):
        filenames = os.listdir(self.path_prefix)
        for filename in filenames:
            tree = ElementTree.parse(os.path.join(self.path_prefix, filename))
            root = tree.getroot()
            bounding_boxes = []
            one_hot_classes = []
            size_tree = root.find('size')
            width = float(size_tree.find('width').text)
            height = float(size_tree.find('height').text)
            for object_tree in root.findall('object'):
                for bounding_box in object_tree.iter('bndbox'):
                    if self.normalization:
                        xmin = float(bounding_box.find('xmin').text)/width
                        ymin = float(bounding_box.find('ymin').text)/height
                        xmax = float(bounding_box.find('xmax').text)/width
                        ymax = float(bounding_box.find('ymax').text)/height
                    else:
                        xmin = float(bounding_box.find('xmin').text)
                        ymin = float(bounding_box.find('ymin').text)
                        xmax = float(bounding_box.find('xmax').text)
                        ymax = float(bounding_box.find('ymax').text)
                bounding_box = [xmin,ymin,xmax,ymax]
                bounding_boxes.append(bounding_box)
                class_name = object_tree.find('name').text
                one_hot_class = self._to_one_hot(class_name)
                one_hot_classes.append(one_hot_class)
            # image_name = root.find('filename').text
            image_name = filename
            bounding_boxes = np.asarray(bounding_boxes)
            one_hot_classes = np.asarray(one_hot_classes)
            image_data = np.hstack((bounding_boxes, one_hot_classes))
            self.data[image_name] = image_data

    def _to_one_hot(self, name):
        one_hot_vector = [0] * self.num_classes
        if name == 'A' or name == 'a':
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


## example on how to use it
# import pickle
# data = XML_preprocessor('VOC2007/Annotations/').data
# pickle.dump(data,open('VOC2007.p','wb'))
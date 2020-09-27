from utils import *
import os, glob

# path = 'Data/02-06-2020/DICOM/Lung_Dx-G0011'
# path = '/home/wangshuo/Desktop/test_data/Lung-PET-CT-Dx/G0011'
# path = 'Data/02-06-2020/DICOM/Lung_Dx-G0011/04-29-2009-LUNGC-51228/2.000000-A phase 5mm Stnd SS50-53792/2-017.dcm'


def getUID_path(path):
    dict = {}
    list = os.listdir(path)

    for date in list:
        date_path = os.path.join(path, date)
        series_list = os.listdir(date_path)
        series_list.sort()

        for series in series_list:
            series_path = os.path.join(date_path, series)
            dicom_list = os.listdir(series_path)
#             dicom_list = glob.glob(series_path, '/*.dcm')
            dicom_list.sort()

            for dicom in dicom_list:
                dicom_path = os.path.join(series_path, dicom)
                info = loadFileInformation(dicom_path)
                dict[info['dicom_num']] = (dicom_path, dicom)

    return dict


def getUID_file(path):
    info = loadFileInformation(path)
    UID = info['dicom_num']
    return UID

# dict = getUID_file(path)
# print(dict)
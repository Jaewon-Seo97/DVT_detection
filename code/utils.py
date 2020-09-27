import os
import cv2
import numpy as np
import pydicom as dicomio 
import SimpleITK as sitk
from PIL import Image


def loadlist(path): # 경로 내 파일 리스트 정렬 후 목록 반환
    list = os.listdir(path)
    list.sort()
    return list


def loadFile(filename): #함수 이름이 loadFile
    ds = sitk.ReadImage(filename) # 파일에서 이미지를 읽어 저장된게 ds
    img_array = sitk.GetArrayFromImage(ds) #ds에서 배열 뽑아낸게 img_arr
    if len(img_array.shape) == 3: #만약 img_array가 행이 3이면
        frame_num, width, height = img_array.shape # frame_num, width, height가 img_array의 행,열,깊이 값을 갖음
        ch = 1
        return img_array, frame_num, width, height, ch #각 값을 리턴
    elif len(img_array.shape) == 4: #만약 행수가 4라면
        frame_num, width, height, ch = img_array.shape # ch이 마지막 값을 갖음
        return img_array, frame_num, width, height, ch # 각 값을 리턴


def loadFileInformation(filename): # 파일의 정보를 불러오는 함수
    information = {}
    ds = dicomio.read_file(filename, force=True) #다이콤 파일 읽어서 ds에 저장(False (기본값) 인 경우 파일에 File Meta Information 헤더가없는 경우 InvalidDicomError가 발생합니다. 파일 메타 정보 헤더가없는 경우에도 강제로 읽으려면 True로 설정하십시오.)
    information['dicom_num'] = ds.SOPInstanceUID #information의 'dicom_num' 값을 ds.SOPInstanceUID(다이콤 파일 내 식별자)로 지정
    # information['PatientID'] = ds.PatientID
    # information['PatientName'] = ds.PatientName
    # information['PatientBirthDate'] = ds.PatientBirthDate
    # information['PatientSex'] = ds.PatientSex
    # information['StudyID'] = ds.StudyID
    # information['StudyDate'] = ds.StudyDate
    # information['StudyTime'] = ds.StudyTime
    # information['InstitutionName'] = ds.InstitutionName
    # information['Manufacturer'] = ds.Manufacturer
    # information['NumberOfFrames'] = ds.NumberOfFrames
    return information #위의 값을 집합한 값으로 리턴 


def showImage(img_array):  #Numpy 배열(이미지 넘파이 배열)을 이미지로 바꿔줌
    img_array = img_array
    img_bitmap = Image.fromarray(img_array) #fronarry는 Numpy배열을 '이미지'로 
    # img_bitmap.show()
    return img_bitmap


def MatrixToImage(data, ch):
    # data = (data+1024)*0.125
    # new_im = Image.fromarray(data.astype(np.uint8))
    # new_im.show()
    if ch == 3: #img_array의 요소 중 ch값이 3일 때
        img_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)  # PIL 패키지는 RGB 사용, OpenCV 는 BGR (즉, BGR  -> RGB하는 코드) 따라서 data를 RGB로 바꾼값을 img_rgb에 저장 
    if ch == 1: #img_array의 요소 중 ch값이 1일 때
        data = (data + 1024) * 0.125 # 모르겠음: 그떄 스케일을 바꿔준다는 말씀을 들었던 것같으나 잘 모으겠음 + ch이 뭘 의미하는지 모르겠음
        img_rgb = data.astype(np.uint8) # 8비트 이미지로 바꿔줌 (그리 큰값이 필요하지 않기때문이라고 들었는데 맞는건지 모르겠음)
        return img_rgb #변환된 값으로 반환

def PETToImage(img_array, color_reversed=True):
    info = np.finfo(img_array.dtype)
    data = img_array.astype(np.float64) / np.max(img_array)
    if color_reversed is True:
        data = 255 - 255 * data
    elif color_reversed is False:
        data = 255 * data
    # data = (data + 1024) * 0.125
    img = data.astype(np.uint8)
    img = np.transpose(img, (1, 2, 0))
    # cv2.imshow('test', img)
    return img


def dfs_showdir(path, depth):
    if depth == 0:
        print("root:[" + path + "]")

    for item in os.listdir(path):
        if '.git' not in item:
            print("|      " * depth + "+--" + item)

            newitem = path +'/'+ item
            if os.path.isdir(newitem):
                dfs_showdir(newitem, depth +1)
    # print(path_list)


def isdir(x):
    return os.path.isdir(x) and x != '.svn'


def mkfloders(src,tar):
    paths = os.listdir(src)
    paths = map(lambda name:os.path.join(src, name), paths)
    paths = list(filter(isdir, paths))
    if(len(paths)<=0):
        return
    for i in paths:
        (filepath, filename)=os.path.split(i)
        targetpath = os.path.join(tar,filename)
        not os.path.isdir(targetpath) and os.mkdir(targetpath)
        mkfloders(i,targetpath)


def mkdir(path):

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print(path + ' successfully be made!')
        return True
    else:
        print(path + ' the folder already existed!')
        return False
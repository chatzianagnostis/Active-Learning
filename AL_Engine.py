import os, glob, random, shutil
from pathlib import Path
from declarations import declarations_instance


def DUA(fDir):

    '''
    This function calculates the Diversity in Uncertainty Aggregation (DUA) for a given directory fDir. 
    It reads the annotations from a file, calculates the uncertainty for each class, aggregates them, 
    and returns the weighted average uncertainty.
    '''
    classes = {}
    object_def = declarations_instance.get_object_def()

    for i in range(len(object_def)):
        classes[str(i)] = {'objectsC' : 0, 'uncer' : 0}
    try:
        with open(fDir, 'r') as file2:  # read annotation.txt
            for row in [x.split(' ') for x in file2.read().strip().splitlines()]:
                classes[str(row[0])]['objectsC'] += 1
                classes[str(row[0])]['uncer'] += ((1-float(row[5])))
        file2.close()
        total = 0
        wAvg = 0
        for i in range(len(object_def)):
            # print(classes[str(i)])
            if classes[str(i)]['objectsC'] != 0:
                wAvg += ((classes[str(i)]['uncer']/classes[str(i)]['objectsC']) * classesWeight[str(i)])
                total += classes[str(i)]['objectsC']

        return(wAvg)
    except (IOError, OSError) as e:
        print(e)
        return(0)


def getUncertinitiesForDir(dir, trainDir = [], valAccuracyDirF = '', method = 'avg', weighting = 1 , budget = 100):

    ''' 
    This function computes the uncertainties for a given directory of labels (dir). It supports different uncertainty 
    aggregation methods such as DUA and takes into account class weighting and budget constraints.
    '''

    classesWeight = getWeightsForClassses(weighting, trainDir = trainDir, valAccuracyDirF = valAccuracyDirF)
    listofFilesNamesUncertinity = {}
    for f in glob.glob(dir+'/labels/*.txt'):
        namef = Path(f).name[:-4]
        fileFullDir = dir+'/labels/'+namef+'.txt'
        if method == 'DUA':
            listofFilesNamesUncertinity[namef] = DUA(fileFullDir,classesWeight)
    print(listofFilesNamesUncertinity)
    return sorted(listofFilesNamesUncertinity, key=listofFilesNamesUncertinity.get, reverse=True)[:budget]


def getWeightsForClassses(weighting, trainDir = [], valAccuracyDirF = '', ):

    '''
    This function calculates weights for classes based on the chosen weighting method. 
    It supports two weighting methods: assigning equal weights to all classes or using weights based on validation accuracy.
    '''
    object_def = declarations_instance.get_object_def()
    classesWeight = {}
    if weighting == 1:
        for i in range(len(object_def)):
            classesWeight[str(i)] = 1
    elif weighting == 3:
        classesWeight = applyMinMaxScalerToW(getWeightForValAccuracy(valAccuracyDirF))
    print(classesWeight)
    return classesWeight


def newTraining(namefolder,setOfFileNames,oldTraning):

    '''
    This function performs new training by copying selected images and their corresponding labels from the previous training set 
    and a set of newly selected images (setOfFileNames) to a new training directory.
    '''
    complete_data_folder = declarations_instance.get_complete_data_folder()
    complete_iteration_folder = declarations_instance.get_complete_iteration_folder()
    budgetPerIteration = declarations_instance.get_budgetPerIteration()
    main_dir = declarations_instance.get_main_dir()
    main_exp_dir = declarations_instance.get_main_exp_dir()
    previous_iteration_folder = declarations_instance.get_previous_iteration_folder()
    previousExpfName = declarations_instance.get_previousExpfName()

    added = 0
    path_label_2 = complete_iteration_folder+namefolder+'/labels/'
    path_images_2 = complete_iteration_folder+namefolder+'/images/'
    os.makedirs(path_label_2) if not os.path.exists(path_label_2) else None
    os.makedirs(path_images_2) if not os.path.exists(path_images_2) else None
    count = 0

    while (added < budgetPerIteration) and (count < len(setOfFileNames)):
        namef = setOfFileNames[count] #Path(setOfFileNames[count]).name[:-4]

        l_src_path = complete_data_folder+'labels/'+ namef+'.txt'
        i_src_path = complete_data_folder+'images/'+ namef+'.png'

        src_path = complete_data_folder+'labels/'+ namef+'.txt'
        if os.path.exists(l_src_path) and os.path.exists(i_src_path):
            dst_path = path_label_2 + namef+'.txt'
            shutil.copy(src_path, dst_path)
            src_path = complete_data_folder+'images/'+ namef+'.png'
            dst_path = path_images_2 + namef+'.png'
            shutil.copy(src_path, dst_path)
            added += 1
        count += 1

    for pth in oldTraning:
        # print(pth)
        namef = Path(pth).name[:-4]
        src_path = main_dir+main_exp_dir+previous_iteration_folder+previousExpfName+'labels/'+ namef+'.txt'
        dst_path = path_label_2 + namef+'.txt'
        shutil.copy(src_path, dst_path)

        src_path = main_dir+main_exp_dir+previous_iteration_folder+previousExpfName+'images/'+ namef+'.png'
        dst_path = path_images_2 + namef+'.png'
        shutil.copy(src_path, dst_path)


def getWeightForValAccuracy(fDir, cnum = declarations_instance.get_object_def()):

    '''
    This function calculates weights for classes based on validation accuracy. It reads validation accuracy data 
    from a file and assigns weights to classes based on their performance.
    '''
    object_def = declarations_instance.get_object_def()
    numberOfClasses = len(object_def)
    accuracyClasses = {}
    for i in range(numberOfClasses):
        accuracyClasses[str(i)] = 0
    try:
        with open(fDir, 'r') as file2:  # read annotation.txt
            first = True
            for row in [x.split(' ') for x in file2.read().strip().splitlines()]:
                if first:
                    first = False
                    continue
                if row == '':
                    continue
                row = list(filter(lambda a: a != '', row))
                accuracyClasses[str(cnum[row[0]])] = float(row[5])


        file2.close()
        return(accuracyClasses)
    except (IOError, OSError) as e:
        print(e)


def applyMinMaxScalerToW (wValCDic):

    '''
    This function applies min-max scaling to the weights calculated based on validation accuracy 
    to normalize them between 0 and 1.
    '''
    object_def = declarations_instance.get_object_def()
    minV = min(wValCDic[item] for item in wValCDic)
    maxV = max(wValCDic[item] for item in wValCDic)
    for i in range(len(object_def)):
        wValCDic[str(i)] = 1- ((wValCDic[str(i)] - minV)/(maxV - minV))
    return wValCDic


def nominateImagesToObtainUncer(wasTrainedOnDir, experimentName, forWeights = False, fromRandSize = 500, seed = 42, trainingDir = declarations_instance.get_complete_data_folder()+'images/', weightedOnDir = '' ):
    
    '''
    This function selects images from the training set that were not used in previous training iterations, 
    optionally weighted based on previous experiments or validation accuracy. 
    It creates a new directory containing the selected images for further processing.
    '''
    complete_data_folder = declarations_instance.get_complete_data_folder()
    complete_iteration_folder = declarations_instance.get_complete_iteration_folder()

    #remove images that were trained on
    trainedOn = glob.glob(wasTrainedOnDir+'images/*.png')
    print(len(trainedOn))
    fullTrainSet = glob.glob(trainingDir+'*.png')
    orpNames = [Path(f).name[:-4] for f in trainedOn]
    if weightedOnDir != '':
        weightedOn = glob.glob(weightedOnDir+'/images/*.png')
        orpNames = orpNames + [Path(f).name[:-4] for f in weightedOn]

    mixedRand = []
    for ele in fullTrainSet:
        for ele2 in orpNames:
            if ele2 in ele:
                mixedRand.append(ele)
                continue
    randomPathes2 = [ele for ele in fullTrainSet if ele not in mixedRand]

    reducedRandomPathes2 = []
    for rp2 in randomPathes2:
        if os.path.exists(complete_data_folder+'labels/'+ Path(rp2).name[:-4] + '.txt'):
            reducedRandomPathes2.append(rp2)
    toGetUncertinityPath = reducedRandomPathes2
    print(len(toGetUncertinityPath))
    if fromRandSize < len(toGetUncertinityPath):
        toGetUncertinityPath = random.sample(reducedRandomPathes2, k=fromRandSize)
    print(len(toGetUncertinityPath))

    newFolderName = experimentName+'_Nominees'
    path_label = complete_iteration_folder+newFolderName+'/labels/'
    path_images = complete_iteration_folder+newFolderName+'/images/'
    os.makedirs(path_label) if not os.path.exists(path_label) else None
    os.makedirs(path_images) if not os.path.exists(path_images) else None

    for pth in toGetUncertinityPath:
        namef = Path(pth).name[:-4]
        if forWeights:
            src_path = complete_data_folder+'/labels/'+ namef+'.txt'
            dst_path = path_label + namef+'.txt'
            shutil.copy(src_path, dst_path)
        src_path = complete_data_folder+'/images/'+ namef+'.png'
        dst_path = path_images + namef+'.png'
        shutil.copy(src_path, dst_path)
    return path_images
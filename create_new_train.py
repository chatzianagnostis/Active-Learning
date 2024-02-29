import argparse
import glob, shutil
from pathlib import Path

from AL_Engine import getUncertinitiesForDir, newTraining
from declarations import declarations_instance


def main(predFile, wafile):
    main_dir = declarations_instance.get_main_dir()
    main_exp_dir = declarations_instance.get_main_exp_dir()
    complete_iteration_folder = declarations_instance.get_complete_iteration_folder()
    previous_iteration_folder = declarations_instance.get_previous_iteration_folder()
    previousExpfName = declarations_instance.get_previousExpfName()
    iteration = declarations_instance.get_iteration()
    approach = declarations_instance.get_approach()
    weighting_approach = declarations_instance.get_weighting_approach()
    number_of_random_images_from_training = declarations_instance.get_number_of_random_images_from_training()
    wexpName = declarations_instance.get_wexpName()

    expfName = 'iteration'+str(iteration)+approach+weighting_approach+'_'+str(number_of_random_images_from_training)
    print (expfName)
    previousFileList = glob.glob(main_dir+main_exp_dir+previous_iteration_folder+previousExpfName+'labels/*.txt')
    trainOnDUA = getUncertinitiesForDir(predFile, valAccuracyDirF =wafile, method='DUA',budget = int(500),weighting = 3,)
    newTraining(expfName,trainOnDUA,previousFileList)

    path_label = complete_iteration_folder+expfName+'/labels/'
    path_images = complete_iteration_folder+expfName+'/images/'

    wimg = glob.glob(complete_iteration_folder+wexpName+'_Nominees/images/*')
    wtxt = glob.glob(complete_iteration_folder+wexpName+'_Nominees/labels/*')
    for pth in wtxt:
        namef = Path(pth).name[:-4]
        src_path = complete_iteration_folder+wexpName+'_Nominees/labels/'+ namef+'.txt'
        dst_path = path_label + namef+'.txt'
        shutil.copy(src_path, dst_path)
    for pth in wimg:
        namef = Path(pth).name[:-4]
        src_path = complete_iteration_folder+wexpName+'_Nominees/images/'+ namef+'.png'
        dst_path = path_images + namef+'.png'
        shutil.copy(src_path, dst_path)


if __name__=='__main__':
    parser = argparse.ArgumentParser()

    # Add arguments for predFile and wafile
    parser.add_argument('--predfile', help='This is the path to the directory where the predictions from the model are stored.')
    parser.add_argument('--wafile', help='This is the path to the file that contains the results of the validation.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.predfile, args.wafile)
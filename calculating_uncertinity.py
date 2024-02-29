from AL_Engine import nominateImagesToObtainUncer
from declarations import declarations_instance

def main():

    main_dir = declarations_instance.get_main_dir()
    main_exp_dir = declarations_instance.get_main_exp_dir()
    previous_iteration_folder = declarations_instance.get_previous_iteration_folder()
    previousExpfName = declarations_instance.get_previousExpfName()
    expName = declarations_instance.get_expName()
    number_of_random_images_from_training = declarations_instance.get_number_of_random_images_from_training()
    
    path_images_nominees = nominateImagesToObtainUncer(main_dir+main_exp_dir+previous_iteration_folder+previousExpfName,expName, fromRandSize = number_of_random_images_from_training)
    print(path_images_nominees)


if __name__ == '__main__':
    main()
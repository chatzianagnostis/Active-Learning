from AL_Engine import nominateImagesToObtainUncer
from declarations import declarations_instance

def main():

    main_dir = declarations_instance.get_main_dir()
    main_exp_dir = declarations_instance.get_main_exp_dir()
    previous_iteration_folder = declarations_instance.get_previous_iteration_folder()
    previousExpfName = declarations_instance.get_previousExpfName()
    wexpName = declarations_instance.get_wexpName()
    budgetPerIteration = declarations_instance.get_budgetPerIteration()
    
    path_images_nominees_test = nominateImagesToObtainUncer(main_dir+main_exp_dir+previous_iteration_folder+previousExpfName,wexpName,fromRandSize=int(budgetPerIteration*0.1),forWeights=True)
    print(path_images_nominees_test)


if __name__ == '__main__':
    main()
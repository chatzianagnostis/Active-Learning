import os

class Declarations:
    def __init__(self):
        self.iteration = 1 # Important: Increase the itereation after completing each iteration
        self.main_dir = 'path' # This is the main directory where your dataset is located.
        self.complete_data_folder = self.main_dir + 'TrainF/'
        self.main_exp_dir = 'DUA500/'
        self.iteration_folder = f'Iteration_{self.iteration}/'
        self.complete_iteration_folder = self.main_dir + self.main_exp_dir + self.iteration_folder
        os.makedirs(self.complete_iteration_folder, exist_ok=True)
        self.object_def = {'item0': 0, 'item1': 1, 'item2': 2, 'item3': 3, 'item4': 4, 'item5': 5} # This is a dictionary that maps the names of the object classes to their corresponding integer labels.
        self.approach = 'DUA'
        self.weighting_approach = 'WRP'
        self.number_of_random_images_from_training = 5000
        self.output_model = f'{self.approach}{self.iteration}{self.number_of_random_images_from_training}{self.weighting_approach}'
        self.previous_model_zip = f'Iteration_{self.iteration - 1}_Training_whole_best.pt'
        self.budgetPerIteration = 500
        self.expName = f'iteration{self.iteration}{self.approach}_{self.number_of_random_images_from_training}'
        self.wexpName = f'w_iteration{self.iteration}{self.approach}_{self.number_of_random_images_from_training}'
        self.previousExpfName = f'iteration{self.iteration - 1}{self.approach}{self.weighting_approach}_{self.number_of_random_images_from_training}/'
        self.previous_iteration_folder = f'Iteration_{self.iteration - 1}/'

    def get_iteration(self):
        return self.iteration

    def get_main_dir(self):
        return self.main_dir

    def get_complete_data_folder(self):
        return self.complete_data_folder

    def get_main_exp_dir(self):
        return self.main_exp_dir

    def get_iteration_folder(self):
        return self.iteration_folder

    def get_complete_iteration_folder(self):
        return self.complete_iteration_folder

    def get_object_def(self):
        return self.object_def

    def get_approach(self):
        return self.approach

    def get_weighting_approach(self):
        return self.weighting_approach

    def get_number_of_random_images_from_training(self):
        return self.number_of_random_images_from_training

    def get_output_model(self):
        return self.output_model

    def get_previous_model_zip(self):
        return self.previous_model_zip

    def get_budgetPerIteration(self):
        return self.budgetPerIteration

    def get_expName(self):
        return self.expName

    def get_wexpName(self):
        return self.wexpName

    def get_previousExpfName(self):
        return self.previousExpfName

    def get_previous_iteration_folder(self):
        return self.previous_iteration_folder

# Instantiate the class to make the variables accessible
declarations_instance = Declarations()

# Active-Learning
This repository contains code that implements [DUA](https://github.com/asmayamani/DUA) as described in the [paper](https://openaccess.thecvf.com/content/WACV2024/papers/Yamani_Active_Learning_for_Single-Stage_Object_Detection_in_UAV_Images_WACV_2024_paper.pdf). 

## Introduction
This project aims to provide a clearer and more distinct set of steps for DUA Active Learning. The goal of the project is to improve the performance of the model with a limited annotation budget by iteratively selecting the most informative images for training.

## Project Fit
This project is suitable for projects that involve:

- Object detection using single-stage models
- Dealing with unbalanced datasets
- Working with multi-labeled images

## High Level Workflow
1. **Random Subset Creation**: A random subset of images is selected from the training set using the `create_random_subset.py` script.

2. **Model Testing**: The model is tested on the selected subset using the `test.py` script. The model’s predictions are saved, and the performance of the model is evaluated.

3. **Uncertainty Calculation**: The uncertainties of the model’s predictions are calculated using the `calculating_uncertinity.py` script. Images with the highest uncertainties are considered the most informative.

4. **Image Nomination**: The most informative images are nominated for the next training iteration using the `detect.py` script.

5. **New Training Set Creation**: A new training set is created for the next iteration using the `create_new_train.py` script. This new training set includes the images from the previous training set and the nominated images.

6. **Iteration**: Steps 2-5 are repeated for a specified number of iterations. With each iteration, the model is trained on an increasingly informative set of images, which improves its performance.

## Usage
To use this code, follow these steps:

0. Clone the repository:

   ```bash
   git clone https://github.com/chatzianagnostis/Active-Learning.git
   cd Active-Learning

## Acknowledgements
We would like to thank the authors of the referenced paper for their valuable contributions.

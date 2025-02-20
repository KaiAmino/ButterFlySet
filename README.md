# ButterFlySet

This repository provides the dataset ButterFlySet, the first video dataset of flying butterflies and the largest dataset for insect pose estimation recorded in the wild, containing 7440 frames with nine key points annotation.


## Download

| Data | Size | Download (zip) |
| :---: | :---: | :---: |
| json | 15.9 MB | [GoogleDrive](https://drive.google.com/drive/folders/1hnuOXGnViC3GLgfz2ndvaQJyCDpdqXSr?usp=share_link) |
| original frames (.jpg) | 3.8 GB | [GoogleDrive](https://drive.google.com/drive/folders/1pvHIArTxYaDH7CTkW9TaqXSxqZrygqhi?usp=share_link) |
| annotated frames (.jpg) | 5.3 GB | [GoogleDrive](https://drive.google.com/drive/folders/1axcFOQKBO7f72v7qjN5oD7VlWOoLU2LM?usp=share_link) |


## How to Use

1. Download at least json and original frames from the GoogleDrive above.

2. Run `python json2h5.py` from the directory where the script is located. The new directory (default name is 'data_train') will be generated which contains .h5 and .csv files. To run this code, you need to install the required packages necessary for DeepLabCut.

The following options are required:
- `-json` specifies the name and location of the directory containing the scenes you are importing to the dataset. The default is set to `'jsons'`. If you want to create a new dataset based on part of the original dataset, it is recommended to modify the contents of the 'jsons' directory.
- `-name` specifies the name of your new dataset. Default is set to `'data_train'`.
- `-user` specifies your name. To match the project owner name in DeepLabCut, it is preferable to use your initials (e.g., Taro Yamada → 'TY').

3. The 'dataset' directory can be directory used for the pose estimation with DeepLabCut and SLEAP.

4. If you want to create the video for the initialization of DeepLabCut, select `-mkvideo` option as `True`. `-fps` also specifies the frames/second of the videos to be created (Default is set to 60).


## Acknowledgements
We thank T. Suzuki for assistance in finding sites for video recording. We also thank N. Nishiumi for help in designing the setup for recording.

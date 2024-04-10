# 2023 ASNR AI workshop - Data annotation and curation

# 3D Slicer

## 3D-Slicer customized GUI for annotations (BraTS semantic segmentation)

<p align="center">
  <img src="https://github.com/laurentletg/2023_ASNR_AI_workshop_curation/blob/main/readme%20image%20asnr%20ai%20workshop.png" />
</p>


## Installing Slicer and the BraTS_annotation module (work-in-progress)
1. [Download 3D slicer](https://download.slicer.org)
2. Enable developer mode (Edit > Application Settings > Developer > Check Enable developer mode). Slicer will restart. 
3. Clone (or download) this repository
4. Load custom module (Edit > Application Settings > Modules > Additional modules paths > (right-sided arrows) Add > add the directory containing the .py file (BraTS_annotation.py). Slicer will restart.
5. If the module appears in red, this is typically because there is a bug in the .py file. You can check for a traceback in the python console embeded in 3D Slicer (will give you the code line and error). 
6. Potential issue with Qt (3D Slicer splash screen appears and disappears, fail to load) : this happens if Qt is not installed on your system (e.g on a new Linux install) : example of Qt [install on Ubuntu](https://wiki.qt.io/Install_Qt_5_on_Ubuntu) 


## Official Slicer ressources
- [Main page](https://www.slicer.org)
- [Download page](https://download.slicer.org)
- [Documentation](https://slicer.readthedocs.io/en/latest/)
- [Developer guide](https://slicer.readthedocs.io/en/latest/developer_guide/index.html)
- [Slicer API (C++)](https://apidocs.slicer.org/main/)

## Python programing in Slicer
- [Slicer Programming Tutorial](https://spujol.github.io/SlicerProgrammingTutorial/)
- [Beyond the basics programming](https://www.slicer.org/w/img_auth.php/7/79/SlicerModulesProgrammingBeyondBasics.pdf)
- [Python script repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)

## Slicer Jupyter
Useful for prototyping and exploring the python API
- [Overview on github](https://github.com/Slicer/SlicerJupyter)
- [Jupyter notebook examples](https://github.com/Slicer/SlicerNotebooks)
- [Other segmentation examples](https://gist.github.com/lassoan)

## Slicer module development 
In order of difficulty/complexity:
- [Basic Python module (Hello python)](https://www.slicer.org/w/img_auth.php/c/c0/Slicer4_ProgrammingTutorial_Slicer4.5.pdf)
- [Robarts lab documentation](https://www.robarts.ca/computerassistedsurgery/create_your_own/index.html) including well documented [example](https://github.com/lgroves6/SlicerIGTDevelopment/blob/master/YourModuleName.py) 
- [PerkLab python module development tutorial (includes Qt designer)](https://www.slicer.org/wiki/Documentation/Nightly/Training#Tutorials_for_software_developers)
- [Developing and contributing extensions for 3D Slicer](https://docs.google.com/presentation/d/1JXIfs0rAM7DwZAho57Jqz14MRn2BIMrjB17Uj_7Yztc/edit#slide=id.g41f90baec_028)

## Videos and other ressources
- [Module development series](https://www.youtube.com/@3dslicertutorial)
- [Short series showing basic python programming and module development (in German with English subtitles)](https://youtube.com/playlist?list=PLJWCUXz3GeAfmYLiFcKus_c0jcsMnVsgb)

## Python module examples
- [Robarts lab good baseline code (without .ui file - requires manually editing the widgets in the .py file)](https://github.com/lgroves6/SlicerIGTDevelopment/blob/master/YourModuleName.py)
- [Slicer Case Iterator](https://github.com/JoostJM/SlicerCaseIterator): iterate through cases 

## PyQt
Building a GUI outside of Slicer (helps to understand how to build a GUI in Slicer)
- [PyQt tutorial](https://realpython.com/python-pyqt-gui-calculator/)
- [PyQt video series](https://youtu.be/Vde5SH8e1OQ)

# Converting nifti files to numpy arrays
Notebook describing basic nifti file reading and visualisation. <br />
This is the transition point between data annotation/curation and building a model. <br />

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zq2zceI3jvngKKagyv57evBfHR5PXPBh?usp=sharing)

# Misc ressources
## MONAI label (3D Slicer extension)
Active learning tool - DL assited annotation.
- [MONAI label](https://monai.io/label.html). 
- [MONAI label youtube - Overview](https://youtu.be/KjwuFx0pTXU)
- [MONAI label youtube - Set-up](https://youtu.be/8y1OBQs2wis)
- [MONAI label github](https://github.com/Project-MONAI/MONAILabel)

## Git
- [Getting started with Git](https://swcarpentry.github.io/git-novice/)






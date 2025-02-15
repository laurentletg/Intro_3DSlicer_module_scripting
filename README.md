# Introduction to 3D Slicer module creation

# 3D Slicer

## 3D-Slicer customized GUI for annotations (BraTS semantic segmentation)

<p align="center">
  <img src="https://github.com/laurentletg/Intro_3DSlicer_module_scripting/blob/main/readme%20image%20asnr%20ai%20workshop.png" />
</p>


## Installing Slicer and the BraTS_annotation module (work-in-progress)
1. [Download 3D slicer](https://download.slicer.org)
2. Enable developer mode (Edit > Application Settings > Developer > Check Enable developer mode). Slicer will restart. 
3. Clone (or download) this repository
4. Activate the checkbox `Enable developer mode` in `Edit -> Application Settings -> Developer -> Enable developer mode`. 
6. Add the path of this repository in `Edit -> Application Settings -> Modules -> Additional module paths`. Slicer must be restarted.
7. If the module appears in red, this is typically because there is a bug in the .py file. You can check for a traceback in the python console embeded in 3D Slicer. 
8. Potential issue with Qt (3D Slicer splash screen appears and disappears, fail to load) : this happens if Qt is not installed on your system (e.g on a new Linux install) : example of Qt [install on Ubuntu](https://wiki.qt.io/Install_Qt_5_on_Ubuntu) 


## Official Slicer ressources
- [Main page](https://www.slicer.org)
- [Download page](https://download.slicer.org)
- [Documentation](https://slicer.readthedocs.io/en/latest/)
- [Developer guide](https://slicer.readthedocs.io/en/latest/developer_guide/index.html)
- [Discourse](https://discourse.slicer.org)

## Python programing in Slicer
> The Slicer python API is not fully documented but slowly improving [including here](https://slicer.readthedocs.io/en/latest/developer_guide/modules/index.html). I usually try first with the [script repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html) or [discourse forum](https://discourse.slicer.org). For the segmentation editor module you can find methods in this [page](https://slicer.readthedocs.io/en/latest/developer_guide/modules/segmenteditor.html). Trying to find methods using *tab completion* sometimes work in combination with the [official C++ API](https://apidocs.slicer.org/main/). A [debugging tool](https://github.com/SlicerRt/SlicerDebuggingTools) exists, I was only able to make it work with VSCode not PyCharm.  ChatGPT is hit or miss, sometimes come up with hallucinated functions. 
- [Slicer Programming Tutorial](https://spujol.github.io/SlicerProgrammingTutorial/)
- [Beyond the basics programming](https://www.slicer.org/w/img_auth.php/7/79/SlicerModulesProgrammingBeyondBasics.pdf)
- [Python script repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
- [Script repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
- [Slicer API (C++)](https://apidocs.slicer.org/main/)


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
- - [GitHub page](https://github.com/SenonETS/3DSlicerTutorial_ExtensionModuleDevelopment.git)
- [Short series showing basic python programming and module development (in German with English subtitles)](https://youtube.com/playlist?list=PLJWCUXz3GeAfmYLiFcKus_c0jcsMnVsgb)

## Python module examples
- [Robarts lab good baseline code (without .ui file - requires manually editing the widgets in the .py file)](https://github.com/lgroves6/SlicerIGTDevelopment/blob/master/YourModuleName.py)
- [Slicer Case Iterator](https://github.com/JoostJM/SlicerCaseIterator): iterate through cases 

## PyQt
Building a GUI outside of Slicer (helps to understand how to build a GUI in Slicer)
- [PyQt tutorial](https://realpython.com/python-pyqt-gui-calculator/)
- [PyQt video series](https://youtu.be/Vde5SH8e1OQ)

# Misc ressources
## MONAI label (3D Slicer extension)
Active learning tool - DL assited annotation.
- [MONAI label](https://monai.io/label.html). 
- [MONAI label youtube - Overview](https://youtu.be/KjwuFx0pTXU)
- [MONAI label youtube - Set-up](https://youtu.be/8y1OBQs2wis)
- [MONAI label github](https://github.com/Project-MONAI/MONAILabel)








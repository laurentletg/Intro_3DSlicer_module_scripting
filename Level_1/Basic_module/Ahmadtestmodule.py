import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import pandas as pd
import json

#
# Ahmadtestmodule
#

class Ahmadtestmodule(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Ahmadtestmodule"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#Ahmadtestmodule">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

    # Additional initialization step after application startup is complete
    #slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#



class AhmadtestmoduleWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self.getParameterNode = None
    self._updatingGUIFromParameterNode = False
    #instantiate an empty hematoma
    self.dicthematoma = {}
    self.volume = None
    self.currentIDx = None
    

  def setup(self):
    # this is the function that implements all GUI 
    ScriptedLoadableModuleWidget.setup(self)
    # This sets the view being used to the red view only 
    slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #Section 3.2.1: Ultrasound connection ang widgets
    #the following code provides a GUI to connect to an external ultrasound scanner throught the PlusServer
    #this section also provides examples of other widgets that can be used 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 
       
    ##################################################################################################################
    #This section creates all the widgets
    #This is where you will create the type of widget and how it will show up 
    ##################################################################################################################
    # Parameters Area
    #Create collapsible button
    self.parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    self.parametersCollapsibleButton.text = "Main collabpsilbe button"



    #### MAIN WIDGETS ARE DESCRIBED BELOW ### 

    # GET THE PATH USING LINE EDIT
    self.inputIPLineEdit = qt.QLineEdit()
    #This sets a placehoder example of what should be inputted to the line edit 
    self.inputIPLineEdit.setPlaceholderText("/Users/laurentletourneau-guillon/Dropbox (Personal)/CHUM/RECHERCHE/2020ICHHEMATOMAS/2021 Kappa Ahmad/2021_11_28 Localisation hematomas/All path cases.csv")
    #This is the help tooltip 
    self.inputIPLineEdit.toolTip = "Put the path to .csv file containing volume paths"
    # New layout for collapsible button


    # LOAD CSV BUTTON
    #This is a push button 
    self.loadcsv = qt.QPushButton()
    self.loadcsv.setDefault(False)
    #This button says connect 
    self.loadcsv.text = "Load csv"
    #help tooltip that explains the funciton 
    self.loadcsv.toolTip = "Loads csv"
    #adds the widget to the layout 

    # LOAD NEW (NEXT) CASE BUTTON
    #This is a push button 
    self.nextButton = qt.QPushButton()
    self.nextButton.setDefault(False)
    #This button says connect 
    self.nextButton.text = "New case"
    #help tooltip that explains the funciton 
    self.nextButton.toolTip = "Loads a new case"
    #adds the widget to the layout 

    # LOAD PREVIOUS CASE BUTTON
    #This is a push button 
    self.previousButton = qt.QPushButton()
    self.previousButton.setDefault(False)
    #This button says connect 
    self.previousButton.text = "Previous case"
    #help tooltip that explains the funciton 
    self.previousButton.toolTip = "Loads the previous case"
    #adds the widget to the layout 


    # Windowing button
    self.windowButton = qt.QPushButton()
    self.windowButton.setDefault(False)
    #This button says connect 
    self.windowButton.text = "Change window level"
    #help tooltip that explains the funciton 
    self.windowButton.toolTip = "Change WM WL"
    #adds the widget to the layout 

    # Combobox for hematoma location
    self.hematomalocation = qt.QComboBox()
    #self.hematomalocation.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    #self.hematomalocation.selectNodeUponCreation = True
    self.hematomalocation.addItem('Basal Ganglia')
    self.hematomalocation.addItem('Thalamus')
    self.hematomalocation.addItem('Internal Capsule')
    self.hematomalocation.addItem('Lobar')
    self.hematomalocation.addItem('Cerebellum')
    self.hematomalocation.addItem('Brainstem')
    #self.hematomalocation.setMRMLScene( slicer.mrmlScene )
    self.hematomalocation.setToolTip( "Enter hematoma location" )


    # BUTTON TO SAVE CURRRENT CASE
    #This is a push button 
    self.saveButton = qt.QPushButton()
    self.saveButton.setDefault(False)
    #This button says connect 
    self.saveButton.text = "Save Case"
    #help tooltip that explains the funciton 
    self.saveButton.toolTip = "Save the case"
    #adds the widget to the layout 

    # Textfield that shows the current case
    self.textfield = qt.QTextEdit()
    self.textfield.setReadOnly(True)
    #bitn textfield to frame 
    



  ##################################################################################################################
  #This section adds the containers to the parent widget 
  ##################################################################################################################  
  
    # Bind the button to the 'root' layout
    self.layout.addWidget(self.parametersCollapsibleButton)

    #This creates a variable that describes layout within this collapsible button 
    # New layout for collapsible button
    self.formLayout = qt.QFormLayout(self.parametersCollapsibleButton)
    # Now put all widget in the form layout
    self.formLayout.addRow("CSV path:", self.inputIPLineEdit)
    self.formLayout.addWidget(self.loadcsv)
    self.formLayout.addWidget(self.nextButton)
    self.formLayout.addWidget(self.previousButton)       
    self.formLayout.addWidget(self.windowButton)
    self.formLayout.addRow("Hematoma location: ", self.hematomalocation)
    self.formLayout.addWidget(self.saveButton)
    self.formLayout.addWidget(self.textfield)

    

    # Add vertical spacer
    self.layout.addStretch(1)


  ##################################################################################################################
  #This section connects the widgets to functions 
  ################################################################################################################## 
    #self.inputIPLineEdit.connect('textChanged(QString)', self.onSaveCurrentCaseClicked)
    self.loadcsv.connect('clicked(bool)', self.onLoadcsvButtonClicked)
    self.nextButton.connect('clicked(bool)', self.onNextButtonClicked)
    self.previousButton.connect('clicked(bool)', self.onPreviousButtonClicked)
    self.saveButton.connect('clicked(bool)', self.onSaveCurrentCaseClicked)
    self.windowButton.connect('clicked(bool)', self.onWindowClicked)


  ##################################################################################################################
  #This section specifies what happens when you activate each widget 
  ################################################################################################################## 
  
  #MY CUSTOM FUNCTIONS START HERE

  def onLoadcsvButtonClicked(self):
    slicer.mrmlScene.Clear(False)
    # The text method allows to get the text from self.inputIPLineEdit in the widget class above
    path_data = '/Users/laurentletourneau-guillon/Dropbox (Personal)/CHUM/RECHERCHE/2020ICHHEMATOMAS/2021 Kappa Ahmad/2021_11_28 Localisation hematomas/All path cases.csv'
    #self.path_csv = pd.read_csv(self.inputIPLineEdit.text)
    self.df = pd.read_csv(path_data)    
    # Set index to beginnnig of csv
    self.currentIDx =0


  def onNextButtonClicked(self):
    slicer.mrmlScene.Clear(False)
    self.currentcase_path = self.df['Path'][self.currentIDx]
    self.currentIDx += 1
    slicer.util.loadVolume(self.currentcase_path)

    # Get the slicer volume name
    self.volume = slicer.util.getNode("vtkMRMLScalarVolumeNode1")
    # Get the name
    self.name = self.volume.GetName()
    self.textfield.clear()
    self.textfield.insertPlainText('Current Loaded (Next) Case:::{}'.format(self.name))
    #return self.currentIDx, self.currentcase_path

  def onPreviousButtonClicked(self):
    slicer.mrmlScene.Clear(False)
    self.currentIDx -= 1
    self.currentcase_path = self.df['Path'][self.currentIDx]
    slicer.util.loadVolume(self.currentcase_path)

    # Get the slicer volume name
    self.volume = slicer.util.getNode("vtkMRMLScalarVolumeNode1")
    # Get the name
    self.name = self.volume.GetName()
    self.textfield.clear()
    self.textfield.insertPlainText('Current Loaded (Previous) Case:::{}'.format(self.name))
    #return self.currentIDx, self.currentcase_path

  def onWindowClicked(self):
    # Adjust windowing
    # Firs acces the volume
    self.volume = slicer.util.getNode("vtkMRMLScalarVolumeNode1")
    self.displayNode = self.volume.GetDisplayNode()
    self.displayNode.AutoWindowLevelOff()
    self.displayNode.SetWindow(95)
    self.displayNode.SetLevel(45)


  def onSaveCurrentCaseClicked(self):
    path_output = '/Users/laurentletourneau-guillon/Dropbox (Personal)/CHUM/RECHERCHE/2020ICHHEMATOMAS/2021 Kappa Ahmad/2021_11_28 Localisation hematomas/PART II SLICER ITERATION/OUTPUTTEST'
    # Get the slicer volume name
    self.volume = slicer.util.getNode("vtkMRMLScalarVolumeNode1")
    # Get the name
    self.name = self.volume.GetName()
    # Fill the dictionnary
    
    if self.currentIDx is not None:
      self.dicthematoma['Case index'] = self.currentIDx
    else:
      self.dicthematoma['Case index'] = 'NaN'
    
    self.dicthematoma['Case number'] = self.name 
    self.dicthematoma['Hematoma Location'] = self.hematomalocation.currentText
    # Save current case     
    with open(os.path.join(path_output,'HematomaLocation_{}.json'.format(self.name)), 'w') as outfile:
        json.dump(self.dicthematoma, outfile)
    
    # Print output to textfield
    self.textfield.clear()
    self.textfield.insertPlainText('Case ***{}**** saved !'.format(self.name))


  ### END OF LLG CUSTOM CODES ####

  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())

    # Select default input nodes if nothing is selected yet to save a few clicks for the user
    if not self._parameterNode.GetNodeReference("InputVolume"):
      firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
      if firstVolumeNode:
        self._parameterNode.SetNodeReferenceID("InputVolume", firstVolumeNode.GetID())

  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True

    # Update node selectors and sliders
    self.ui.inputSelector.setCurrentNode(self._parameterNode.GetNodeReference("InputVolume"))
    self.ui.outputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume"))
    self.ui.invertedOutputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolumeInverse"))
    self.ui.imageThresholdSliderWidget.value = float(self._parameterNode.GetParameter("Threshold"))
    self.ui.invertOutputCheckBox.checked = (self._parameterNode.GetParameter("Invert") == "true")

    # Update buttons states and tooltips
    if self._parameterNode.GetNodeReference("InputVolume") and self._parameterNode.GetNodeReference("OutputVolume"):
      self.ui.applyButton.toolTip = "Compute output volume"
      self.ui.applyButton.enabled = True
    else:
      self.ui.applyButton.toolTip = "Select input and output volume nodes"
      self.ui.applyButton.enabled = False

    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

    self._parameterNode.SetNodeReferenceID("InputVolume", self.ui.inputSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID("OutputVolume", self.ui.outputSelector.currentNodeID)
    self._parameterNode.SetParameter("Threshold", str(self.ui.imageThresholdSliderWidget.value))
    self._parameterNode.SetParameter("Invert", "true" if self.ui.invertOutputCheckBox.checked else "false")
    self._parameterNode.SetNodeReferenceID("OutputVolumeInverse", self.ui.invertedOutputSelector.currentNodeID)

    self._parameterNode.EndModify(wasModified)

  def onApplyButton(self):
    """
    Run processing when user clicks "Apply" button.
    """
    try:

      # Compute output
      self.logic.process(self.ui.inputSelector.currentNode(), self.ui.outputSelector.currentNode(),
        self.ui.imageThresholdSliderWidget.value, self.ui.invertOutputCheckBox.checked)

      # Compute inverted output (if needed)
      if self.ui.invertedOutputSelector.currentNode():
        # If additional output volume is selected then result with inverted threshold is written there
        self.logic.process(self.ui.inputSelector.currentNode(), self.ui.invertedOutputSelector.currentNode(),
          self.ui.imageThresholdSliderWidget.value, not self.ui.invertOutputCheckBox.checked, showResult=False)

    except Exception as e:
      slicer.util.errorDisplay("Failed to compute results: "+str(e))
      import traceback
      traceback.print_exc()


#
# AhmadtestmoduleLogic
#

class AhmadtestmoduleLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("Threshold"):
      parameterNode.SetParameter("Threshold", "100.0")
    if not parameterNode.GetParameter("Invert"):
      parameterNode.SetParameter("Invert", "false")

  def process(self, inputVolume, outputVolume, imageThreshold, invert=False, showResult=True):
    """
    Run the processing algorithm.
    Can be used without GUI widget.
    :param inputVolume: volume to be thresholded
    :param outputVolume: thresholding result
    :param imageThreshold: values above/below this threshold will be set to 0
    :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
    :param showResult: show output volume in slice viewers
    """

    if not inputVolume or not outputVolume:
      raise ValueError("Input or output volume is invalid")

    import time
    startTime = time.time()
    logging.info('Processing started')

    # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
    cliParams = {
      'InputVolume': inputVolume.GetID(),
      'OutputVolume': outputVolume.GetID(),
      'ThresholdValue' : imageThreshold,
      'ThresholdType' : 'Above' if invert else 'Below'
      }
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
    # We don't need the CLI module node anymore, remove it to not clutter the scene with it
    slicer.mrmlScene.RemoveNode(cliNode)

    stopTime = time.time()
    logging.info('Processing completed in {0:.2f} seconds'.format(stopTime-startTime))

#
# AhmadtestmoduleTest
#

class AhmadtestmoduleTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_Ahmadtestmodule1()

  def test_Ahmadtestmodule1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    registerSampleData()
    inputVolume = SampleData.downloadSample('Ahmadtestmodule1')
    self.delayDisplay('Loaded test data set')

    inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    self.assertEqual(inputScalarRange[0], 0)
    self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    logic = AhmadtestmoduleLogic()

    # Test algorithm with non-inverted threshold
    logic.process(inputVolume, outputVolume, threshold, True)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    logic.process(inputVolume, outputVolume, threshold, False)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], inputScalarRange[1])

    self.delayDisplay('Test passed')

import logging
import os, re, glob

import vtk, qt

import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin


#
# BraTS_annotation
#

class BraTS_annotation(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "BraTS_annotation"  # TODO: make this more human readable by adding spaces
        self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["Laurent Letourneau-Guillon"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#BraTS_annotation">module documentation</a>.
"""
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

#
# BraTS_annotationWidget
#

class BraTS_annotationWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._updatingGUIFromParameterNode = False
        
        ### Added by Laurent
        self.DefaultDir = '/Users/laurentletourneau-guillon/Dropbox/CHUM/RECHERCHE/1 PROJECTS/2023 BRATS/Dr. Laurent_Letourneau-Guillon_LLG/Cases_to_approve'
        self.DefaultOutDir = '/Users/laurentletourneau-guillon/Dropbox/CHUM/RECHERCHE/1 PROJECTS/2023 BRATS/Dr. Laurent_Letourneau-Guillon_LLG/Output directory'
        self.OutDir = None
        self.current_index = 0
        

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/BraTS_annotation.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = BraTS_annotationLogic()
        
        
        ###################################################################
        ####################    WIDGETS CONNECTIONS    ####################
        ###################################################################
            
        self.ui.pushButton_DefaultDir.connect('clicked(bool)', self.onpushButton_DefaultDir)

        self.ui.listWidget.itemClicked.connect(self.on_listWidget_clicked)
        self.ui.pushButton_Next.connect('clicked(bool)', self.onNext)
        self.ui.pushButton_Previous.connect('clicked(bool)', self.onPrevious)
        self.ui.pushButton_OutDir.connect('clicked(bool)', self.onpushButton_OutDir)
        self.ui.pushButton_Save.connect('clicked(bool)', self.onpushButton_Save)




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
            

    # All methods containing ParameterNode in their name were partially commented out. 
    # More details about these methods can be found in this video series :  https://www.youtube.com/@3dslicertutorial

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
        pass

        # if inputParameterNode:
        #     self.logic.setDefaultParameters(inputParameterNode)

        # # Unobserve previously selected parameter node and add an observer to the newly selected.
        # # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
        # # those are reflected immediately in the GUI.
        # if self._parameterNode is not None and self.hasObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode):
        #     self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
        # self._parameterNode = inputParameterNode
        # if self._parameterNode is not None:
        #     self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

        # # Initial GUI update
        # self.updateGUIFromParameterNode()

    def updateGUIFromParameterNode(self, caller=None, event=None):
        """
        This method is called whenever parameter node is changed.
        The module GUI is updated to show the current state of the parameter node.
        """
        pass
        # if self._parameterNode is None or self._updatingGUIFromParameterNode:
        #     return

        # # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
        # self._updatingGUIFromParameterNode = True

        # # Update node selectors and sliders
        # self.ui.inputSelector.setCurrentNode(self._parameterNode.GetNodeReference("InputVolume"))
        # self.ui.outputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume"))
        # self.ui.invertedOutputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolumeInverse"))
        # self.ui.imageThresholdSliderWidget.value = float(self._parameterNode.GetParameter("Threshold"))
        # self.ui.invertOutputCheckBox.checked = (self._parameterNode.GetParameter("Invert") == "true")

        # # Update buttons states and tooltips
        # if self._parameterNode.GetNodeReference("InputVolume") and self._parameterNode.GetNodeReference("OutputVolume"):
        #     self.ui.applyButton.toolTip = "Compute output volume"
        #     self.ui.applyButton.enabled = True
        # else:
        #     self.ui.applyButton.toolTip = "Select input and output volume nodes"
        #     self.ui.applyButton.enabled = False

        # All the GUI updates are done
        self._updatingGUIFromParameterNode = False

    def updateParameterNodeFromGUI(self, caller=None, event=None):
        """
        This method is called when the user makes any change in the GUI.
        The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
        """
        pass

        # if self._parameterNode is None or self._updatingGUIFromParameterNode:
        #     return

        # wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

        # self._parameterNode.SetNodeReferenceID("InputVolume", self.ui.inputSelector.currentNodeID)
        # self._parameterNode.SetNodeReferenceID("OutputVolume", self.ui.outputSelector.currentNodeID)
        # self._parameterNode.SetParameter("Threshold", str(self.ui.imageThresholdSliderWidget.value))
        # self._parameterNode.SetParameter("Invert", "true" if self.ui.invertOutputCheckBox.checked else "false")
        # self._parameterNode.SetNodeReferenceID("OutputVolumeInverse", self.ui.invertedOutputSelector.currentNodeID)

        # self._paramet
    
    def onpushButton_DefaultDir(self):
        self.CurrentFolder= qt.QFileDialog.getExistingDirectory(None,"default director", self.DefaultDir, qt.QFileDialog.ShowDirsOnly)
        self.generate_listWidget()
        
        
    def get_case_IDs(self):
        folders = os.listdir(self.CurrentFolder)
        self.case_IDs = sorted([re.findall('Met([0-9]+)', folder)[0] for folder in folders if folder.startswith('Met')])

    def get_folder_paths(self):
        folders = os.listdir(self.CurrentFolder)
        self.folder_ID_paths = sorted([os.path.join(self.CurrentFolder, folder) for folder in folders if folder.startswith('Met')])
        try:
            assert len(self.case_IDs) == len(self.folder_ID_paths)
        except AssertionError as e:
            print('case_IDs and folder_ID_paths have different lengths')    
    
    def generate_listWidget(self):
        self.ui.listWidget.clear()
        self.get_case_IDs()
        self.get_folder_paths()
        self.ui.listWidget.addItems(self.case_IDs)
        self.update_current_index()
        self.get_current_case()
        self.load_case()
        
    def update_current_index(self):
        self.ui.listWidget.setCurrentRow(self.current_index)
        print('current index:', self.current_index)
        
    def get_current_case(self):
        self.current_case_ID = self.case_IDs[self.current_index]
        self.current_path = self.folder_ID_paths[self.current_index]
    
        
    def on_listWidget_clicked(self):
        print(f'clicked {self.current_index}')
        self.load_case()
    
    def onNext(self):
        self.current_index = min(self.current_index + 1, len(self.case_IDs) - 1)
        self.ui.listWidget.setCurrentRow(self.current_index)
        self.update_current_index()
        self.get_current_case()
        self.load_case()

    
    def onPrevious(self):
        self.current_index = max(self.current_index - 1, 0)
        self.ui.listWidget.setCurrentRow(self.current_index)
        self.update_current_index()
        self.get_current_case()
        self.load_case()

    def get_sequence(self):
        # for i in os.listdir(self.current_path):
    #     if i.endswith('flair.nii.gz'):
    #         sequence = i
        sequences = {
            'flair': 'flair.nii.gz',
            't1': 't1.nii.gz',
            't1ce': 't1ce.nii.gz',
            't2': 't2.nii.gz',
            'subtraction': 'subtraction.nii.gz'
        }
        
        loadable_volumes = []
        for i in sorted(glob.glob(self.current_path + '/*.nii.gz')):
            for key, value in sequences.items():
                if i.endswith(value):
                    loadable_volumes.append(i)
        return loadable_volumes


    def load_case(self):
        slicer.mrmlScene.Clear()
        print(f'loading {self.current_index}')
        
        # Load series (MR sequences)
        loadable_volumes = self.get_sequence()
        for i in loadable_volumes:
            slicer.util.loadVolume(i)
            
        self.VolumeNode = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')[0]
        
        #### NESTING ALL SERIES UNDER A CASE####
        # This allows to keep the segment connected to all series (MR Sequences)
        
        #Extract all names in VolumeNodes
        VolumeNodes = slicer.util.getNodesByClass('vtkMRMLVolumeNode')
        VolumeNodeNames = [i.GetName() for i in VolumeNodes]
        #remove the segmentation
        VolumeNodeNames = [i for i in VolumeNodeNames]
        print(f'VolumeNodeNames ::: {VolumeNodeNames}')
        
        
        # Create a subject so that all series can be nested under this subject
        # Create a subject
        shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
        # folderID = shNode.CreateFolderItem(shNode.GetSceneItemID(), 'MyFolder')
        # Create a case name
        self.case_name = f'Case_{self.case_IDs[self.current_index]}'
        shNode.CreateSubjectItem(shNode.GetSceneItemID(), self.case_name)
        
        ## Get all the needed IDs (including the parent and child IDs)
        # Get scene item ID first because it is the root item:
        sceneItemID = shNode.GetSceneItemID()
        # print(sceneItemID)
        # Get direct parent (subjectItemID) by name
        subjectItemID = shNode.GetItemChildWithName(sceneItemID, self.case_name)

        # Get all child (itemID = MR seris/sequences)
        for i in VolumeNodeNames:
            itemID  = shNode.GetItemChildWithName(sceneItemID, i)
            shNode.SetItemParent(itemID, subjectItemID)
    

        # Create segment names 
        self.ET_segment_name = "{}_ET".format(self.case_IDs[self.current_index])
        self.NCR_segment_name = "{}_NCR".format(self.case_IDs[self.current_index])
        self.SNFH_segment_name = "{}_SNFH".format(self.case_IDs[self.current_index])
        self.segmentationNodeName = "{}_segmentation".format(self.case_IDs[self.current_index])
        # Create segment editor widget and node
        self.segmentEditorWidget = slicer.modules.segmenteditor.widgetRepresentation().self().editor
        self.segmentEditorNode = self.segmentEditorWidget.mrmlSegmentEditorNode()
        # Create segmentation node
        self.segmentationNode=slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
        # Set segmentation node name
        self.segmentationNode.SetName(self.segmentationNodeName)
        # Set segmentation node to segment editor
        self.segmentEditorWidget.setSegmentationNode(self.segmentationNode)
        # Set master volume node to segment editor
        self.segmentEditorWidget.setMasterVolumeNode(self.VolumeNode)
        # set refenrence geometry to Volume node (important for the segmentation to be in the same space as the volume)
        self.segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(self.VolumeNode)
        #below will add a 'segment' in the segmentatation node which is called 'self.ICH_segm_name (for each of the 3 classes)
        self.addedSegmentID = self.segmentationNode.GetSegmentation().AddEmptySegment(self.ET_segment_name)
        self.addedSegmentID = self.segmentationNode.GetSegmentation().AddEmptySegment(self.NCR_segment_name)
        self.addedSegmentID = self.segmentationNode.GetSegmentation().AddEmptySegment(self.SNFH_segment_name)
        # Nest the segmentation node under subject
        
        SegmentationNode = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
        print(f'SegmentationNode :: {SegmentationNode.GetName()}')
        # Nest segmentation Node under subject
        segm_itemID  = shNode.GetItemChildWithName(sceneItemID, SegmentationNode.GetName())
        shNode.SetItemParent(segm_itemID, subjectItemID)
            
    def onpushButton_OutDir(self):
        self.OutDir= qt.QFileDialog.getExistingDirectory(None,"default director", self.DefaultOutDir, qt.QFileDialog.ShowDirsOnly)


    def onpushButton_Save(self):
        """
        Updates the segmentation node and save as *.nii.gz      
        """
        # Update the segmentation and volume node (since brats sequences are all the same shape and size) we can
        # Choose only the first volume node. 
        # This update is done in case the user has changed the segmentation (e.g. manually) and wants to save it. 
        volumeNode = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')[0]
        segmentationNode = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
        print('Getting the segmentation Node prior to saving')
        print(f'segmentationNode :: {segmentationNode.GetName()}')
        

        if not self.OutDir:
            msg_nodir = qt.QMessageBox()
            msg_nodir.setWindowTitle('Output directory')
            msg_nodir.setText('No output directory !')
            msg_nodir.setIcon(qt.QMessageBox.Warning)
            msg_nodir.setStandardButtons(qt.QMessageBox.Ok)
            msg_nodir.exec()
        else:   
            # Convert segment labels to  labelmap representation
            labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode')
            slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode,labelmapVolumeNode, volumeNode)
            
            # Create a file and save the segmentation
            outputSegmFileNifti = os.path.join(self.OutDir,
                                                    "Segmentation_{}.nii.gz".format(self.current_case_ID))
            
            
        # Save the file    
        slicer.util.saveNode(labelmapVolumeNode, outputSegmFileNifti)
        print('Saved segmentation as .nii.gz file!')
     
        
#
# BraTS_annotationLogic
#

class BraTS_annotationLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """
    pass

    # def __init__(self):
    #     """
    #     Called when the logic class is instantiated. Can be used for initializing member variables.
    #     """
    #     ScriptedLoadableModuleLogic.__init__(self)

    # def setDefaultParameters(self, parameterNode):
    #     """
    #     Initialize parameter node with default settings.
    #     """
    #     if not parameterNode.GetParameter("Threshold"):
    #         parameterNode.SetParameter("Threshold", "100.0")
    #     if not parameterNode.GetParameter("Invert"):
    #         parameterNode.SetParameter("Invert", "false")

    # def process(self, inputVolume, outputVolume, imageThreshold, invert=False, showResult=True):
    #     """
    #     Run the processing algorithm.
    #     Can be used without GUI widget.
    #     :param inputVolume: volume to be thresholded
    #     :param outputVolume: thresholding result
    #     :param imageThreshold: values above/below this threshold will be set to 0
    #     :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
    #     :param showResult: show output volume in slice viewers
    #     """

    #     if not inputVolume or not outputVolume:
    #         raise ValueError("Input or output volume is invalid")

    #     import time
    #     startTime = time.time()
    #     logging.info('Processing started')

    #     # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
    #     cliParams = {
    #         'InputVolume': inputVolume.GetID(),
    #         'OutputVolume': outputVolume.GetID(),
    #         'ThresholdValue': imageThreshold,
    #         'ThresholdType': 'Above' if invert else 'Below'
    #     }
    #     cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
    #     # We don't need the CLI module node anymore, remove it to not clutter the scene with it
    #     slicer.mrmlScene.RemoveNode(cliNode)

    #     stopTime = time.time()
    #     logging.info(f'Processing completed in {stopTime-startTime:.2f} seconds')


#
# BraTS_annotationTest
#

class BraTS_annotationTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_BraTS_annotation1()

    def test_BraTS_annotation1(self):
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
        inputVolume = SampleData.downloadSample('BraTS_annotation1')
        self.delayDisplay('Loaded test data set')

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = BraTS_annotationLogic()

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

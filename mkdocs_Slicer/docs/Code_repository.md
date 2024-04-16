
<!-- TOC -->
* [Subject hierarchy](#subject-hierarchy)
* [Save volume statistis](#save-volume-statistis)
<!-- TOC -->

# Segmentation
## Getting specific segments
- Hierarchical data structure of the segmentation node : SegmentationNode -> Segmentation -> Segment
- [Example on the script repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#modify-segmentation-display-options)
```py linenums="1" hl_lines="12"
segmentation = slicer.util.getNode('Segmentation')
#If the segment name is already known, you can get the segment by name:
segmentname = 'Segment_1'

#Change the 3D display properties of the segmentation
displayNode = segmentation.GetDisplayNode()
displayNode.SetOpacity3D(0.9)  # Set overall opacity of the segmentation
displayNode.SetSegmentOpacity3D(segmentname, 0.2)  # Set opacity of a single segment


# Segment color is not just a display property, but it is stored in the segment itself (and stored in the segmentation file)
segment = segmentation.GetSegmentation().GetSegment(segmentname)
segment.SetColor(1, 0, 0)  # red
```


# Subject hierarchy
- [Subject hierarchy](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#subject-hierarchy)
> ![Slicer subject hierachy.png](images%2FSlicer%20subject%20hierachy.png)
```py
import slicer
def subjectHierarchy(self):
    # Get the subject hierarchy node
    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()

    # Get scene item ID first because it is the root item:
    sceneItemID = shNode.GetSceneItemID()
    # Get the scene item ID (check if the scene item exists)
    subjectItemID = shNode.GetItemChildWithName(shNode.GetSceneItemID(), self.currentCase)
    if not subjectItemID:
        subjectItemID = shNode.CreateSubjectItem(shNode.GetSceneItemID(), self.currentCase)

    # TODO: this will need to be updated when moving to multiple studies per patient (or done in a separate script)
    # Creat a folder to include a study (if more than one study)
    # check if the folder exists and if not create it (avoid recreating a new one when reloading a mask)
    Study_name = 'Study to be updated'
    folderID = shNode.GetItemChildWithName(subjectItemID, Study_name)
    if not folderID:
        folderID = shNode.CreateFolderItem(subjectItemID, Study_name)
    # set under the subject
    shNode.SetItemParent(folderID, subjectItemID)

    # get all volume nodes
    VolumeNodes = slicer.util.getNodesByClass('vtkMRMLVolumeNode')
    VolumeNodeNames = [i.GetName() for i in VolumeNodes]
    # Get all child (itemID = CT or MR series/sequences)
    for i in VolumeNodeNames:
        itemID = shNode.GetItemChildWithName(sceneItemID, i)
        shNode.SetItemParent(itemID, folderID)
    # same thing for segmentation nodes
    SegmentationNodes = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')
    SegmentationNodeNames = [i.GetName() for i in SegmentationNodes]
    # move all segmentation nodes to the subject
    for i in SegmentationNodeNames:
        itemID = shNode.GetItemChildWithName(sceneItemID, i)
        shNode.SetItemParent(itemID, folderID)
```


# Save volume statistis
```py
  def save_statistics(self):
      volumeNode=slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')[0]
      segmentationNode=slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
      segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(volumeNode)
      segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
      segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
      segStatLogic.getParameterNode().SetParameter("ScalarVolume", volumeNode.GetID())
      segStatLogic.getParameterNode().SetParameter("LabelSegmentStatisticsPlugin.obb_origin_ras.enabled",str(True))
      segStatLogic.getParameterNode().SetParameter("LabelSegmentStatisticsPlugin.obb_diameter_mm.enables",str(True))
      segStatLogic.getParameterNode().SetParameter("LabelSegmentStatisticsPlugin.obb_direction_ras_x_.enabled", str(True))
      segStatLogic.getParameterNode().SetParameter("LabelSegmentStatisticsPlugin.obb_direction_ras_y_.enabled",str(True))
      segStatLogic.getParameterNode().SetParameter("LabelSegmentStatisticsPlugin.obb_direction_ras_z_.enabled", str(True))
      segStatLogic.getParameterNode().SetParameter("LabelSegmentStatisticsPLugin.obb_diameter_mm.enables", str(True))
      segStatLogic.computeStatistics()
      output_file_pt_id_instanceUid = re.findall(self.VOL_REGEX_PATTERN_PT_ID_INSTUID_SAVE, os.path.basename(self.currentCasePath))[0]


      outputFilename = f'Volumes_{output_file_pt_id_instanceUid}.csv'
      output_dir_volumes_csv = os.path.join(self.output_dir_labels, 'csv_volumes')
      output_dir_volumes_csv = os.path.join(self.output_dir_labels, 'csv_volumes')
      outputFilename = os.path.join(output_dir_volumes_csv, outputFilename)

      segStatLogic.exportToCSVFile(outputFilename)
      stats = segStatLogic.getStatistics()

      # Read the csv and clean it up
      df = pd.read_csv(outputFilename)
      df.set_index('Segment')
      df = df[['Segment', 'LabelmapSegmentStatisticsPlugin.volume_cm3']]
      df.rename(columns={'LabelmapSegmentStatisticsPlugin.volume_cm3': "Volumes"}, inplace=True)
      df['ID'] = df['Segment'].str.extract("(ID_[a-zA-Z0-90]+)_")
      df['Category'] = df['Segment'].str.extract("_([A-Z]+)$")

      if not os.path.exists(output_dir_volumes_csv):
          os.makedirs(output_dir_volumes_csv)


      if not os.path.isfile(outputFilename):
          df.to_csv(outputFilename, index=False)
          print(f'Wrote segmentation file here {outputFilename}')
      else:
          msg = qt.QMessageBox()
          msg.setWindowTitle('Save As')
          msg.setText(f'The file {outputFilename} already exists \n Do you want to replace the existing file?')
          msg.setIcon(qt.QMessageBox.Warning)
          msg.setStandardButtons(qt.QMessageBox.Ok | qt.QMessageBox.Cancel)
          msg.exec()
          if msg.clickedButton() == msg.button(qt.QMessageBox.Ok):
              df.to_csv(outputFilename, index=False)
              print(f'Wrote segmentation file here {outputFilename}')
```

<!-- TOC -->
* [Segmentation](#segmentation)
  * [Getting specific segments](#getting-specific-segments)
  * [Changing the ID color based on completion status](#changing-the-id-color-based-on-completion-status)
* [Subject hierarchy](#subject-hierarchy)
* [Save volume statistics](#save-volume-statistics)
* [Keyboard shortcuts from configuration file](#keyboard-shortcuts-from-configuration-file)
<!-- TOC -->


# Layout

## Compare view widescreen (with 1 row and 2 columns). I have not yet figured out how to get the 1x1 view. 
```py
# Set to widescreen compare view
layoutManager = slicer.app.layoutManager()
layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutCompareWidescreenView)

# Configure the layout to display 2 viewers in Compare Widescreen mode
layoutNode = slicer.app.layoutManager().layoutLogic().GetLayoutNode()
layoutNode.SetNumberOfCompareViewRows(1)  # 1 row
layoutNode.SetNumberOfCompareViewColumns(2)  # 2 columns
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


# Segmentation
## Getting specific segments
- Hierarchical data structure of the segmentation node : SegmentationNode -> Segmentation -> Segment. The key is `segmentation.GetSegmentation().GetSegment(segmentname)`
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
## Changing the ID color based on completion status

```py
    def update_current_case_paths_by_segmented_volumes(self):
        if not self.VolumeNode and not self.segmentationNode:
            qt.QMessageBox.warning(None, 'No case selected', 'Please load volumes and segmentations first')
            raise ValueError('No case selected')
        print('coloring segmented volumes')
        print(self.OutDir)
        segmentations = glob(os.path.join(self.config['OutDir'], self.config['SEGM_FILE_TYPE']))
        print(len(segmentations))
        print(self.config['SEGM_REGEX'])
        print(os.path.basename(segmentations[0]))
        segmented_IDs = [re.findall(self.config['SEGM_REGEX'], os.path.basename(segmentation))[0] for segmentation in
                         segmentations]

        self.ui.SlicerDirectoryListView.clear()
        for case in self.CasesPaths:
            case_id = re.findall(self.config['VOL_REGEX'], case)[0]
            item = qt.QListWidgetItem(case_id)
            if not case_id in segmented_IDs:
                item.setForeground(qt.QColor('red'))

            elif case_id in segmented_IDs:
                item.setForeground(qt.QColor('green'))
            self.ui.SlicerDirectoryListView.addItem(item)
```

## Nifti: Updating the segment names and color 
e.g. import from nnUNet

```py

    def convert_nifti_header_Segment(self):

        # Check if the first segment starts with Segment_1 (e.g. loaded from nnunet).
        # If so change the name and colors of the segments to match the ones in the config file
        first_segment_name = self.segmentationNode.GetSegmentation().GetNthSegment(0).GetName()
        print(f'first_segment_name :: {first_segment_name}')
        if first_segment_name.startswith("Segment_"):
            # iterate through all segments and rename them

            for i in range(self.segmentationNode.GetSegmentation().GetNumberOfSegments()):
                segment_name = self.segmentationNode.GetSegmentation().GetNthSegment(i).GetName()
                print(f' src segment_name :: {segment_name}')
                for label in self.config_yaml["labels"]:
                    if label["value"] == int(segment_name.split("_")[-1]):
                        self.segmentationNode.GetSegmentation().GetNthSegment(i).SetName(label['name'])
                        # set color
                        self.segmentationNode.GetSegmentation().GetNthSegment(i).SetColor(label["color_r"] / 255,
                                                                                          label["color_g"] / 255,
                                                                                          label["color_b"] / 255)

        self.add_missing_nifti_segment()

    def add_missing_nifti_segment(self):
        for label in self.config_yaml['labels']:
            name = label['name']
            segment_names = [self.segmentationNode.GetSegmentation().GetNthSegment(node).GetName() for node in
                             range(self.segmentationNode.GetSegmentation().GetNumberOfSegments())]
            if not name in segment_names:
                self.segmentationNode.GetSegmentation().AddEmptySegment(name)
                segmentid = self.segmentationNode.GetSegmentation().GetSegmentIdBySegmentName(name)
                segment = self.segmentationNode.GetSegmentation().GetSegment(segmentid)
                segment.SetColor(label["color_r"] / 255,
                                 label["color_g"] / 255,
                                 label["color_b"] / 255)

```


## Segment QC




# Save volume statistics
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

# Keyboard shortcuts from configuration file
- Pass the method name (without 'self.' and '()') and the keyboard shortcut. Make sure this does not conflict with the default shortcuts.
```yaml
KEYBOARD_SHORTCUTS: 
  - method: "keyboard_toggle_fill"
    shortcut: "d"
```
Corresponds to section in `SEGMENTER_V2Widget.setup()` immediately after the widget connections. Adapted from the [3D Slicer script repository](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html#customize-keyboard-shortcuts)
```py
    # KEYBOARD SHORTCUTS
    keyboard_shortcuts = []
    for i in self.config_yaml["KEYBOARD_SHORTCUTS"]:
        shortcutKey = i.get("shortcut")
        callback_name = i.get("method")
        callback = getattr(self, callback_name)
        keyboard_shortcuts.append((shortcutKey, callback))

    print(f'keyboard_shortcuts: {keyboard_shortcuts}')


    for (shortcutKey, callback) in keyboard_shortcuts:
        shortcut = qt.QShortcut(slicer.util.mainWindow())
        shortcut.setKey(qt.QKeySequence(shortcutKey))
        shortcut.connect("activated()", callback)
```
For buttons that 'toggles' this method was created:
- [ ] create a more general method that can be used for all buttons that toggle on and off.
```py
  def keyboard_toggle_fill(self):
      print('keyboard_toggle_fill')
      if self.ui.pushButton_ToggleFill.isChecked():
          self.ui.pushButton_ToggleFill.toggle()
          self.toggleFillButton()
      else:
          self.ui.pushButton_ToggleFill.toggle()
          self.toggleFillButton()

```



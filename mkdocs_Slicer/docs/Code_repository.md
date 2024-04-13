
<!-- TOC -->
  * [Subject hierarchy](#subject-hierarchy)
<!-- TOC -->

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

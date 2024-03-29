# Perception

## perception.py

<center>

![alt text](./Images/Software_perception.png)

</center>

### Detector

We offer two different detectors, built by VITA laboratory: 

* **Openpifpaf** 

Human detector. Reference: https://github.com/vita-epfl/openpifpaf

<center>

Closed-Loop Tests               |  Openpifpaf Keypoint Extraction
:-------------------------: |:-------------------------:
<img src="../control/Images/MR_EPFL.gif" alt="drawing" width="500"/> | <img src="../control/Images/MR_EPFL_skeleton.gif" alt="drawing" width="500"/>

</center>

* **Minion (Default)** 

Minion images detector. Reference: https://github.com/vita-epfl/socket-loomo/blob/master/python/detector.py

<p align="center">
<img src="./Images/Perception_minion.gif" alt="drawing" width="400"/>
</p>

**Comparison between both detectors:**

All real time detectors can be added inside the pipeline, setting the required parameters.

``` python 
detection_image = DetectorConfig(width=w, height=h, channels=c, downscale=d,
                                        global_path='path', detector=detector_class(),
                                        load=bool, type_input=t) 
```

Where ```width```, ```height``` and ```channels``` are the sizes expected by ```detector```, and ```downscale``` is the resize relation between detection size product _(w·h·c)_ and Loomo camera size multiplication _(80·60·3)_. If we need to load a model for the detector, we use parameter ```load=True ``` and we add set ```global_path='path_to_model'```. ```type_input``` depends on detector's input requirements, usually varying between _opencv_ and _pil_ modules.

Finally, in every iteretion, attribute ```detect``` from class ```DetectorConfig``` is used in order to output bounding boxes and labels with the remarked observations. 

``` python
bbox_list, label_list = detection_image.detect(received_image)
```




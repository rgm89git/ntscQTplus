from app.Renderer import DefaultRenderer, Config
from app.ntsc import Ntsc
import cv2
import numpy

from app.logs import logger
from app.funcs import resize_to_height, trim_to_4width, expand_to_4width

class InterlacedRenderer(DefaultRenderer):
    interlaced = True
    
    @staticmethod
    def apply_main_effect(nt: Ntsc, frame1, frame2=None, frameId=0):
        #raise NotImplementedError()
        if frame2 is None:
            frame2 = frame1

        frame1 = nt.composite_layer(frame1, frame1, field=0, fieldno=0, frame=frameId)
        frame1 = cv2.convertScaleAbs(frame1)

        frame2 = cv2.copyMakeBorder(frame2,1,0,0,0,cv2.BORDER_CONSTANT)
        frame2 = nt.composite_layer(frame2, frame2, field=2, fieldno=2, frame=frameId)
        frame2 = cv2.convertScaleAbs(frame2)
        frame = frame1
        frame[1::2,:] = frame2[2::2,:]
        return frame
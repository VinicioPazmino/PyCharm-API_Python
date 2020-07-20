import cv2
import numpy as np 
from PIL import Image

KEYESCAPE=27
KEYENTER=10 ## Different from Windows
KEYLEFT=81
KEYRIGHT=83
KEYUP=82
KEYDOWN=84
WAITMSTOREFRESH=15


CMD_STRLEN_DEF=50 			###< Default length for commands
BUFFER_FRAME_DEF=10000000  ###< 10Mb fixed-size buffer for TX-RX

STRLEN_SHORT_DEF=50
STRLEN_LONG_DEF=255

CAM_FPS_DEF=10		###< Default frames per second (FPS) 
CAM_POSX_DEF=10.0	###< Default X-position (left-right)
CAM_POSY_DEF=-4.0	###< Default Y - position(Height)
CAM_POSZ_DEF=3.0	###< Default Z-position (Forward-backward)
CAM_ROTX_DEF=20.0	###< Default X-axis rotation
CAM_ROTY_DEF=10.0	###< Default Y-axis rotation
CAM_ROTZ_DEF=0.0	###< Default Z-axis rotation
CAM_FOV_DEF=1.0		###< Default FOV
CAM_JPGQ_DEF=80		###< Default JPEG quality


CAM_MOVE_LEFT = 0	###< ID to move camera left
CAM_MOVE_RIGHT=1	###< ID to move camera right
CAM_MOVE_UP=2		###< ID to move camera up
CAM_MOVE_DOWN=3		###< ID to move camera down
CAM_MOVE_FORWARD=4	###< ID to move camera forward
CAM_MOVE_BACKWARD=5	###< ID to move camera backward
CAM_ROTATE_LEFT=6	###< ID to rotate camera left
CAM_ROTATE_RIGHT=7	###< ID to rotate camera right
CAM_ROTATE_UP=8		###< ID to rotate camera up
CAM_ROTATE_DOWN=9	###< ID to rotate camera down


### Possible compression schemes to TX/RX images between MSS server & client
CAM_JPEG=0		###< JPEG codec (lossy image compression)
CAM_PNG=1		###< PNG codec (lossless image compression)

## Minimum pixel height-coordinates (in the displayed image for the "showCameraScheme")
SECOND_IMG_OFFSET=95.0

## Distance between min & max user inputs for the 2nd screen ("showCameraScheme" --> cameraHeight-GUI)
SECOND_IMG_WIDTH=550.0

def overlayImage(bg,icon,pos):
    w_bg=bg.width
    h_bg=bg.height
    w_icon=icon.width
    h_icon=icon.height
    full_icon=Image.new('RGBA',(w_bg,h_bg),(0,0,0,0))
    icon=np.array(icon)
    full_icon=np.array(full_icon)
	# position of start of camera icon given by pos, 
	# or 0 if the pos given is negative
    start_full_w=max(pos[0],0)
    start_full_h=max(pos[1],0)
	# position of end of camera icon given by pos, 
	# or size of background if the pos given is out of bounds
    end_full_w=min(pos[0]+w_icon,w_bg)
    end_full_h=min(pos[1]+h_icon,h_bg)
	# Coordinates to crop the icon if we go out of bounds with pos
    start_icon_w=start_full_w-pos[0]
    start_icon_h=start_full_h-pos[1]
    end_icon_w=end_full_w-pos[0]
    end_icon_h=end_full_h-pos[1]
    full_icon[start_full_h:end_full_h,start_full_w:end_full_w,:]=icon[start_icon_h:end_icon_h,start_icon_w:end_icon_w,:]
    out_icon=Image.fromarray(np.uint8(full_icon))
    imout=Image.alpha_composite(bg,out_icon)
    return imout

### Method create strings to display messages in the command window
"""static std::map<int, std::string> create_codec_str() {

	std::map<int, std::string> m;
	m.insert(std::make_pair(CAM_JPEG, "CAM_JPEG"));
	m.insert(std::make_pair(CAM_PNG, "CAM_PNG"));
	m.insert(std::make_pair(CAM_RAW, "CAM_RAW"));
	return m;
}"""

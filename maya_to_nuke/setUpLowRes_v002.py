import maya.cmds as cmds

def set_arnold_lowres_preview():
    w = cmds.getAttr("defaultResolution.width")
    h = cmds.getAttr("defaultResolution.height")
    resize_w = w / 2
    resize_h = h / 2
    
    
    # ------------------------
    # OK / Cancel Dialog
    # ------------------------
    result = cmds.confirmDialog(
        title="Arnold Low Res Settings",
        message=f"all samples set to 1<br>resize to Resolution:\n{resize_w} x {resize_h} ?",
        button=["YES", "NO"],
        defaultButton="YES",
        cancelButton="NO",
        dismissString="NO",
        icon="question"
    )

    if result == "YES":
        cmds.setAttr("defaultResolution.width",  resize_w)
        cmds.setAttr("defaultResolution.height",  resize_h)
       
        
       

    # ------------------------
    # Settings anwenden
    # ------------------------


    cmds.setAttr("defaultArnoldRenderOptions.AASamples", 1)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 1)
    cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 1)
    cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 1)
    cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", 1)
    cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", 1)
    cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 0)

    #cmds.setAttr("defaultArnoldRenderOptions.motion_steps", 2)

    # ------------------------
    # Success Message
    # ------------------------
    cmds.inViewMessage(
        amg=f"<hl>Arnold LowRES Rendering aktiv</hl><br>{w} x {h}",
        pos="topCenter",
        fade=True,
        fadeStayTime=1000
    )

    # print("✅ Arnold Ultra-Low-Res Preview Settings gesetzt")

set_arnold_lowres_preview()

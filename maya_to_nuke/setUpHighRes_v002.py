import maya.cmds as cmds

WINDOW_NAME = "arnoldPreviewTool"

# ---------------------------------------------------
# Resolution Funktionen
# ---------------------------------------------------

def update_resolution_label():
    w = cmds.getAttr("defaultResolution.width")
    h = cmds.getAttr("defaultResolution.height")
    cmds.text("resLabel", e=True, label=f"Current Resolution: {w} x {h}")

def double_resolution(*args):
    w = cmds.getAttr("defaultResolution.width")
    h = cmds.getAttr("defaultResolution.height")

    cmds.setAttr("defaultResolution.width", int(w * 2))
    cmds.setAttr("defaultResolution.height", int(h * 2))

    update_resolution_label()
    print("Resolution x2 gesetzt")

def half_resolution(*args):
    w = cmds.getAttr("defaultResolution.width")
    h = cmds.getAttr("defaultResolution.height")

    cmds.setAttr("defaultResolution.width", int(w * 0.5))
    cmds.setAttr("defaultResolution.height", int(h * 0.5))

    update_resolution_label()
    print("Resolution x0.5 gesetzt")

# ---------------------------------------------------
# Motion Blur Toggle
# ---------------------------------------------------

def toggle_motionblur(*args):
    state = cmds.checkBox("mbCheck", q=True, v=True)
    cmds.intField("mbStepsField", e=True, enable=state)

# ---------------------------------------------------
# Apply Arnold Settings
# ---------------------------------------------------

def apply_arnold_settings(*args):

    aa = cmds.intField("aaField", q=True, v=True)
    diffuse = cmds.intField("diffField", q=True, v=True)
    spec = cmds.intField("specField", q=True, v=True)
    trans = cmds.intField("transField", q=True, v=True)
    sss = cmds.intField("sssField", q=True, v=True)
    vol = cmds.intField("volField", q=True, v=True)

    motion_enabled = cmds.checkBox("mbCheck", q=True, v=True)
    motion_steps = cmds.intField("mbStepsField", q=True, v=True)

    # Arnold Sampling setzen
    cmds.setAttr("defaultArnoldRenderOptions.AASamples", aa)
    cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", diffuse)
    cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", spec)
    cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", trans)
    cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", sss)
    cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", vol)

    # Motion Blur
    cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", motion_enabled)

    if motion_enabled:
        cmds.setAttr("defaultArnoldRenderOptions.motion_steps", motion_steps)

    print("Arnold Settings gesetzt.")

    # >>> Fenster schließen <<<
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)
    
    ###########UI MESSAGE
    w = cmds.getAttr("defaultResolution.width")
    h = cmds.getAttr("defaultResolution.height")    
    message = (
        f"<hl>Arnold HIGHRES Rendering aktiv</hl><br>"
        f"AA: {aa} | Diff: {diffuse} | Spec: {spec}<br>"
        f"resolution: {w} x {h}<br>"
        f"Motion Blur: {'ON' if motion_enabled else 'OFF'}"
    )

    cmds.inViewMessage(
        amg=message,
        pos='topCenter',
        fade=True,
        fadeStayTime=1000
    )


# ---------------------------------------------------
# UI
# ---------------------------------------------------

def create_ui():

    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    cmds.window(
        WINDOW_NAME,
        title="SETUP HIGH RES",
        widthHeight=(380, 520),
        sizeable=True
    )

    # WICHTIG:
    cmds.scrollLayout(childResizable=True)

    # WICHTIG:
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=10,
        columnAttach=("both", 5)  # kleiner Rand links/rechts
    )


    # ---------------- Resolution ----------------
    cmds.frameLayout(label="Resolution", collapsable=False)

    cmds.text("resLabel", label="")
    update_resolution_label()

    cmds.rowLayout(nc=2, adjustableColumn=1)
    cmds.button(label="x2 Resolution", height=35, command=double_resolution)
    cmds.button(label="x0.5 Resolution", height=35, command=half_resolution)
    cmds.setParent("..")

    cmds.setParent("..")

    # ---------------- Sampling ----------------
    cmds.frameLayout(label="Arnold Sampling", collapsable=False)

    def create_row(label, name, default):
        cmds.rowLayout(nc=2, adjustableColumn=2)
        cmds.text(label=label, width=180)
        cmds.intField(name, v=default, min=0)
        cmds.setParent("..")

    create_row("AA Samples", "aaField", 4)
    create_row("Diffuse Samples", "diffField", 2)
    create_row("Specular Samples", "specField", 2)
    create_row("Transmission Samples", "transField", 4)
    create_row("SSS Samples", "sssField", 2)
    create_row("Volume Samples", "volField", 2)

    cmds.setParent("..")

    # ---------------- Motion Blur ----------------
    cmds.frameLayout(label="Motion Blur", collapsable=False)

    cmds.checkBox(
        "mbCheck",
        label="Enable Motion Blur",
        value=False,
        changeCommand=toggle_motionblur
    )

    cmds.rowLayout(nc=2, adjustableColumn=2)
    cmds.text(label="Motion Steps", width=180)
    cmds.intField("mbStepsField", v=6, min=1, enable=False)
    cmds.setParent("..")

    cmds.setParent("..")

    # ---------------- Apply Button ----------------
    cmds.separator(h=15)
    cmds.button(
        label="Apply Settings",
        height=45,
        command=apply_arnold_settings
    )

    cmds.showWindow(WINDOW_NAME)

# ---------------------------------------------------
# Start UI
# ---------------------------------------------------

create_ui()

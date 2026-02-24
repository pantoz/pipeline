import maya.cmds as cmds
import mtoa.aovs as aovs

###############   DEFINE PASSES   ################################
standard_aovs = [
    "albedo",
    "background",
    "coat",
    "diffuse",
    "diffuse_direct",
    "diffuse_indirect",
    "specular",
    "transmission",
    "emission",
    "sss",
    "volume",
]
tech_passe = [
    "N",
    "P",
    "Pref",
    "Z",
    "motionvector"
]
##################################################################

###########    DEFINE OUTPUT SETTINGS     ########################
cmds.setAttr("defaultArnoldDriver.aiTranslator", "exr", type="string")
cmds.setAttr("defaultArnoldDriver.mergeAOVs", 0)       # Multilayer EXR
cmds.setAttr("defaultArnoldDriver.exrCompression", 2)  # ZIP
cmds.setAttr("defaultArnoldDriver.halfPrecision", 1)   # 16-bit EXR
cmds.setAttr("defaultArnoldDriver.tiled", False)       # Tiled
cmds.setAttr("defaultArnoldDriver.autocrop", True)     # Autocrop

######### SET TECH PASSES ########################################
if not cmds.objExists("techArnoldDriver"):
    tech_driver = cmds.createNode("aiAOVDriver", name="techArnoldDriver")
    cmds.setAttr(tech_driver + ".aiTranslator", "exr", type="string")
    cmds.setAttr(tech_driver + ".mergeAOVs", 0)
    cmds.setAttr(tech_driver + ".exrCompression", 2)
    cmds.setAttr(tech_driver + ".halfPrecision", 0)
    cmds.setAttr(tech_driver + ".tiled", False)
    cmds.setAttr(tech_driver + ".autocrop", True)
    print("techArnoldDriver erstellt")
else:
    tech_driver = "techArnoldDriver"
    print("techArnoldDriver schon vorhanden")
    
if not cmds.objExists("DeepArnoldDriver"):
    deep_driver = cmds.createNode("aiAOVDriver", name="DeepArnoldDriver")
    cmds.setAttr(deep_driver + ".aiTranslator", "deepexr", type="string")
    cmds.setAttr(deep_driver + ".mergeAOVs", 0)
    cmds.setAttr(deep_driver + ".exrCompression", 2)
    cmds.setAttr(deep_driver + ".halfPrecision", 0)
    cmds.setAttr(deep_driver + ".tiled", False)
    cmds.setAttr(deep_driver + ".autocrop", True)
    print("techArnoldDriver erstellt")
else:
    deep_driver = "DeepArnoldDriver"
    print("DeepArnoldDriver schon vorhanden")

aov_interface = aovs.AOVInterface()
layer_name = None  # MasterLayer

##################### LIGHT GROUPS FINDEN #########################
arnold_light_types = ["aiAreaLight", "aiSkyDomeLight", "aiPhotometricLight"]
all_lights = cmds.ls(type=arnold_light_types, long=True)

lightgroups_set = set()
for light_shape in all_lights:
    if cmds.attributeQuery("aiAov", node=light_shape, exists=True):
        aov_value = cmds.getAttr(f"{light_shape}.aiAov")
        if aov_value:
            groups = [g.strip() for g in aov_value.split(",")]
            lightgroups_set.update(groups)

lightgroups_list = sorted(list(lightgroups_set))
print("\nAlle gefundenen Light Groups:")
for lg in lightgroups_list:
    print(" -", lg)
    
# ---------------- LIGHTGROUP CHECK ----------------

#if not lightgroups_list:
#    result = cmds.confirmDialog(
#        title="Keine Lightgroups gefunden",
#        message="Du hast noch keine Lightgroups definiert.\n\nTrotzdem weitermachen?",
#        button=["JA", "NEIN"],
#        defaultButton="JA",
#        cancelButton="NEIN",
#        dismissString="NEIN",
#        icon="warning"
#    )

#    if result == "NEIN":
#        cmds.warning("AOV Setup abgebrochen – keine Lightgroups vorhanden.")
#        raise RuntimeError("Script abgebrochen durch Benutzer.")


######### FUNCTION TO CREATE CUSTOM AOV ##########################
def create_custom_aov(aov_name):
    if not aov_name:
        return None
    if aov_interface.getAOVNode(aov_name, layer_name):
        print(f"AOV '{aov_name}' existiert bereits.")
        return aov_interface.getAOVNode(aov_name, layer_name)
    aov_interface.addAOV(aov_name)
    print(f"Custom AOV '{aov_name}' wurde erstellt.")
    return aov_interface.getAOVNode(aov_name, layer_name)

######### CREATE STANDARD AOVS ###################################
for lg in lightgroups_list:
    for p in standard_aovs:
        name = f"{p}_{lg}"
        create_custom_aov(name)

######### CREATE TECH AOVS #######################################
for aov_name in tech_passe:
    aov = create_custom_aov(aov_name)
    if aov:
        cmds.connectAttr(tech_driver + ".message", aov + ".outputs[0].driver", force=True)

######### CREATE CRYPTOMATTE AOVS ################################
crypto_aovs = ["CryptoObject", "CryptoMaterial", "CryptoAsset"]
for aov_name in crypto_aovs:
    create_custom_aov(aov_name)

######### CREATE DEEP PASS #######################################
result = cmds.confirmDialog(
    title="Deep Pass",
    message="Setup Deep Pass?",
    button=["YES", "NO"],
    defaultButton="YES",
    cancelButton="NO",
    dismissString="NO",
    icon="question"
)

if result == "YES":
    deep = create_custom_aov("deep")
    if deep:
        cmds.connectAttr(deep_driver + ".message", deep + ".outputs[0].driver", force=True)
        deep_created = True
if result == "NO":
        deep_created = False

# ---------------------------------------------------
# SUMMARY MESSAGE
# ---------------------------------------------------

lg_count = len(lightgroups_list)
deep_status = "Deep added" if deep_created == True else "Deep not added"

message = (
    f"<hl>AOVs added</hl><br>"
    f"Lightgroups found: {lg_count}<br>"
    f"{deep_status}"
)

cmds.inViewMessage(
    amg=message,
    pos="topCenter",
    fade=True,
    fadeStayTime=1000
)

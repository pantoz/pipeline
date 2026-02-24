import nuke
import os
import re

def create_aov_shuffles_under_beauty():
    selected_nodes = nuke.selectedNodes('Read')
    if not selected_nodes:
        nuke.message("Bitte wähle einen Read-Node (Beauty) aus.")
        return

    beauty_read = selected_nodes[0]
    beauty_file = beauty_read['file'].getValue()
    
    parent_folder = os.path.dirname(beauty_file)
    grandparent_folder = os.path.dirname(parent_folder)
    
    for folder_name in sorted(os.listdir(grandparent_folder)):
        folder_path = os.path.join(grandparent_folder, folder_name)
        if os.path.isdir(folder_path):
            # Liste EXR-Dateien im Unterordner
            exr_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.exr')])
            if not exr_files:
                continue
            
            first_file = exr_files[0]
            
            # Ersetze die Frame-Zahl (z.B. 0001) durch #### für Nuke-Sequenz
            seq_path = os.path.join(folder_path, first_file)
            seq_path = seq_path.replace("\\", "/")
            seq_path = re.sub(r'\d+(?=\.exr$)', '####', seq_path)
            
            # Read-Node für die AOV-Sequenz
            aov_read = nuke.createNode("Read")
            aov_read['file'].setValue(seq_path)
            
            # Shuffle-Node unter dem Beauty-Read
            shuffle_node = nuke.createNode("Shuffle")
            shuffle_node.setInput(0, aov_read)    # Input A = AOV
            shuffle_node.setInput(1, beauty_read) # Input B = Beauty
            
            shuffle_node['in'].setValue('rgba')   # Input A Channels
            #shuffle_node['postage'].setValue(0)   # optional, nur wenn du willst
            
            # Den Output-Kanal auf den Namen des AOVs setzen
            shuffle_node['label'].setValue(folder_name)
            #shuffle_node['postage'].setValue(0)
            shuffle_node['in2'].setValue('rgba')  # Input B = Beauty

            # Output auf neuen Channel legen
            #shuffle_node['postage'].setValue(0)
            shuffle_node['label'].setValue(folder_name)
            shuffle_node['red'].setValue('red')
            shuffle_node['green'].setValue('green')
            shuffle_node['blue'].setValue('blue')
            shuffle_node['alpha'].setValue('alpha')

    nuke.message("AOV-Shuffles unter Beauty erstellt!")

create_aov_shuffles_under_beauty()

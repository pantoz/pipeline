import nuke
import os
import re

# Sicherstellen, dass ein Read-Node ausgewählt ist
selected_nodes = nuke.selectedNodes('Read')
if not selected_nodes:
    nuke.message("Bitte wähle einen Read-Node aus.")
else:
    read_node = selected_nodes[0]
    file_path = nuke.filename(read_node).replace("\\", "/")

    # Split und Parent/Current Folder bestimmen
    path_parts = file_path.split("/")[:-1]
    if len(path_parts) < 2:
        nuke.message("Pfad zu kurz.")
    else:
        parent_folder = "/".join(path_parts[:-1])
        current_folder = path_parts[-1]

        # Alle anderen Ordner auf derselben Ebene
        sibling_folders = [f for f in os.listdir(parent_folder)
                           if os.path.isdir(os.path.join(parent_folder, f)) and f != current_folder]

        # 🔹 Progress Bar starten
        task = nuke.ProgressTask("Loading AOV sequences")
        total = int(len(sibling_folders))
        i = 1
        # Startposition im Nodegraph
        xpos = read_node['xpos'].value() + 120 
        ypos = read_node['ypos'].value() + 160  # initial 60 px unter dem selektierten Node

        last_shuffle = read_node
#######GRUPPE#################################
        group = nuke.createNode("Group")
        group['xpos'].setValue(read_node['xpos'].value())
        group['ypos'].setValue(read_node['ypos'].value()+160)
        group['label'].setValue('AOVS')
        group.begin()

        group_input = nuke.createNode("Input")
        group_input['xpos'].setValue(xpos-120)
        group_input['ypos'].setValue(ypos-160)

        last_shuffle = group_input


        for folder_name in sorted(sibling_folders):
            i = i+1
            length = int(len(sibling_folders))
            #print (i)
            folder_path = os.path.join(parent_folder, folder_name)
            if task.isCancelled():
                group.end()
                break
            task.setMessage("Loading: {}".format(folder_name))


            # EXR-Dateien im Ordner
            exr_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.exr')])
            if not exr_files:
                continue  # Ordner überspringen, falls keine EXRs

            first_file = exr_files[0]
            # Sequenz-Pfad mit ####
            seq_path = os.path.join(folder_path, first_file).replace("\\", "/")
            seq_path = re.sub(r'\d+(?=\.exr$)', '####', seq_path)

            # Read-Node erstellen
            new_read = nuke.createNode("Read")
            new_read['file'].setValue(seq_path)

            # Frame Range vom originalen Read übernehmen
            new_read['first'].setValue(int(read_node['first'].getValue()))
            new_read['last'].setValue(int(read_node['last'].getValue()))
            new_read['origfirst'].setValue(int(read_node['origfirst'].getValue()))
            new_read['origlast'].setValue(int(read_node['origlast'].getValue()))

            # Nodegraph-Position setzen
            new_read['xpos'].setValue(xpos)
            new_read['ypos'].setValue(ypos)

            # shuffle-Node
            new_shuffle = nuke.createNode("Shuffle2")
            
            new_shuffle.setInput(1, new_read)
            new_shuffle.setInput(0, last_shuffle)
            new_shuffle['fromInput2'].setValue(1)  
            new_shuffle['in2'].setValue("rgb") 
            print (folder_name)
            nuke.Layer(folder_name, [folder_name+'.red', folder_name+'.green',folder_name+'.blue'])
            new_shuffle['out2'].setValue(folder_name) 
            new_shuffle["mappings"].setValue( [(1, 'rgba.red',folder_name+'.red'), (1, 'rgba.green', folder_name+'.green'), (1, 'rgba.blue', folder_name+'.blue')])       
            
            new_shuffle['xpos'].setValue(read_node['xpos'].value())
            new_shuffle['ypos'].setValue(ypos)
            
            last_shuffle = new_shuffle

            # Nächster Node 20 px tiefer
            ypos += 120
            


            print(f"Loaded sequence from: {seq_path}")
            progress = int(((i/length)*100)+1)
            print (progress)
            if progress >= 100:
                group_output = nuke.createNode("Output")
                group_output.setInput(0, last_shuffle)

                group.end()

                task.setProgress(100)
                task = None
                #break
            else:
                
                task.setProgress(progress)

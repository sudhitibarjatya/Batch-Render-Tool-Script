import nuke
import os
import time


def batch_render_tool():
    
    settings = nuke.Root()
    default_first_frame = int(settings["first_frame"].value())
    default_last_frame = int(settings["last_frame"].value())
    all_nodes = nuke.allNodes()

    #Looping till the user enters valid input data

    while True:
        
        #Initializing Variables

        write_nodes_sorted = []
        render_times = []
        write_nodes = []
     
        #Initializing exit_loop variable
        exit_loop = True

        panel = nuke.Panel("Batch Render Tool")
        panel.addFilenameSearch("Root Output Directory:","")              
       
        #Creating gui input for write nodes and their execution order 
        #The user can choose which write node to render and in what order
        #Adding write nodes to write_nodes list
        index = 1
        for node in all_nodes:
            if node.Class() == 'Write':
                write_nodes.append(node)
                node_name = node.name()
                panel.addBooleanCheckBox(node_name, True)
                panel.addSingleLineInput(node_name+' Execution Order:', index)
                index += 1

        #Breaking out of the loop if there are no write nodes in the scene
        if len(write_nodes) == 0:
            nuke.message("No write to render.")
            break



        panel.addEnumerationPulldown('File Format:', 'png exr mov')
        panel.addEnumerationPulldown('Image Sequence Padding:', '%03d %04d %05d')
        panel.addSingleLineInput('First Frame:', default_first_frame)
        panel.addSingleLineInput('Last Frame:', default_last_frame)
        panel.addButton('Cancel')
        panel.addButton('Validate')


        result = panel.show()

        #If the user clicks the Validate Button 
        if result == 1:

            write_nodes_length = len(write_nodes)
            previous_order_number = 0  
            
            root = panel.value('Root Output Directory:')
            first_frame = panel.value('First Frame:')
            last_frame = panel.value('Last Frame:')

            #Assigning exit_loop variable as false for errors
            #Checking if the selected file path exists
            if not os.path.exists(root):
                 nuke.message("Please enter a vaild root path.")
                 exit_loop = False

            #Checking if the first_frame and last_frame input are integers
            try:
                int_value = int(first_frame)
            except ValueError:
                nuke.message("Invalid input. Please enter an integer for first frame input.")
                exit_loop = False
            
            try:
                int_value = int(last_frame)
            except ValueError:
                nuke.message("Invalid input. Please enter an integer for last frame input.")
                exit_loop = False

            #Looping over  write_nodes to check if the execution order is valid
            for write_node in write_nodes:

                node_name = write_node.name()
                order_number = panel.value(node_name +' Execution Order:')
                
                #Checking if the order_number input for the write node is integer
                try:
                    int_value = int(order_number)

                except ValueError:
                    nuke.message("Invalid input. Please enter an integer for execution order.")
                    exit_loop = False
                    break

                #Checking if all the order numbers are unique leaving when they are 0
                if order_number is previous_order_number and int(order_number) != 0:
                    nuke.message("Repetition. Please enter unique order numbers.")
                    exit_loop = False
                    break       

                #Checking if order_number is greater than the number of write nodes in the graph
                if int(order_number) > write_nodes_length:
                    nuke.message("Order number has to be less than {}".format(write_nodes_length))
                    exit_loop = False
                    break

     
                previous_order_number = order_number

        #if user cancels the batch rendering operation,break out of the loop
        if result == 0:
            break
        
        #If the exit loop variable remains true that means the data entered is valid
        if exit_loop:

            #Show a new panel to confirm from the user if they want to continue the operation
            render_panel = nuke.Panel("Render")
            render_panel.addButton('Cancel')
            render_panel.addButton('Validation Complete! Click to start batch rendering.')
            render_panel_result = render_panel.show()
            
            #Perform Batch Rendering Operation 
            if render_panel_result:
                
                #Rearrange write nodes in the execution order and store it in the write_nodes_sorted list   
                for write_node in write_nodes:

                    write_node_name = panel.value(write_node.name()) 

                    if write_node_name:
                        node_name = write_node.name()
                        order_number = int(panel.value(node_name +' Execution Order:'))
                        write_nodes_sorted.insert(order_number-1,write_node)
                        
                #Loop over write nodes sorted list to set parameters and execute the write nodes
                for node in write_nodes_sorted:
                    absolute_path = "" 
                    folder_name = node.name()
                    selected_padding = panel.value('Image Sequence Padding:')
                    selected_file_type  = panel.value('File Format:')


                    #Creating absolute file path for diffrent file_types
                    #Setting file types
                    if selected_file_type == "png" or selected_file_type == "exr":
                        absolute_path = "{}/{}/{}.{}.{}".format(root,folder_name,folder_name,selected_padding,selected_file_type)
                        node["file_type"].setValue(selected_file_type)
      
                    else:
                        absolute_path = "{}/{}/{}.{}".format(root,folder_name,folder_name,selected_file_type)
                        node["file_type"].setValue(selected_file_type)
                        node["mov64_codec"].setValue("h264")

                    node["file"].setValue(absolute_path)
                    node['create_directories'].setValue("True")

                    #Storing the time when nuke begins execution in start_frame_variable
                    start_time = time.time()
      
                    nuke.execute(node, int(first_frame), int(last_frame), 1)

                    #Storing the time when nuke stops execution in end_frame_variable
                    end_time = time.time()
                    
                    #Calculating render time and storing it in render_times list
                    render_time = end_time - start_time
                    render_times.append("Render time for {}: {} seconds".format(node.name(),render_time))

                #Convert List to string
                all_render_times = "\n".join(render_times)
                
      
                nuke.message("TASK COMPLETED! \n"+all_render_times)

                break

            #Breaking out of the loop as user canceled the operation
            else:
                nuke.message("Render Canceled")
                break
        

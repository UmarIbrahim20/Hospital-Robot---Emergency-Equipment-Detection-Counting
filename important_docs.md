## ROS2 Workspace Template

This repository serves as a template for creating ROS2 packages, equipped with a basic CI workflow and devcontainer configuration.

### Development Environment Setup

To begin development in a containerized environment:

1. **Use this repo as a template (You only do this once!):**
   The best way to work with this repo is to use it as a template for your ROS package development, to do so, in the top right corner select `Use this template` and then `Create new repository`:
   <img width="715" alt="image" src="https://github.com/user-attachments/assets/1d60f491-5e35-4bed-be62-3d35aba7e6b7">

   Alternatively, you may choose to "Fork" the repository ([read here about the differences](https://docs.github.com/en/enterprise-server@2.22/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)). However, if you create a "fork" your repository will be public, which you may want to avoid for assessed work.

   Then, in the next step specify the owner (yourself) and the repository name (e.g. `cmp3103`) you want to create as shown below (You are recommended to make this a _private_ repository until the marking of the assessment is complete):

   <img width="735" alt="image" src="https://github.com/user-attachments/assets/8b48fb41-d389-432b-80c4-9f623bc3f793">

   You will end up having your own repository, which looks something like this:

   <img width="923" alt="image" src="https://github.com/user-attachments/assets/dacc7fa2-43d5-46ce-94cb-1231ab63f4f3">


2. **Open in Visual Studio Code:**
   Open your new repository in VSCode. The easiest way is to go to the git tab in VSCode and select `Clone Repository` and then copy the URL to the repository into the dialog that opens, e.g. `https://github.com/marc-hanheide/my-cmp3103-ws` in the example case. Then, choose the local folder you want to repository to be checked out into and choose to open the new workspace.

   <img width="577" alt="image" src="https://github.com/user-attachments/assets/71c78415-4461-464a-8b65-3ec046108846">

   After cloning the repository and opening it, VSCode will prompt you if you want to "Reopen in Container", as it has found a devContainer configuration. You should say "yes". Alternatively if you don't see the prompt, you can use the command palette (`Ctrl+Shift+P`) and search for the "Reopen in Container" command.

   <img width="451" alt="image" src="https://github.com/user-attachments/assets/6f4d2df4-bcb5-4887-8009-427aab59037c">

3. **Container Setup:**
   Once reopened in the container, VSCode will initiate the building process and pull all necessary dependencies. You can monitor the building log within VSCode. This may take a while (in particular if you have not previouly used the computer with the container), as you entire image with all installations is being pulled.
   
   <img width="485" alt="image" src="https://github.com/user-attachments/assets/c3b8202c-dc8e-4f04-a80d-09bc1719a7d0">


5. **Verify Container Environment:**
   After the build completes, VSCode will connect to the container. You can verify that you are within the container environment.

   <img width="1746" alt="image" src="https://github.com/user-attachments/assets/47f9f505-d913-4b2c-a805-3d3ef0809751">
   
   See bottom left, saying "Dev Container":
   <img width="311" alt="image" src="https://github.com/user-attachments/assets/04662426-e7ff-4a00-9838-14e125767895">

   You can now open the virtual desktop (see next section) or a terminal in VSCode inside the DevContainer:
   
   <img width="1158" alt="image" src="https://github.com/user-attachments/assets/088b150f-5cb7-4c0d-b18a-448944f15ffa">


### Devcontainer Features

The devcontainer includes a virtual 3D accelerated (if the host has an NVIDIA GPU and docker runtime installed) desktop.


1. **Accessing the Desktop Interface:**
   Open the user interface by navigating to the `PORTS` tab in VSCode, selected the URL labeled `desktop` to open it in your browser. You can also right-click on the URL it and choose "Preview in Editor" to have that desktop shown directly in VSCode, instead.

   <img width="934" alt="image" src="https://github.com/user-attachments/assets/d90e90ed-3d46-465a-8589-0f96fee5cff2">

2. **Complete the connection:**
   Click on "Connect".

   <img width="404" alt="image" src="https://github.com/user-attachments/assets/33a370cb-6063-4242-ba34-c4997050dcae">

   Your desktop will open. If you want the size of this virtual desktop to adjust automatically to your browser window, choose "Remote Resizing" in the options on the left hand side.

   <img width="276" alt="image" src="https://github.com/user-attachments/assets/d455cb56-4eda-400d-bef2-bf1aa2ef1ca0">

### Enjoy Development!

By leveraging this setup, you can develop on a remote machine with a lightweight desktop interface. Magic! Furthermore, this template package provides very nice ROS2 functionality like syntax highlight and template code generation. 

You can now use the VSCode terminal to launch all the commands you need and run code directly from VSCode in your devcontainer. Any windows you open from the terminal or from your code will appear in the virtual desktop (i.e. you Browser).

**All ROS2 packages should go into the `src/` folder. Create them with `ros2 pkg create...`.**

**The devcontainer installs all dependencies of the workspace automatically as much as possible, and also tries to build the workspace when it is created, to speed up later colcon builds.**

### References

1. [cmp3103-ws](https://github.com/UoL-SoCS/cmp3103-ws)
2. [Get Started with Dev Containers in VS Code](https://youtu.be/b1RavPr_878?si=ADepc_VocOHTXP55)


## ROS2 Workspace Template

This repository serves as a template for creating ROS2 packages, equipped with a basic CI workflow and devcontainer configuration.

### Development Environment Setup

To begin development in a containerized environment:

1. **Use this repo as a template (You only do this once!):**
   The best way to work with this repo is to use it as a template for your ROS package development, to do so, in the top right corner select `Use this template` and then `Create new repository`:
   <img width="715" alt="image" src="https://github.com/user-attachments/assets/1d60f491-5e35-4bed-be62-3d35aba7e6b7">

   Alternatively, you may choose to "Fork" the repository ([read here about the differences](https://docs.github.com/en/enterprise-server@2.22/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)). However, if you create a "fork" your repository will be public, which you may want to avoid for assessed work.

   Then, in the next step specify the owner (yourself) and the repository name (e.g. `cmp3103`) you want to create as shown below (You are recommended to make this a _private_ repository until the marking of the assessment is complete):

   <img width="735" alt="image" src="https://github.com/user-attachments/assets/8b48fb41-d389-432b-80c4-9f623bc3f793">

   You will end up having your own repository, which looks something like this:

   <img width="923" alt="image" src="https://github.com/user-attachments/assets/dacc7fa2-43d5-46ce-94cb-1231ab63f4f3">


2. **Open in Visual Studio Code:**
   Open your new repository in VSCode. The easiest way is to go to the git tab in VSCode and select `Clone Repository` and then copy the URL to the repository into the dialog that opens, e.g. `https://github.com/marc-hanheide/my-cmp3103-ws` in the example case. Then, choose the local folder you want to repository to be checked out into and choose to open the new workspace.

   <img width="577" alt="image" src="https://github.com/user-attachments/assets/71c78415-4461-464a-8b65-3ec046108846">

   After cloning the repository and opening it, VSCode will prompt you if you want to "Reopen in Container", as it has found a devContainer configuration. You should say "yes". Alternatively if you don't see the prompt, you can use the command palette (`Ctrl+Shift+P`) and search for the "Reopen in Container" command.

   <img width="451" alt="image" src="https://github.com/user-attachments/assets/6f4d2df4-bcb5-4887-8009-427aab59037c">

3. **Container Setup:**
   Once reopened in the container, VSCode will initiate the building process and pull all necessary dependencies. You can monitor the building log within VSCode. This may take a while (in particular if you have not previouly used the computer with the container), as you entire image with all installations is being pulled.
   
   <img width="485" alt="image" src="https://github.com/user-attachments/assets/c3b8202c-dc8e-4f04-a80d-09bc1719a7d0">


5. **Verify Container Environment:**
   After the build completes, VSCode will connect to the container. You can verify that you are within the container environment.

   <img width="1746" alt="image" src="https://github.com/user-attachments/assets/47f9f505-d913-4b2c-a805-3d3ef0809751">
   
   See bottom left, saying "Dev Container":
   <img width="311" alt="image" src="https://github.com/user-attachments/assets/04662426-e7ff-4a00-9838-14e125767895">

   You can now open the virtual desktop (see next section) or a terminal in VSCode inside the DevContainer:
   
   <img width="1158" alt="image" src="https://github.com/user-attachments/assets/088b150f-5cb7-4c0d-b18a-448944f15ffa">


### Devcontainer Features

The devcontainer includes a virtual 3D accelerated (if the host has an NVIDIA GPU and docker runtime installed) desktop.


1. **Accessing the Desktop Interface:**
   Open the user interface by navigating to the `PORTS` tab in VSCode, selected the URL labeled `desktop` to open it in your browser. You can also right-click on the URL it and choose "Preview in Editor" to have that desktop shown directly in VSCode, instead.

   <img width="934" alt="image" src="https://github.com/user-attachments/assets/d90e90ed-3d46-465a-8589-0f96fee5cff2">

2. **Complete the connection:**
   Click on "Connect".

   <img width="404" alt="image" src="https://github.com/user-attachments/assets/33a370cb-6063-4242-ba34-c4997050dcae">

   Your desktop will open. If you want the size of this virtual desktop to adjust automatically to your browser window, choose "Remote Resizing" in the options on the left hand side.

   <img width="276" alt="image" src="https://github.com/user-attachments/assets/d455cb56-4eda-400d-bef2-bf1aa2ef1ca0">

### Enjoy Development!

By leveraging this setup, you can develop on a remote machine with a lightweight desktop interface. Magic! Furthermore, this template package provides very nice ROS2 functionality like syntax highlight and template code generation. 

You can now use the VSCode terminal to launch all the commands you need and run code directly from VSCode in your devcontainer. Any windows you open from the terminal or from your code will appear in the virtual desktop (i.e. you Browser).

**All ROS2 packages should go into the `src/` folder. Create them with `ros2 pkg create...`.**

**The devcontainer installs all dependencies of the workspace automatically as much as possible, and also tries to build the workspace when it is created, to speed up later colcon builds.**

### References

1. [cmp3103-ws](https://github.com/UoL-SoCS/cmp3103-ws)
2. [Get Started with Dev Containers in VS Code](https://youtu.be/b1RavPr_878?si=ADepc_VocOHTXP55)




fire extenghusher : 21
first aid : 15
fire exit door : 5


### Notes :

` before starting navigation , first start gazebo so that time will synx `

Use the "Current Directory" Trick
Instead of giving a long path, navigate into the folder first and save it there. This bypasses path resolution errors:

Bash

cd ~/workspaces/cmp9767-MdUmarIbrahim-module/src/hospital_sim_navigation/maps/
ros2 run nav2_map_server map_saver_cli -f hospital_map_first

os@4d6fcf12c205:/opt/ros/lcas/install$ 

rviz2 -d /opt/ros/lcas/install/limo_description/share/limo_description/rviz/model_sensors_real.rviz

sudo apt update && sudo apt install ros-humble-rqt-tf-tree
ros2 run rqt_tf_tree rqt_tf_tree
ros2 run tf2_ros tf2_echo

sudo apt-get install ros-humble-rqt-image-view
ros2 run rqt_image_view rqt_image_view --ros-args -r image:=/limo/depth_camera_link/image_raw

ros2 bag record [-o bagfilename] <topics>
ros2 bag play <filename>

1.1 These values can be dynamically reconfigured on the fly by opening ros2 run rqt_gui rqt_gui or by simply typing rqt from the console and then from the menu bar Plugins/Configuration/Dynamic Reconfigure. Please select global_costamp or local_costamp in the menu on the left, and you should be able to visualise all the parameters you can change.

world coordinates:
left top: -14.795800 -0.036803 0        right top: 14.795800 0.036803 0

lett bottom: -14.795800 -6.109800 0     right bottom: 14.795800 -6.089250 0

robot spawing should cover in y axis : from -0.036803 to -6.109800
robot spawing should cover in x axis : from -14.795800 to 14.795800

cd /workspaces/cmp9767-MdUmarIbrahim-module/src/hospital_sim_dataset/hospital_yolo

# Create batch 2 (next 200 images)
mkdir -p test_batch_6
for i in {1000..1199}; do
    cp images/test/$(printf "%06d" $i).png test_batch_5 2>/dev/null
done

mkdir -p upload_batch_2
for i in {100..299}; do
    cp images/train/$(printf "%06d" $i).png upload_batch_2/ 2>/dev/null
done

cd /workspaces/cmp9767-MdUmarIbrahim-module

# Install YOLOv8 and dependencies
pip3 install ultralytics
pip3 install opencv-python
pip3 install numpy

# Verify installation
python3 -c "from ultralytics import YOLO; print('✓ YOLOv8 installed successfully')"

ros2 pkg create hospital_sim_perception \
    --build-type ament_python \
    --dependencies rclpy sensor_msgs std_msgs cv_bridge


# First, verify your model exists
ls -lh /workspaces/cmp9767-MdUmarIbrahim-module/src/hospital_sim_perception/hospital_sim_perception/weights/best.pt

# Run with explicit model path (bypasses config file)
ros2 run hospital_sim_perception yolo_node \
  --ros-args \
  -p model_path:=/workspaces/cmp9767-MdUmarIbrahim-module/src/hospital_sim_perception/weights/best.pt \
  -p camera_topic:=/limo/depth_camera_link/image_raw

src/hospital_sim_perception/weights/best.pt
pip install "numpy<2.0"

sudo apt update
sudo apt install ros-humble-rqt*   

rm -rf /home/ros/.local/lib/python3.10/site-packages/torch*
rm -rf /home/ros/.local/lib/python3.10/site-packages/ultralytics*

# Force delete the numpy folder from your local user directory
rm -rf /home/ros/.local/lib/python3.10/site-packages/numpy*

# Delete the actual library folder
rm -rf /home/ros/.local/lib/python3.10/site-packages/cv2

# Delete the package metadata (version info)
rm -rf /home/ros/.local/lib/python3.10/site-packages/opencv_python*

pip3 install opencv-python==4.8.1.78 
pip install numpy==1.24.3 --user
pip install opencv-python==4.8.1.78 --user
pip install --user --force-reinstall "torch==2.4.1" "torchvision==0.19.1" "torchaudio==2.4.1" --index-url https://download.pytorch.org/whl/cu121

pip install ultralytics==8.0.200 --user


pip3 install torch==2.4.1 torchvision==0.19.1 --user --index-url https://download.pytorch.org/whl/cpu
pip install --user "torch==2.4.1" "torchvision==0.19.1" "torchaudio==2.4.1" --index-url https://download.pytorch.org/whl/cpu

python3 << 'EOF'
import torch
print(f"PyTorch Version: {torch.__version__}")
if "2.6" in torch.__version__:
    print("❌ Still on version 2.6 (Too New)")
else:
    print("✅ Successfully downgraded!")
EOF

pip install --user --force-reinstall "torch==2.4.1" "torchvision==0.19.1" "torchaudio==2.4.1" --index-url https://download.pytorch.org/whl/cu121

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/ros/.local/lib/python3.10/site-packages/nvidia/cudnn/lib

pip install Pillow

pip install --upgrade pip
pip install "torch==2.4.1" "torchvision==0.19.1" "torchaudio==2.4.1" \
    --index-url https://download.pytorch.org/whl/cu121
pip install ultralytics==8.0.200 opencv-python numpy

pip show ultralytics numpy opencv-python torch
pip install Flask





sudo apt install ros-humble-nav2-simple-commander

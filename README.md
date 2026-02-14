# AlohaScorpion

<p align="center">
  <img src="assets/top_image.jpg" alt="AlohaScorpion_top" width="90%" />
</p>

AlohaScorpion is a 7 dof + gripper, dual-arm mobile manipulator with lift. It is designed for research and development in robotics, particularly in manipulation and mobile robotics.
This project is heavily inspired by the 

- Lerobot(https://github.com/k1000dai/lerobot)
- Alohamini(https://github.com/liyiteng/AlohaMini)
- Xlerobot(https://github.com/Vector-Wangel/XLeRobot)
- DualScorpion(https://github.com/momoiorg-repository/dual_scorpion)
- PincOpen(https://github.com/pollen-robotics/PincOpen)


## Update Log 
2/14 : Updated to the version 2.0. Better BOM, better chassis design, better arm position, pincopen gripper.

## To Do

- [ ] Add more details to the assembly instructions.
- [ ] Support VLA training.
- [ ] Support URDF and simulators.

## Images
<p align="center">
  <img src="assets/IMG_5167.jpg" alt="AlohaScorpion" width="45%" />
  <img src="assets/leader.jpg" alt="leader" width="45%" />
</p>
## Features
- 7 degrees of freedom per arm for enhanced manipulation capabilities. inspired by dual_scorpion

- Gripper for object handling. We use the PincOpen gripper, which is open-source parallel-finger gripper, derived from Pollen Robotics Reachy 2's gripper. It is compatible with the arms of AlohaScorpion.

- Mobile base for navigation and mobility. based on alohamini.

- Lift mechanism for vertical movement. based on Alohamini.

- Data collection and logging capabilities for research purposes. based on the lerobot framework.

- Large battery capacity for extended operation time. based on the Xlerobot. Use Anker Solix C300 Portable Power Station 288Wh.

## Bill of Materials (BOM)
The complete Bill of Materials (BOM) can be found in the this Google Sheet : https://docs.google.com/spreadsheets/d/1W7IXB0Fid7SDyZUYEEcC63fRW-HXA5QO-rrAWQz4-Ek/edit?usp=sharing.

If you want to use  parallel-finger gripper, you can refer PincOpen github repository[https://github.com/pollen-robotics/PincOpen] for the BOM and assembly instructions. The gripper is compatible with the arms of AlohaScorpion. You need to use the updated mount plate in hardware/misc/stl/sointerface.stl.


## Assembly Instructions
Please see AlohaMini's assembly instructions as the mobile base and lift mechanism are almost the same.

Also, for the arms, please follow the dual_scorpion's assembly instructions. In order to keep the motor id, we use the 0 ~ 
7 motor for the arms. 8,9,10,11 motors are used for the mobile base and lift mechanism.


## Software

### Environment Setup
We setup the host with jetson nano. You can also use any PC or raspberry pi 5 as the host.

if you use raspberry pi 5 or PC, please follow the instructions below to setup conda environment.
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
source ~/.bashrc
conda create -y -n lerobot_alohamini python=3.10
conda activate lerobot_alohamini
cd ~/lerobot_alohamini
pip install -e .[all]
conda install ffmpeg=7.1.1 -c conda-forge
```


if you stack with jetson nano, please follow the instructions below to setup conda environment.
```
conda create -y -n lerobot_alohamini python=3.10
conda activate lerobot_alohamini
conda install -c conda-forge pyarrow
# remove torchvision and rerun-sdk, datasets
pip install -e .[feetech]
conda install -c huggingface -c conda-forge datasets
conda install ffmpeg=7.1.1 -c conda-forge
pip install torchvision==0.20.1
pip install zmq
```

### Running the Software
#### teleoperation
host side
```
python -m lerobot.robots.alohamini_scorpion.lekiwi_host
```

client side
```
python examples/alohamini_scorpion/teleoperate_bi.py \
--remote_ip ip_address_of_host \
```

#### data collection
host side
```
python -m lerobot.robots.alohamini_scorpion.lekiwi_host
```
client side
```
python examples/alohamini_scorpion/record_bi.py \
--remote_ip ip_address_of_host \
--dataset user/my_dataset_name 
```

#### Replay
host side
```
python -m lerobot.robots.alohamini_scorpion.lekiwi_host
```

client side
```
python examples/alohamini_scorpion/replay_bi.py \
--remote_ip ip_address_of_host \
--dataset user/my_dataset_name
```

#### VLA training
```
lerobot-train \
  --dataset.repo_id=k1000dai/alohascorpion_pick_plate_put_box \
  --policy.type=act \
  --output_dir=outputs/train/alohascorpion_pick_plate_put_box\
  --job_name=alohascorpion_act \
  --policy.device=cuda \
  --wandb.enable=true \
  --policy.repo_id=k1000dai/alohascorpion_act
```

#### Evaluation model
```
python examples/alohamini/evaluate_bi.py \
  --num_episodes 3 \
  --fps 20 \
  --episode_time 45 \
  --task_description "Pick and place task" \
  --hf_model_id liyitenga/act_policy \
  --hf_dataset_id liyitenga/eval_dataset \
  --remote_ip 127.0.0.1 \
  --robot_id my_alohamini \
  --hf_model_id ./outputs/train/act_your_dataset1/checkpoints/020000/pretrained_model
```
## License
This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.


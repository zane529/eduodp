
## Service Workbench with SageMaker Notebook Template @ml.g5.8xlarge

### Setup SageMaker jupyterlab in AWS Console

    1  Notebook Instance Type: ml.g5.8xlarge
    2  Platform Identifier: Amazon Linux 2, Jupyter Lab 3(notebook-al2-v2)
    3  Volume Size: 100GB EBS
    4  Minimum IMDS Version: 2

### Use Mode JupyterLab

    1  Setup Terminal in JupyterLab for lateron inputs. 

### Git Repository Setup

    1  cd SageMaker && git clone https://github.com/ddipass/ODP_Demo.git && exit

### Leafmap on SageMaker Studio Lab / Easy online access notes

    1  fast_deploy.sh

### SageMaker Jupyter Lab Extension Check

    1  jupyter labextension list

### Kernel Selection

    1  python3(ipykernel)
    
### Monitor CUDA Memory Usage

    1  conda install -c conda-forge nvitop
    2  [Terminal Command] # nvitop

### Check Disk & Log

    1  df -h
    2  history




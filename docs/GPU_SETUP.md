# *GPU* visibility check

The presence of the machine's access to *NVIDIA GPU* can be verified using the following command:

```bash
lspci | grep -i nvidia
```

In case *GPU* is visible after executing the above command, then we can check the *GPU* visibility in this way:

```bash
nvidia-smi
```
> **NOTE:** Successful run of the above command will display the information about the *GPU* in a table. Error might signal that the machine does not have *NVIDIA* drivers installed.

## Installing *NVIDIA* drivers (in case of their absence)

In order to install the required drivers one needs to firstly check the recommended drivers version in this way:

```bash
ubuntu-drivers devices
```

In the resulting output we would need to find a row similar to the one below:

```
driver   : nvidia-driver-XXX - distro non-free recommended
```
> where XXX - recommended driver version for the current machine

Now we are installing the *NVIDIA* drivers replacing `XXX` with the version number shown in the output of the command above (installation may take some time):
```bash
sudo apt install nvidia-driver-XXX
```

After drivers installation we need to reboot the machine so that the drivers would get loaded into the system:

```bash
sudo reboot
```
> After reboot, command `nvidia-smi` should show the *GPU* accessible to the machine.

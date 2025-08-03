import torch

print("Torch version:", torch.__version__)
print("CUDA built-in version:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("Current device:", torch.cuda.current_device())
print("Device name:", torch.cuda.get_device_name(0))

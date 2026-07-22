import sys
import torch
import transformers
import datasets

print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}, CUDA available: {torch.cuda.is_available()}")
print(f"Transformers: {transformers.__version__}")
print(f"Datasets: {datasets.__version__}")
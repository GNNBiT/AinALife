# clear.py
import torch
import gc

def clear_cuda():
    """Очищает память CUDA и собирает мусор."""
    print("[CLEAR] Cleaning CUDA memory...")

    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()

    print("[CLEAR] CUDA memory cleared.")

if __name__ == "__main__":
    clear_cuda()

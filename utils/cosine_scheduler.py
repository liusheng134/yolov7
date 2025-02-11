import torch
import numpy as np


def warm_up_cosine_lr_scheduler(optimizer, steps=100, warm_up_steps=5, eta_min=1e-9, lrf=0.001):
    """
    Description:
        - Warm up cosin learning rate scheduler, first epoch lr is too small
    
    Arguments:
        - optimizer: input optimizer for the training
        - epochs: int, total epochs for your training, default is 100. NOTE: you should pass correct epochs for your training
        - warm_up_epochs: int, default is 5, which mean the lr will be warm up for 5 epochs. if warm_up_epochs=0, means no need
          to warn up, will be as cosine lr scheduler
        - eta_min: float, setup ConsinAnnealingLR eta_min while warm_up_epochs = 0

    Returns:
        - scheduler
    """
    
    if warm_up_steps <= 0:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=steps, eta_min=eta_min)
    
    else:
        warm_up_with_cosine_lr = lambda step: eta_min + (step / warm_up_steps) if step <= warm_up_steps else max(0.5 * (
            np.cos((step - warm_up_steps) / (steps - warm_up_steps) * np.pi) + 1), lrf)
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=warm_up_with_cosine_lr)
    
    return scheduler

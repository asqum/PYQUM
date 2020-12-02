import os
import numpy as np
import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import time
import pytorchtools as tools
from PIL import Image
import myfunctions as my

workspace_dir = './output_test'
test_x, test_y = my.readfile(os.path.join(workspace_dir, "testing"), True)
print("Size of Testing data = {}".format(len(test_x)))
cpu = torch.device("cpu")
gpu = torch.device("cuda")
model = tools.maxout_conv_net(4).to(gpu)
model.load_state_dict(torch.load('digitalnetwork_3.pkl'))
print("success")
test_transform = transforms.Compose([
    transforms.ToPILImage(),                                    
    transforms.ToTensor(),
])
batch_size = 150
test_set = tools.DigitDataset(test_x, test_y, transform=test_transform)
test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)
model.eval()
test_acc = 0.0
test_loss = 0.0
loss = nn.CrossEntropyLoss()
with torch.no_grad():
  for i, data in enumerate(test_loader):
    epoch_start_time = time.time()
    test_pred = model(data[0].to(gpu))
    batch_loss = loss(test_pred, data[1].to(gpu))

    test_acc += np.sum(np.argmax(test_pred.to(cpu).data.numpy(), axis=1) == data[1].numpy())
    test_loss += batch_loss.item()
    print("the predicted numbers: ")
    print(np.argmax(test_pred.to(cpu).data.numpy(), axis=1))
    print("the true patterns of number:")
    print(data[1].numpy())
  #print out accuracy and loss
  print('%2.2f sec(s) Test Acc: %3.6f Loss: %3.6f' % \
      (time.time()-epoch_start_time, \
      test_acc/test_set.__len__(), test_loss/test_set.__len__()))
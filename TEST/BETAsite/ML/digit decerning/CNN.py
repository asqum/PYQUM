# Import library(toolkit) for deep learning
import numpy as np
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
import pytorchtools as tools
import pandas as pd
import time
import myfunctions as my

# read data
workspace_dir = './output'
print("Reading data")
train_x, train_y = my.readfile(os.path.join(workspace_dir, "training"), True)
print("Size of training data = {}".format(len(train_x)))
test_x, test_y = my.readfile(os.path.join(workspace_dir, "testing"), True)
print("Size of Testing data = {}".format(len(test_x)))

train_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomRotation((-15,15)),                                    
    transforms.ToTensor(),
])
test_transform = transforms.Compose([
    transforms.ToPILImage(),                                    
    transforms.ToTensor(),
])

train_x, train_y = my._shuffle(train_x, train_y)
train_x, train_y, val_x, val_y = my._train_dev_split(train_x, train_y, 0.2)
batch_size = 150
train_set = tools.DigitDataset(train_x, train_y, train_transform)
train_loader = DataLoader(train_set, batch_size=batch_size, shuffle = True)
print("Size of training data = {}".format(len(train_x)))
val_set = tools.DigitDataset(val_x, val_y, test_transform)
val_loader = DataLoader(val_set, batch_size=batch_size, shuffle = False)
print("Size of validation data = {}".format(len(val_x)))

#training model
cpu = torch.device("cpu")
gpu = torch.device("cuda:0")
model = tools.maxout_conv_net(4).to(gpu)
model.load_state_dict(torch.load('digitalnetwork_3.pkl'))
patience = 3
loss = nn.CrossEntropyLoss() # since now it is problem about classification, we would use croos entropy to be our loss function
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001) # Adam is a optimizer with momentum, avoiding stucked at saddle points or local minimum
num_epoch = 15
trainingtime = 10
early_stopping = tools.EarlyStopping(patience = patience, verbose=True)
for i in range(trainingtime):
  if i > 0:
    train_x, train_y = my._shuffle(np.concatenate((train_x, val_x), axis = 0), np.concatenate((train_y, val_y), axis = 0))
    train_x, train_y, val_x, val_y = my._train_dev_split(train_x, train_y, 0.2)
    train_set = tools.DigitDataset(train_x, train_y, train_transform)
    train_loader = DataLoader(train_set, batch_size = batch_size, shuffle = True)
    val_set = tools.DigitDataset(val_x, val_y, test_transform)
    val_loader = DataLoader(val_set, batch_size = batch_size, shuffle = False)
    early_stopping.refresh()
  
  for epoch in range(num_epoch):
    epoch_start_time = time.time()
    train_acc = 0.0
    train_loss = 0.0
    val_acc = 0.0
    val_loss = 0.0

    model.train() # ensure model in train mode(for dropout)
    for i, data in enumerate(train_loader):
        optimizer.zero_grad() # we have to set gradient to be zero before new decending
        train_pred = model(data[0].to(gpu)) #use model to get the predicted probabilities distrubution, which actually is done by calling forward function in the model
        batch_loss = loss(train_pred, data[1].to(gpu)) # to calculate out loss, noting prediction and label should be simultaneously on CPU or GPU
        batch_loss.backward() # use back propagation algorithm to calculate out gradients for each parameters
        optimizer.step() # use gradient to update our parameters by optimizer
        train_acc += np.sum(np.argmax(train_pred.to(cpu).data.numpy(), axis=1) == data[1].numpy())
        train_loss += batch_loss.item()
    
    model.eval()
    with torch.no_grad():
        for i, data in enumerate(val_loader):
            val_pred = model(data[0].to(gpu))
            batch_loss = loss(val_pred, data[1].to(gpu))

            val_acc += np.sum(np.argmax(val_pred.to(cpu).data.numpy(), axis=1) == data[1].numpy())
            val_loss += batch_loss.item()
        
        early_stopping(val_loss/val_set.__len__(), model)
        #print out now on accuracy
        print('[%03d/%03d] %2.2f sec(s) Train Acc: %3.6f Loss: %3.6f | Val Acc: %3.6f loss: %3.6f' % \
            (epoch + 1, num_epoch, time.time()-epoch_start_time, \
             train_acc/train_set.__len__(), train_loss/train_set.__len__(), val_acc/val_set.__len__(), val_loss/val_set.__len__()))
    if early_stopping.early_stop:
      print("Early stopping")
      break

#combine validation data and training data in order to get better model adter getting better model
#train_val_x = np.concatenate((train_x, val_x), axis = 0)
#train_val_y = np.concatenate((train_y, val_y), axis = 0)
#train_val_x, train_val_y = _shuffle(train_val_x, train_val_y)
#train_val_set = DigitDataset(train_val_x, train_val_y, train_transform)
#train_val_loader = DataLoader(train_val_set, batch_size=batch_size, shuffle=True)

#for epoch in range(num_epoch):
#    epoch_start_time = time.time()
#    train_acc = 0.0
#    train_loss = 0.0

#    model.train()
#    for i, data in enumerate(train_val_loader):
#        optimizer.zero_grad()
#        train_pred = model(data[0].to(gpu))
#        batch_loss = loss(train_pred, data[1].to(gpu))
#        batch_loss.backward()
#        optimizer.step()

#        train_acc += np.sum(np.argmax(train_pred.to(cpu).data.numpy(), axis=1) == data[1].numpy())
#        train_loss += batch_loss.item()

#    print('[%03d/%03d] %2.2f sec(s) Train Acc: %3.6f Loss: %3.6f' % \
#      (epoch + 1, num_epoch, time.time()-epoch_start_time, \
#      train_acc/train_val_set.__len__(), train_loss/train_val_set.__len__()))
#print out prediction on testing set
test_set = tools.DigitDataset(test_x, test_y, transform = test_transform)
test_loader = DataLoader(test_set, batch_size = batch_size, shuffle = False)

model.load_state_dict(torch.load('digitalnetwork_3.pkl'))
model.eval()
test_acc = 0.0
test_loss = 0.0
with torch.no_grad():
  for i, data in enumerate(test_loader):
    epoch_start_time = time.time()
    test_pred = model(data[0].to(gpu))
    batch_loss = loss(test_pred, data[1].to(gpu))

    test_acc += np.sum(np.argmax(test_pred.to(cpu).data.numpy(), axis=1) == data[1].numpy())
    test_loss += batch_loss.item()

  #print out accuracy and loss
  print('%2.2f sec(s) Test Acc: %3.6f Loss: %3.6f' % \
      (time.time()-epoch_start_time, \
      test_acc/test_set.__len__(), test_loss/test_set.__len__()))
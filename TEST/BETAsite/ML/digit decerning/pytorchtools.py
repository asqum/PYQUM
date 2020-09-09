import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn

class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""
    def __init__(self, patience=7, verbose=False, delta=0, path='digitalnetwork_3.pkl'):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement. 
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
            path (str): Path for the checkpoint to be saved to.
                            Default: 'checkpoint.pt'
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.inf
        self.delta = delta
        self.path = path

    def __call__(self, val_loss, model):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        '''Saves model when validation loss decrease.'''
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), self.path)
        self.val_loss_min = val_loss
    
    def refresh(self):
        a = self.counter
        self.counter = 0
        self.early_stop = False
        print(f'refreshing counter: {a} --> {self.counter}')
        print(f'refreshing early_stop flag: {self.early_stop}')
#self defined model which is used to build customized neuron network, such as maxout layer, which is
#somehow efficient in training model
class ListModule(object):
    def __init__(self, module, prefix, *args):
        self.module = module
        self.prefix = prefix
        self.num_module = 0
        for new_module in args:
            self.append(new_module)

    def append(self, new_module):
        if not isinstance(new_module, nn.Module):
            raise ValueError('Not a Module')
        else:
            self.module.add_module(self.prefix + str(self.num_module), new_module)
            self.num_module += 1

    def __len__(self):
        return self.num_module

    def __getitem__(self, i):
        if i < 0 or i >= self.num_module:
            raise IndexError('Out of bound')
        return getattr(self.module, self.prefix + str(i))

# convolutional maxout neuron network: adding maxout layer
class maxout_conv_net(nn.Module):
    def __init__(self, num_units = 2):
        super(maxout_conv_net, self).__init__()
        self.conv1_list = ListModule(self, "conv1_")
        self.conv2_list = ListModule(self, "conv2_")
        self.fc1_list = ListModule(self, "fc1_")
        self.fc2_list = ListModule(self, "fc2_")
        self.fc3_list = ListModule(self, "fc3_")
        self.fc4_list = ListModule(self, "fc4_")
        #network structure
        conv_1 = nn.Sequential( 
          nn.Conv2d(3, 64, 3, 1, 1),  # [64, 28, 28]
          nn.BatchNorm2d(64),
          nn.PReLU(num_parameters = 1, init = 0.25),
          nn.MaxPool2d(2, 2, 0),      # [64, 14, 14]
        )
        conv_2 = nn.Sequential(
          nn.Conv2d(64, 128, 3, 1, 1), # [128, 14, 14]
          nn.BatchNorm2d(128),
          nn.PReLU(num_parameters = 1, init = 0.25),
          nn.MaxPool2d(2, 2, 0),      # [128, 7, 7]
        )
        fc_1 = nn.Sequential(
          nn.Linear(128*7*7, 1024),
          nn.BatchNorm1d(1024),
          nn.Dropout(0.3),
          nn.PReLU(num_parameters = 1, init = 0.25)
        )
        fc_2 = nn.Sequential(
          nn.Linear(1024, 512),
          nn.BatchNorm1d(512),
          nn.Dropout(0.3),
          nn.PReLU(num_parameters = 1, init = 0.25)
        )
        fc_3 = nn.Sequential(
          nn.Linear(512, 216),
          nn.BatchNorm1d(216),
          nn.Dropout(0.3),
          nn.PReLU(num_parameters = 1, init = 0.25)
        )
        fc_4 = nn.Sequential(
          nn.Linear(216, 10),
          nn.BatchNorm1d(10),
          nn.PReLU(num_parameters = 1, init = 0.25)
        )
        for _ in range(num_units):
            self.conv1_list.append(conv_1)
            self.conv2_list.append(conv_2)
            self.fc1_list.append(fc_1)
            self.fc2_list.append(fc_2)
            self.fc3_list.append(fc_3)
            self.fc4_list.append(fc_4)

    def forward(self, x): 
        x = self.maxout(x, self.conv1_list)
        x = self.maxout(x, self.conv2_list)
        x = x.view(x.size()[0], -1)
        x = self.maxout(x, self.fc1_list)
        x = self.maxout(x, self.fc2_list)
        x = self.maxout(x, self.fc3_list)
        x = self.maxout(x, self.fc4_list)
        return x
    # there are several neurons composing one neuron in maxout layer. if you are interested in the content, you may directly search 
    # maxout layer on the internet
    def maxout(self, x, layer_list):
        max_output = layer_list[0](x)
        for _, layer in enumerate(layer_list, start = 1):
          max_output = torch.max(max_output, layer(x))
        return max_output
#overwrite class Dataset in pytorch
class DigitDataset(Dataset):
    def __init__(self, x, y = None, transform = None):
        self.x = x
        # label is required to be a LongTensor
        self.y = y
        if y is not None:
            self.y = torch.LongTensor(y)
        self.transform = transform
    def __len__(self):
        return len(self.x)
    def __getitem__(self, index):
        X = self.x[index]
        if self.transform is not None:
            X = self.transform(X)
        if self.y is not None:
            Y = self.y[index]
            return X, Y
        else:
            return X
        
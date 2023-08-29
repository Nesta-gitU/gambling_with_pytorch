from torch.utils.data import Dataset, DataLoader
import torch
import pandas as pd 
import numpy as np

class TrackingDistanceData(Dataset):

    def __init__(self):
        x = pd.read_csv("C:/Nesta/side projects/gambling_with_vscode/data/features.csv", index_col=0).to_numpy()
        y = pd.read_csv("C:/Nesta/side projects/gambling_with_vscode/data/y.csv", index_col=0).to_numpy()

        y = np.array([1 if x == True else 0 for x in y]).T
        x = x.astype(np.float32)

        self.x = torch.from_numpy(x)
        self.y = torch.from_numpy(y).type(torch.LongTensor)

        print(self.y)
        print(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return len(self.y)
    

TrackingDistanceData()
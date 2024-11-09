import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader, Dataset
from PIL import Image
from sklearn.model_selection import train_test_split
import os

class CarImageDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        img_path = self.dataframe.iloc[idx]['image_path']
        label = self.dataframe.iloc[idx]['type_of_seller']
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)
        
        label = 1 if label == 'Prywatny sprzedawca' else 0

        return image, label

def predicat_seller(df: pd.DataFrame):
    df['image_path'] = df['id'].apply(lambda x: f"..\\..\\images\\data\\{x}.jpg")
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # Data Transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    train_dataset = CarImageDataset(train_df, transform=transform)
    test_dataset = CarImageDataset(test_df, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # Load Pretrained Model
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 1)  # Binary classification
    
    # Define Loss and Optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
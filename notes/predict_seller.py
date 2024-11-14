import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Custom Dataset Class
class CarImageDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.dataframe = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        img_path = self.dataframe.iloc[idx]['image_path']
        label = self.dataframe.iloc[idx]['type_of_seller']
        file_path = os.path.abspath(img_path)
        image = Image.open(file_path).convert('RGB')

        if self.transform:
            image = self.transform(image)
        
        label = 1 if label == 'Prywatny sprzedawca' else 0

        return image, label

def prepare_loaders(df):
    df['image_path'] = df['img_local'].apply(lambda x: f"data_img/{x}")

    # Split the data into train and test sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    # Save DataFrame to JSON
    #df.to_json('../updated_data.json', orient='records', lines=True)

    # Data Transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Create DataLoader for Training and Testing
    train_dataset = CarImageDataset(train_df, transform=transform)
    test_dataset = CarImageDataset(test_df, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    return train_loader, test_loader

def prepare_model():
    # Load Pretrained Model
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 1)  # Binary classification

    # Define Loss and Optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    return model, criterion, optimizer


def train_and_save_model(model, criterion, optimizer, loader):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    # Training Loop
    epochs = 10
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.float().to(device)

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward
            outputs = model(inputs).squeeze()
            loss = criterion(outputs, labels)

            # Backward
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)

        epoch_loss = running_loss / len(loader.dataset)
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss:.4f}")

    # Save the model
    torch.save(model.state_dict(), "seller_type_model.pth")

# Evaluation
def evaluate(model, data_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs, labels = inputs.to(device), labels.float().to(device)
            outputs = model(inputs).squeeze()
            predicted = (torch.sigmoid(outputs) > 0.5).float()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    print(f'Accuracy: {accuracy:.2f}%')


# Prepare Data
file_path = os.path.abspath(f'cleaned_base_data.json')
json_data = pd.read_json(file_path, lines=True)
df = pd.DataFrame(json_data)
df = df[df['type_of_seller'].notna()]
print(df.info())
print(df.head(5))

train_loader, test_loader = prepare_loaders(df)
model, criterion, optimizer = prepare_model()
train_and_save_model(model, criterion, optimizer, train_loader)

evaluate(model, test_loader)


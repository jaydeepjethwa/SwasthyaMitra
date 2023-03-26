import torch
from torch import nn
from torchvision import models
import torchvision.transforms as T
from PIL import Image
import torchvision.transforms as T
import cv2


class ChestModel(torch.nn.Module):
    def __init__(self, no_labels):
        super(ChestModel, self).__init__()
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        # freezing weights for transfer learning
        # for param in model.parameters():
        #    param.requires_grad = False

        model.fc = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features=model.fc.in_features, out_features=no_labels)
        )
        self.base_model = model

    def forward(self, image):
        outputs = self.base_model(image)

        return outputs


def load_model():
    global model, device

    model = ChestModel(20)

    fine_tuned_path = "notebooks/chest_model_resnet50.pth"
    # loads model to GPU if available else on CPU

    device = 'cpu'
    if torch.cuda.is_available():
        device = 'cuda'
        model.load_state_dict(torch.load(fine_tuned_path))
        model.to(device)
    else:
        model.load_state_dict(torch.load(fine_tuned_path, map_location=device))


transforms = T.Compose([
                       T.ToPILImage(),
                       T.Resize((224, 224)),
                       T.ToTensor(),
                       T.Normalize(
                           mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225]
                       )
                       ])

label_map = {0: 'Atelectasis', 1: 'Cardiomegaly', 2: 'Consolidation', 3: 'Edema', 4: 'Effusion', 5: 'Emphysema', 6: 'Fibrosis', 7: 'Hernia', 8: 'Infiltration', 9: 'Mass', 10: 'Nodule', 11: 'Pleural_Thickening',
             12: 'Pneumonia', 13: 'Pneumothorax', 14: 'Pneumoperitoneum', 15: 'Pneumomediastinum', 16: 'Subcutaneous Emphysema', 17: 'Tortuous Aorta', 18: 'Calcification of the Aorta', 19: 'No Finding'}


async def classify(img_id: str):
    image = cv2.imread(f'app/static/images/{img_id}')
    image = transforms(image)
    image = image.to(device)

    model.eval()
    preds = model(image.unsqueeze(0))
    y_pred_softmax = torch.log_softmax(preds, dim=1)
    _, y_pred_tags = torch.max(y_pred_softmax, dim=1)

    return label_map[y_pred_tags.item()]


disease_inference = {
    "Atelectasis": {
        "description": "Atelectasis is a condition where one or more areas of the lung collapse or don't inflate properly. It can be caused by blockages in the air passages, lung injury, or pressure on the lung from a buildup of fluid in the pleural space.",
        "symptoms": "Symptoms of atelectasis may include difficulty breathing, rapid or shallow breathing, chest pain, and coughing.",
        "treatment": "Treatment for atelectasis depends on the underlying cause but may include deep breathing exercises, bronchodilators, antibiotics, or surgery in severe cases."
    },
    "Cardiomegaly": {
        "description": "Cardiomegaly is a condition where the heart is enlarged. It can be caused by a variety of factors including high blood pressure, heart valve disease, or congenital heart defects.",
        "symptoms": "Symptoms of cardiomegaly may include shortness of breath, fatigue, chest pain, and palpitations.",
        "treatment": "Treatment for cardiomegaly may include medications to treat underlying conditions, lifestyle changes, or surgery in severe cases."
    },
    "Consolidation": {
        "description": "Consolidation is a condition where the lung tissue becomes solid instead of being filled with air. It can be caused by a variety of factors including pneumonia, tuberculosis, or lung cancer.",
        "symptoms": "Symptoms of consolidation may include cough, fever, chest pain, and difficulty breathing.",
        "treatment": "Treatment for consolidation depends on the underlying cause but may include antibiotics, antifungal medications, or chemotherapy in severe cases."
    },
    "Edema": {
        "description": "Edema is a condition where there is an accumulation of fluid in the body tissues. It can be caused by a variety of factors including heart failure, kidney disease, or liver disease.",
        "symptoms": "Symptoms of edema may include swelling in the legs, feet, or hands, weight gain, and difficulty breathing.",
        "treatment": "Treatment for edema depends on the underlying cause but may include medications to reduce fluid buildup, lifestyle changes, or surgery in severe cases."
    },
    "Effusion": {
        "description": "Effusion is a condition where there is an abnormal buildup of fluid in the body cavities, such as the pleural or pericardial space. It can be caused by a variety of factors including infection, inflammation, or cancer.",
        "symptoms": "Symptoms of effusion may include chest pain, shortness of breath, coughing, and fever.",
        "treatment": "Treatment for effusion depends on the underlying cause but may include draining the fluid through a needle or tube, medications, or surgery in severe cases."
    },
    "Emphysema": {
        "description": "Emphysema is a condition where the air sacs in the lungs are damaged, leading to difficulty breathing. It is commonly caused by smoking or exposure to air pollution.",
        "symptoms": "Symptoms of emphysema may include shortness of breath, coughing, wheezing, and chest tightness.",
        "treatment": "Treatment for emphysema may include medications to improve breathing, oxygen therapy, or surgery in severe cases."
    },
    "Fibrosis": {
        "description": "Fibrosis is a condition where there is an excessive buildup of scar tissue in the body, leading to organ damage and dysfunction. It can be caused by a variety of factors including chronic inflammation, infection, or exposure to toxins.",
        "symptoms": "Symptoms of fibrosis depend on the affected organ but may include shortness of breath, coughing, fatigue, and abdominal pain.",
        "treatment": "Treatment for fibrosis depends on the underlying cause but may include medications to slow the progression of the disease, oxygen therapy, or lung transplant in severe cases."
    },
    "Hernia": {
        "description": "Hernia is a condition where an organ or tissue protrudes through a weak spot in the surrounding muscle or connective tissue. It can occur in various parts of the body, including the abdomen, groin, and diaphragm.",
        "symptoms": "Symptoms of hernia may include a bulge or lump in the affected area, pain or discomfort, and nausea or vomiting.",
        "treatment": "Treatment for hernia may include watchful waiting, lifestyle changes, or surgery to repair the hernia."
    },
    "Infiltration": {
        "description": "Infiltration is a condition where foreign substances, such as blood, medications, or air, enter the lung tissue instead of staying in the airways. It can be caused by a variety of factors including improper insertion of a medical device or trauma to the chest.",
        "symptoms": "Symptoms of infiltration may include coughing, shortness of breath, chest pain, and fever.",
        "treatment": "Treatment for infiltration depends on the underlying cause but may include stopping the medication or removing the medical device, oxygen therapy, or antibiotics in case of infection."
    },
    "Mass": {
        "description": "Mass refers to an abnormal growth or lump in the body. It can be benign or malignant and can occur in various parts of the body, including the lungs.",
        "symptoms": "Symptoms of a mass depend on its location and size but may include pain, swelling, and difficulty breathing.",
        "treatment": "Treatment for a mass depends on the underlying cause but may include surgery, chemotherapy, radiation therapy, or watchful waiting in case of a benign mass."
    },
    "Nodule": {
        "description": "Nodule refers to a small, solid lump in the body. It can be benign or malignant and can occur in various parts of the body, including the lungs.",
        "symptoms": "Symptoms of a nodule depend on its location and size but may include coughing, shortness of breath, chest pain, and fever.",
        "treatment": "Treatment for a nodule depends on the underlying cause but may include watchful waiting, surgery, chemotherapy, or radiation therapy."
    },
    "Pleural_Thickening": {
        "description": "Pleural thickening is a condition where the lining of the lungs becomes thicker than normal, leading to difficulty breathing. It can be caused by a variety of factors including asbestos exposure, infections, or inflammatory conditions.",
        "symptoms": "Symptoms of pleural thickening may include shortness of breath, chest pain, and coughing.",
        "treatment": "Treatment for pleural thickening depends on the underlying cause but may include medications to reduce inflammation, oxygen therapy, or surgery in severe cases."
    },
    "Pneumonia": {
        "description": "Pneumonia is a respiratory infection where the air sacs in the lungs become inflamed and fill with fluid. It can be caused by a variety of factors including bacteria, viruses, or fungi.",
        "symptoms": "Symptoms of pneumonia may include coughing, fever, chest pain, and difficulty breathing.",
        "treatment": "Treatment for pneumonia depends on the underlying cause but may include antibiotics, antiviral medications, or antifungal medications."
    },
    "Pneumothorax": {
        "description": "Pneumothorax is a condition where air leaks into the space between the lung and the chest wall, causing the lung to collapse partially or completely. It can be caused by a variety of factors including trauma to the chest, underlying lung disease, or medical procedures.",
        "symptoms": "Symptoms of pneumothorax may include chest pain, shortness of breath, and rapid heart rate.",
        "treatment": "Treatment for pneumothorax depends on the severity and underlying cause but may include observation, oxygen therapy, chest tube insertion to remove the air, or surgery in severe cases."
    },
    "Pneumoperitoneum": {
        "description": "Pneumoperitoneum is a condition where air accumulates in the abdominal cavity, leading to abdominal pain and discomfort. It can be caused by a variety of factors including trauma to the abdomen or medical procedures.",
        "symptoms": "Symptoms of pneumoperitoneum may include abdominal pain and discomfort, bloating, and nausea.",
        "treatment": "Treatment for pneumoperitoneum depends on the underlying cause but may include observation, antibiotics in case of infection, or surgery in severe cases."
    },
    "Pneumomediastinum": {
        "description": "Pneumomediastinum is a condition where air accumulates in the space between the lungs, causing chest pain and discomfort. It can be caused by a variety of factors including trauma to the chest, underlying lung disease, or medical procedures.",
        "symptoms": "Symptoms of pneumomediastinum may include chest pain, shortness of breath, and rapid heart rate.",
        "treatment": "Treatment for pneumomediastinum depends on the severity and underlying cause but may include observation, oxygen therapy, or surgery in severe cases."
    },
    "Subcutaneous Emphysema": {
        "description": "Subcutaneous emphysema is a condition where air accumulates under the skin, leading to swelling and discomfort. It can be caused by a variety of factors including trauma to the chest or neck, underlying lung disease, or medical procedures.",
        "symptoms": "Symptoms of subcutaneous emphysema may include swelling, discomfort, and crackling sensation under the skin.",
        "treatment": "Treatment for subcutaneous emphysema depends on the severity and underlying cause but may include observation, oxygen therapy, or surgery in severe cases."
    },
    "Tortuous Aorta": {
        "description": "Tortuous aorta is a condition where the aorta, the largest artery in the body, becomes abnormally twisted or curved. It can be caused by a variety of factors including aging, high blood pressure, and atherosclerosis.",
        "symptoms": "Tortuous aorta may not cause any symptoms but can lead to high blood pressure, chest pain, and difficulty breathing in severe cases.",
        "treatment": "Treatment for tortuous aorta depends on the underlying cause but may include medications to control blood pressure or surgery in severe cases."
    },
    "Calcification of the Aorta": {
        "description": "Calcification of the aorta is a condition where calcium deposits accumulate in the walls of the aorta, leading to stiffening and narrowing of the artery. It can be caused by a variety of factors including aging, high blood pressure, and atherosclerosis.",
        "symptoms": "Calcification of the aorta may not cause any symptoms but can lead to high blood pressure, chest pain, and difficulty breathing in severe cases.",
        "treatment": "Treatment for calcification of the aaorta depends on the severity and underlying cause but may include medications to control blood pressure, lifestyle modifications such as a healthy diet and exercise, or surgery in severe cases."
    }
}

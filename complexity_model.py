import argparse
import xgboost as xgb
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import math
from tqdm import tqdm
import torch
import csv
import glob


class ComplexityModel:
    def __init__(self, model_type, rubert_path, xgbmetrics_path, xgbhybrid_path, batch_size, text_path, metrics_path, save_path):
        self.model_type = model_type,
        self.rubert_path = rubert_path,
        self.xgbmetrics_path = xgbmetrics_path,
        self.xgbhybrid_path = xgbhybrid_path,
        self.batch_size = batch_size,
        self.text_path = text_path,
        self.metrics_path = metrics_path,
        self.save_path = save_path

        file_list =  [self.text_path + f[0].replace('.xml', '.txt') for f in self.metrics]
        self.texts = []
        for f in file_list:
            with open(f, 'r') as file:
                data = file.read()
            self.texts.append(data)

    def predict_metrics(self):
        model_xgb = xgb.XGBClassifier()
        model_xgb.load_model(self.metrics_xgb)
        self.metrics_predictions = model_xgb.predict(self.metrics_list)

    def predict_rubert(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased", truncation=True, padding=True)
        model = AutoModelForSequenceClassification.from_pretrained(self.rubert_modelpath, num_labels=1, local_files_only=True).to(device)
        BATCH_SIZE = 16
        logits = []
        #model_encodings = []
        nb_batches = math.ceil(len(self.texts)/BATCH_SIZE)
        for i in tqdm(range(nb_batches)):
            input_texts = self.texts[i * BATCH_SIZE: (i+1) * BATCH_SIZE]
            with torch.no_grad():
                encoded = tokenizer(input_texts, max_length = 768, return_tensors="pt").to(device)
                model_codes = model(**encoded)
                logits += model_codes.logits
                #return encodings
                #model_encodings += model_codes[1][-1][:,0,:] 
        self.rubert_predictions = [i.tolist()[0] for i in logits]

    def predict_hybrid(self):
        self.predict_rubert(self)
        model_xgb = xgb.XGBClassifier()
        model_xgb.load_model(self.hybrid_xgb)
        prediction_inputs = [[float(k) for k in i]+[j] for i,j in zip(self.metrics_list, self.rubert_predictions)]
        self.hybrid_predictions = model_xgb.predict(prediction_inputs)

    def run_predict(self):
        if self.model_type == 'metrics':
            self.predict_metrics(self)
            self.predictions = self.metrics_predictions
        if self.model_type == 'RUBERT':
            self.predict_rubert(self)
            self.predictions = [round(i*12) if round(i*12)<13 else 12 for i in self.rubert_predictions]
        if self.model == 'hybrid':
            self.predict_hybrid(self)
            self.predictions = self.hybrid_predictions

    def save(self):
        results = [[i,k] for i,k in zip([i[0] for i in self.metrics_list], self.predictions)]
        with open(self.save_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(results)

def main():
    parser = argparse.ArgumentParser(description="Get complexity predictions")

    parser.add_argument(
        "--model-type", default="hybrid", help="model type: metrics, RUBERT, hybrid"
    )

    parser.add_argument(
        "--rubert-path", default="./complexitymodel/rubert", help="path to fine-tuned rubert model"
    )

    parser.add_argument(
        "--xgbmetrics-path", default="metrics_model.json", help="path to the xgboost model, trained for metrics"
    )

    parser.add_argument(
        "--xgbhybrid-path", default="hybrid_model.json", help="path to the xgboost model, trained for metrics"
    )

    parser.add_argument(
        "--batch-size", default=16, type=int, help="batch size for language model predictions"
    )

    parser.add_argument(
        "--text-path", default="/texts", help="path to texts with names matching first column of metrics table"
    )

    parser.add_argument(
        "--metrics-path", default="metrics.csv", help="path to the xgboost model, trained for metrics"
    )

    parser.add_argument(
        "--save-path", default="predictions.csv", help="save path"
    )

    args = parser.parse_args()

    complexity_model = ComplexityModel(
        model_type = args.model_type,
        rubert_path = args.rubert_path,
        xgbmetrics_path = args.xgbmetrics_path,
        xgbhybrid_path = args.xgbhybrid_path,
        batch_size = args.batch_size,
        text_path = args.text_path,
        metrics_path = args.metrics_path,
        save_path = args.save_path
    )
    complexity_model.run_predict()
    complexity_model.save()


if __name__ == "__main__":
    main()
class Training:
    def __init__(self, model, data_processor):
        self.model = model
        self.data_processor = data_processor

    def train(self, raw_data):
        processed_data = self.data_processor.process(raw_data)
        self.model.fit(processed_data['features'], processed_data['labels'])

    def evaluate(self, test_data):
        processed_test_data = self.data_processor.process(test_data)
        return self.model.score(processed_test_data['features'], processed_test_data['labels'])

    def save_model(self, file_path):
        import joblib
        joblib.dump(self.model, file_path)

    def load_model(self, file_path):
        import joblib
        self.model = joblib.load(file_path)
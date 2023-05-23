import pickle
import os


def classify_email_body(encoded_email_body):
    model_file = os.path.join(os.path.dirname(
        __file__), 'files', 'emails_body_classification_model.sav')

    loaded_model = pickle.load(
        open(model_file, 'rb'))

    return loaded_model.predict([encoded_email_body]).flatten()[0]


def classifyUrl(url_features):
    model_file = os.path.join(os.path.dirname(
        __file__), 'files', 'phishing_url_classification.sav')
    loaded_model = pickle.load(open(model_file, 'rb'))
    return loaded_model.predict([url_features]).flatten()[0]

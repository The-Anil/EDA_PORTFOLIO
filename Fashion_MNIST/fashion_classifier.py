import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

def load_data(train_csv, test_csv):
    train_df = pd.read_csv(train_csv)
    test_df = pd.read_csv(test_csv)
    X_train = train_df.iloc[:, 1:].values / 255.0
    y_train = train_df.iloc[:, 0].values
    X_test = test_df.iloc[:, 1:].values / 255.0
    y_test = test_df.iloc[:, 0].values
    return X_train, y_train, X_test, y_test

def build_model():
    model = Sequential([
        Dense(128, activation='relu', input_shape=(784,)),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def evaluate_model(model, X_test, y_test):
    import numpy as np
    from sklearn.metrics import ConfusionMatrixDisplay

    # Predict labels
    y_pred = np.argmax(model.predict(X_test), axis=1)

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

    # Precision, Recall, F1-score (macro for multiclass)
    precision = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    print(f"Precision (macro): {precision:.4f}")
    print(f"Recall (macro): {recall:.4f}")
    print(f"F1-score (macro): {f1:.4f}")

    # Specificity for each class
    specificity = []
    for i in range(cm.shape[0]):
        tn = cm.sum() - (cm[i,:].sum() + cm[:,i].sum() - cm[i,i])
        fp = cm[:,i].sum() - cm[i,i]
        specificity.append(tn / (tn + fp) if (tn + fp) > 0 else 0)
    print("Specificity (per class):", np.round(specificity, 4))
    print(f"Specificity (macro): {np.mean(specificity):.4f}")

    # Optional: Display confusion matrix
    ConfusionMatrixDisplay(cm).plot()

def main():
    train_csv = 'fashion-mnist_train.csv'  # Update path as needed
    test_csv = 'fashion-mnist_test.csv'    # Update path as needed
    X_train, y_train, X_test, y_test = load_data(train_csv, test_csv)
    model = build_model()
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()

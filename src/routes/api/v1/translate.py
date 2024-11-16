from keras.api.models import Sequential
from keras.api.layers import Dense, GRU, Bidirectional, Softmax, Input
from keras.api.utils import to_categorical
from keras.api.saving import save_model

# from keras.cOallbacks import Callback
# from livelossplot import PlotLossesKeras
from threading import Thread
from flask import Blueprint, request

# from numpy.core.arrayprint import np
import numpy as np
import os

# from tensorflow.keras.layers import Dense, GRU, Bidirectional
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from ....models.word import TWORD
from ....models.response import Response
import requests


translateRoutes = Blueprint("translate", __name__, url_prefix="/translate")

model = None
training_status = 0


# Definir una clase personalizada para imprimir el progreso del entrenamiento cada n épocas
# class NBatchLogger(Callback):
#     def __init__(self, display):
#         self.seen = 0
#         self.display = display
#
#     def on_batch_end(self, batch, logs={}):
#         self.seen += logs.get("size", 0)
#         if self.seen % self.display == 0:
#             # Actualizar el estado del entrenamiento con la pérdida y la precisión actuales
#             global training_status
#             training_status = f"Training... Loss: {logs.get('loss'):.4f}, Accuracy: {logs.get('accuracy'):.4f}"


def send_update_model():
    try:
        response = requests.post(
            f"{translation_service_host}/update",
            files={"model": ("lsb.keras", open("lsb.keras", "rb"))},
        )
        print(response.text)

        response.raise_for_status()
    except Exception as e:
        raise e


def train_model(actions):
    # send_update_model()
    # return
    global model
    try:
        DATA_PATH = os.path.join(os.getcwd(), "static", "points")
        sequence_length = 30

        label_map = {label: num for num, label in enumerate(actions)}
        sequences, labels = [], []
        for action in actions:
            for sequence in np.array(
                os.listdir(os.path.join(DATA_PATH, action))
            ).astype(int):
                window = []
                for frame_num in range(0, sequence_length):
                    res = np.load(
                        os.path.join(
                            DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)
                        )
                    )
                    window.append(res)
                sequences.append(window)
                labels.append(label_map[action])

        X = np.array(sequences)
        y = to_categorical(labels).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

        model = Sequential()
        model.add(Input(shape=(30, 1662)))
        model.add(
            Bidirectional(
                GRU(
                    64,
                    return_sequences=True,
                    activation="relu",
                )
            )
        )
        model.add(Bidirectional(GRU(128, return_sequences=True, activation="relu")))
        model.add(Bidirectional(GRU(64, return_sequences=False, activation="relu")))
        model.add(Dense(64, activation="relu"))
        model.add(Dense(32, activation="relu"))
        model.add(Dense(actions.shape[0], activation="softmax"))

        model.compile(
            optimizer="Adam",
            loss="categorical_crossentropy",
            metrics=["categorical_accuracy"],
        )
        model.fit(X_train, y_train, epochs=500)
        model.summary()
        save_model(model, "lsb.keras")

        send_update_model()

        global training_status
        training_status = 2
    except Exception as e:
        training_status = 3


# Definir una ruta para iniciar el entrenamiento del modelo
@translateRoutes.route("/train", methods=["POST"])
def train():
    global training_status
    if training_status == 1:
        return Response.fail("En entrenamiento")

    training_status = 1

    # actions = db.session.query(TWORD).filter(TWORD.state.ilike("active")).filter(
    #     exists().where(TWORDVIDEO.word_id == TWORD.id)).all()
    actions = TWORD.query.filter(TWORD.state.ilike("active")).all()

    actions = np.array([word.word for word in actions])

    thread = Thread(target=train_model, args=(actions,))
    thread.start()

    return Response.success("Se empezo el entrenamiento correctamente", None)


@translateRoutes.route("/status", methods=["GET"])
def status():
    global training_status
    response = Response.success("Estado del entrenamiento", {"status": training_status})

    if training_status == 2:
        response = Response.success(
            "Entrenamiento completado", {"status": training_status}
        )
        training_status = 0

    if training_status == 3:
        response = Response.success(
            "Error en el entrenamiento", {"status": training_status}
        )
        training_status = 0

    return response


translation_service_host = "http://localhost:6969/"


@translateRoutes.post("/service-link")
def update_service():
    host_json = request.json

    if host_json is None:
        return Response.fail("Petición incorrecta"), 400

    global translation_service_host
    translation_service_host = host_json["host"]

    return Response.success("Servicio cambiado correctamente", None)


@translateRoutes.get("/service-link")
def get_service():
    global translation_service_host

    return Response.success(
        "Link del servicio de traducción", {"host": translation_service_host}
    )

# from keras.models import Sequential
# from keras.layers import Dense
# from keras.callbacks import Callback
# from livelossplot import PlotLossesKeras
from threading import Thread
from flask import Blueprint, request
from numpy.core.arrayprint import np
from sqlalchemy.util.deprecations import os

from tensorflow.keras.layers import Dense, GRU, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from models.word import TWORD
from models.response import Response


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


def train_model(actions):
    global model

    DATA_PATH = os.path.join(os.getcwd(), "static", "points")
    sequence_length = 30

    label_map = {label: num for num, label in enumerate(actions)}
    sequences, labels = [], []
    for action in actions:
        for sequence in np.array(os.listdir(os.path.join(DATA_PATH, action))).astype(
            int
        ):
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
    model.add(
        Bidirectional(
            GRU(
                64,
                return_sequences=True,
                activation="relu",
                input_shape=(30, 1662),
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
    model.fit(X_train, y_train, epochs=2000)
    model.summary()
    model.save(f"lsb_test.h5")

    global training_status
    training_status = 2


# Definir una ruta para iniciar el entrenamiento del modelo
@translateRoutes.route("/train", methods=["POST"])
def train():
    global training_status
    if training_status == 1:
        return Response.fail("En entrenamiento"), 400

    training_status = 1

    actions = TWORD.query.filter(
        TWORD.state.ilike("active"),
    ).all()
    actions = np.array(
        [str(word.word if word.word is not None else "") for word in actions]
    )

    thread = Thread(target=train_model, args=(actions,))
    thread.start()

    return Response.success("Se empezo el entrenamiento correctamente", None)


@translateRoutes.route("/status", methods=["GET"])
def status():
    global training_status
    response = Response.success("Estado del entrenamiento", {"status": training_status})

    if training_status == 2:
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

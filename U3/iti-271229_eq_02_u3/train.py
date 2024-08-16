import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten

# Configuración del generador de imágenes
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    'data/train',  # Ruta a tus datos de entrenamiento
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',   
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    'data/train',  # Usa la misma ruta, pero se dividirá en entrenamiento y validación
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Crear el modelo
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(2, activation='softmax')  # 2 clases: Pemex y Oxxogas
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_generator, validation_data=validation_generator, epochs=10)

# Guardar el modelo
model.save('modeloGasolineras.h5')

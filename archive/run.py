import pandas as pd
import gc
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
stop_words = stopwords.words('english')
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
import transformers
from sklearn.model_selection import train_test_split
import numpy as np
from transformers import TFAutoModel
from keras.utils.vis_utils import plot_model
import warnings
import os
warnings.filterwarnings("ignore")


os.environ["CUDA_VISIBLE_DEVICES"] =
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
print(gpus)

train_df=pd.read_csv('dealt_data_2.tsv',sep='\t')
train_y=train_df['label']
train_x,val_x,train_y,val_y=train_test_split(train_df['text'],train_y,test_size=0.2,random_state=50)

AUTO = tf.data.experimental.AUTOTUNE
strategy = tf.distribute.get_strategy()
print("Replicas num: ", strategy.num_replicas_in_sync)

def quick_encode(texts,tokenizer, maxlen):
    enc_di = tokenizer.batch_encode_plus(
        texts,
        return_attention_mask=False,
        return_token_type_ids=False,
        pad_to_max_length=True,
        max_length=maxlen,
        truncation=True,
    )
    return np.array(enc_di["input_ids"])

def built_model(transformer,train_data,val_data,batch_size,img_name, max_len):
    inp_words_ids = Input(shape =(max_len,),dtype = tf.int32)
    print(inp_words_ids.shape)
    seq_output = transformer(inp_words_ids)[0]
    cls_token = seq_output[:,0,:]
    output =  Dense(2,activation='softmax')(cls_token)
    model = Model(inputs =inp_words_ids,outputs=output)
    model.compile(Adam(lr=1e-5),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    model.summary()
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath='./model/model.h5',
        monitor='val_accuracy',
        mode='max',
        save_best_only=True,
        save_weights_only=True
        )
    csv_logger = tf.keras.callbacks.CSVLogger('training.log')
    plot_model(
        model,to_file=img_name,
        show_shapes=True,
        show_layer_names=True,
        rankdir="TB",
        expand_nested=False,
        dpi=96)
    model.fit(
        train_data,
        steps_per_epoch=batch_size,
        validation_data=val_data,
        epochs=EPOCHS,
        callbacks=[model_checkpoint_callback,csv_logger]
        )
    return model

def del_obects(*args):
    for arg in args:
        del arg
        gc.collect()
model=None
EPOCHS = 5
BATCH_SIZE = 64
MAX_LEN = 192
with strategy.scope():
    #distilbert_tokenizer = transformers.AlbertTokenizer.from_pretrained('albert-large-v2')
    distilbert_tokenizer =transformers.DistilBertTokenizer.from_pretrained('distilbert-base-multilingual-cased')
    train_x_enc = quick_encode(train_x.astype(str), distilbert_tokenizer, maxlen=MAX_LEN)
    val_x_enc = quick_encode(val_x.astype(str), distilbert_tokenizer, maxlen=MAX_LEN)
    train_dataset = (
        tf.data.Dataset.from_tensor_slices((train_x_enc, train_y))
            .repeat()
            .shuffle(2048)
            .batch(BATCH_SIZE)
            .prefetch(AUTO)
    )
    valid_dataset = (
        tf.data.Dataset.from_tensor_slices((val_x_enc, val_y))
            .batch(BATCH_SIZE)
            .cache()
            .prefetch(AUTO)
    )
    #transformer_layer = TFAutoModel.from_pretrained('albert-large-v2')
    transformer_layer = TFAutoModel.from_pretrained('distilbert-base-multilingual-cased')
    model=built_model(transformer_layer, train_dataset, valid_dataset, BATCH_SIZE,
                "Distilbert_Multilingual_Transformer.png", max_len=MAX_LEN)
    del_obects(train_x_enc, val_x_enc, train_dataset, valid_dataset, distilbert_tokenizer, transformer_layer)

model.save_weights('./model/final.h5')
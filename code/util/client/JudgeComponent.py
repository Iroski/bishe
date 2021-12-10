import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
import numpy as np
from tensorflow.keras.models import Model
from transformers import TFAutoModel, AlbertTokenizer, DistilBertTokenizer
from threading import RLock
from util.client.DataCleaner import DataCleaner


class JudgeComponent:
    _lock = RLock()

    def __init__(self, max_len):
        self.max_len = max_len
        inp_words_ids = Input(shape=(max_len,), dtype=tf.int32)
        transformer = TFAutoModel.from_pretrained('./resources/al_mo', local_files_only=True)
        seq_output = transformer(inp_words_ids)[0]
        cls_token = seq_output[:, 0, :]
        output = Dense(2, activation='softmax')(cls_token)
        self.model = Model(inputs=inp_words_ids, outputs=output)
        self.model.load_weights('./resources/albert20_192.h5')
        self.tokenizer = AlbertTokenizer.from_pretrained('./resources/al_to', local_files_only=True)
        self.dataCleaner = DataCleaner()

    @classmethod
    def init(cls, maxlen):
        JudgeComponent._instance = JudgeComponent(maxlen)

    @classmethod
    def get_instance(cls, maxlen=192):
        if not hasattr(JudgeComponent, '_instance'):
            cls._lock.acquire()
            if not hasattr(JudgeComponent, '_instance'):
                JudgeComponent._instance = JudgeComponent(maxlen)
            cls._lock.release()
        return JudgeComponent._instance

    def judge(self, data) -> {bool, str}:
        data = self.dataCleaner.clean_text(data)
        data = [data]
        sentence = self.quick_encode(data, self.tokenizer, maxlen=self.max_len)
        result = self.model.predict(sentence)
        return result[0][0] > result[0][1], str(round(result[0][0] * 100, 1))

    def quick_encode(self, texts, tokenizer, maxlen):
        enc_di = tokenizer.batch_encode_plus(
            texts,
            return_attention_mask=False,
            return_token_type_ids=False,
            pad_to_max_length=True,
            max_length=maxlen,
            truncation=True,
        )
        return np.array(enc_di["input_ids"])


if __name__ == '__main__':
    con = JudgeComponent(192)
    result = con.judge("bug")
    print(result)
    result = con.judge("this is a bug")
    print(result)
    result = con.judge("defect")
    print(result)

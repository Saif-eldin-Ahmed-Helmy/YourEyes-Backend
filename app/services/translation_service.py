from transformers import AutoTokenizer, MarianMTModel

src = "en"  # source language
trg = "ar"  # target language

model_name = f"Helsinki-NLP/opus-mt-{src}-{trg}"
model = MarianMTModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def translate(txt):
    batch = tokenizer([txt], return_tensors="pt")
    generated_ids = model.generate(**batch)
    arabic_txt = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(arabic_txt)
    return arabic_txt
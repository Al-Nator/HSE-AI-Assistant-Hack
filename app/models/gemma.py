from typing import Optional

from app.models.base import BaseModel
from unsloth import FastLanguageModel


class Gemma(BaseModel):
    def __init__(self, max_tokens: int = 2048) -> None:
        super().__init__('')
        self.prompt = '''### INSTRUCTION:
{}

### ОСНОВНАЯ ЗАДАЧА ДЛЯ СТУДЕНТА:
{}

### ВЕРНОЕ РЕШЕНИЕ АВТОРА:
```python
{}
```

### ВЕРНЫЕ ОТВЕТЫ НА UNIT ТЕСТЫ:
{}

### НЕВЕРНОЕ РЕШЕНИЕ СТУДЕНТА:
```python
{}
```

### КОММЕНТАРИИ К НЕВЕРНОМУ РЕШЕНИЮ:
{}'''

        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name = "gemma-2-9b-0.71540-1.5",  #  "gemma-2-9b-0.71540-1.5", "gemma-2-9b", "google/gemma-2-9b-it"
            max_seq_length = max_tokens,
            dtype = None,
            load_in_4bit = True,
        )
        self.model.to('cuda')

    def ask(self, row: str) -> Optional[str]:
        FastLanguageModel.for_inference(self.model)
        text = self.prompt.format(row['system'], row['description'], row['author_solution'], row['unit_true'], row['student_solution'], '')

        inputs = self.tokenizer([text], return_tensors = "pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens = 512, use_cache = True)  # temperature=0.9
        output_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        output_text = output_text.split('### КОММЕНТАРИИ К НЕВЕРНОМУ РЕШЕНИЮ:\n')[-1].replace('<eos>', '').strip()

        return output_text

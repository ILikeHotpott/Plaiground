from transformers import LlamaTokenizer, LlamaForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset

# 加载 LLaMA 模型和分词器
model_name = "meta-llama/Llama-3.2"  # 替换为你的模型路径
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(model_name)

# 加载清理后的数据集
dataset = load_dataset("text", data_files="data/cleaned_tweets.txt")


# 数据分词
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)


tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 定义训练参数
training_args = TrainingArguments(
    output_dir="agents/tech/tech_blogger_history",  # 模型保存路径
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
)

# 初始化 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
)

# 开始训练
trainer.train()

# 保存模型
model.save_pretrained("agents/tech/tech_blogger_history")
tokenizer.save_pretrained("agents/tech/tech_blogger_history")
print("Model fine-tuned and saved to agents/tech/tech_blogger_history")

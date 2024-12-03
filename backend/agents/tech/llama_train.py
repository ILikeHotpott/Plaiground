from transformers import LlamaTokenizer, LlamaForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset

# 路径设置
DATA_FILE = "agents/tech/data/cleaned_tweets.txt"
OUTPUT_DIR = "agents/tech/tech_blogger_history"


# 加载模型和分词器
def load_llama_model(model_name="meta-llama/Llama-3.2"):
    """
    加载预训练的 LLaMA 模型和分词器
    """
    tokenizer = LlamaTokenizer.from_pretrained(model_name)
    model = LlamaForCausalLM.from_pretrained(model_name)
    return tokenizer, model


# 加载数据集并分词
def prepare_dataset(tokenizer, data_file=DATA_FILE):
    """
    加载和分词数据集
    """
    dataset = load_dataset("text", data_files=data_file)

    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    return tokenized_datasets


# 微调模型
def train_llama_model(tokenizer, model, tokenized_datasets, output_dir=OUTPUT_DIR):
    """
    微调 LLaMA 模型并保存
    """
    training_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_steps=500,
        save_total_limit=2,
        logging_dir="./logs",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
    )

    print("开始训练...")
    trainer.train()
    print("训练完成，保存模型...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)


# 主函数
def main():
    print("加载模型和分词器...")
    tokenizer, model = load_llama_model()

    print("加载和分词数据集...")
    tokenized_datasets = prepare_dataset(tokenizer)

    print("开始微调模型...")
    train_llama_model(tokenizer, model, tokenized_datasets)


if __name__ == "__main__":
    main()

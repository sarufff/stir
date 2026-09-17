from datasets import load_dataset

dataset = load_dataset("corbt/all-recipes", split="train")
print(dataset)
print(dataset[0])

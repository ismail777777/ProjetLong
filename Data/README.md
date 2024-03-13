#   Note
The model requires a single column dataset. This is a two column dataset. 

You can follow these steps to transform it into a single column dataset.
## Step 1: Import the Pandas library 
```bash
import pandas as pd
```

## Step 2: Read the train and test csv files
```bash
train_df = pd.read_csv('/train/data_train_train_data.csv')
test_df = pd.read_csv('/test/data_test_test_data.csv')
```

## Step 3: Concatenate 'prompt' and 'code' columns
```bash
train_df['text'] = "<s>[INST] " + train_df['prompt'] + " [/INST] " + train_df['code'] + " </s>"
test_df['text'] = "<s>[INST] " + test_df['prompt'] + " [/INST] " + test_df['code'] + " </s>"
```

## Step 4: Drop the original 'prompt' and 'code' columns if necessary
```bash
train_df.drop(['prompt', 'code'], axis=1, inplace=True)
test_df.drop(['prompt', 'code'], axis=1, inplace=True)
```

# Save the result into a new CSV file
```bash
train_df.to_csv('Merged_train.csv', index=False)
test_df.to_csv('Merged_test.csv', index=False)
```

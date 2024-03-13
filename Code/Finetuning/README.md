# Content
- The notebook "Fine_Tune_C_in_Llama2.ipynb" contains the code of the first attempt of fine-tuning with the LoRA method. (5 epochs)

- The notebook "Fine_Tune_Llama2_etape2.ipynb" contains the code of the second attempt of fine-tuning with the LoRA method. (15 epochs going from the first attempt fine-tuned model, so 20 epochs in total)

- The required versions of the used libraries are given in the "requirements.txt" file. (generated with pip freeze)

- You can download the configuration files of the fine-tuned model here: "link coming soon!"

- The notebook "Test_Model.ipynb" contains the code of how to load and use the fine-tuned model from the configuration files given in the link above. If you want to use the Web interface, you can see the Interface folder.

- The notebooks are documented. To understand more about how the LoRA method works, you can see the project report.  
  
# PS
The fine-tuning will not run on a free Colab GPU (T4 15GB), neither on a V100 16GB. 
You will need at least a GPU with 24GB VRAM to run the fine-tuning. However, you can load and use the model on a free Colab session (T4 15GB) 

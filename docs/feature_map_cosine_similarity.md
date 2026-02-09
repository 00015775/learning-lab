## Feature Maps


<!-- ![original-cat-image](../images/Screenshot%202026-02-06%20at%2017.24.19.png) -->
#### Original `3x1200x1200` image of cat (dtype=`torch.uint8` or `np.uint8`)

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.24.19.png" style="width: 60%" alt="Image of cat">
</div>

<br>

#### The same image but after a convolution layer with `kernel_size=5, padding=1, stride=1, dilation=5`

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.24.39.png" style="width: 60%" alt="Image of cat">
</div>

<br>

#### The same image but after max pooling layer with `kernel_size=5, padding=1, stride=10, dilation=25`

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.24.49.png" style="width: 60%" alt="Image of cat">
</div>

<br>

#### The image but after applying 9 feature maps.

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.24.59.png" style="width: 60%" alt="Feature maps">
</div>

<br>

#### The image but after 12 feature maps.

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.25.10.png" style="width: 60%" alt="Feature maps">
</div>

<br>

#### For cosine similarity calculation, two feature maps were chosen.

<table align="center">
  <tr>
    <td>
      <img src="../images/Screenshot 2026-02-06 at 17.49.53.png" width="60%" alt="Image of cat">
    </td>
    <td>
      <img src="../images/Screenshot 2026-02-06 at 17.50.01.png" width="60%" alt="Image of cat">
    </td>
  </tr>
</table>

<br>

#### Their cosine similarity, input/output shapes.

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.50.16.png" style="width: 60%" alt="Cosine Similarity">
</div>

<br>

## Cosine Similarity


#### The below matrix is the first attempt and incorrect, because it calculated the cosine similarity of inputs `(x, y)`, or more precisely `(H_out, W_out)` - height and width of the convulation layer output.

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.40.47.png" style="width: 60%" alt="Wrong Cosine Similarity">
</div>

<br>

#### After some experimentations, then drew the cosine similarity matrix for 9 different feature maps of the convolution layers. Input and output shapes are provided, along with some relevant statistics.

<br>

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.41.18.png" style="width: 60%" alt="Cosine Similarity">
</div>

<br>

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.42.46.png" style="width: 60%" alt="Cosine Similarity">
</div>

<br>

<div align="center">
<img src="../images/Screenshot 2026-02-06 at 17.44.06.png" style="width: 60%" alt="Cosine Similarity">
</div>



## Transfer learning with `timm`

[Notebook for transfer learning with `timm`](../pytorch/notebooks/03_experiment_timm_cont.ipynb)

#### Training and Validation Loss/Accuracy

> Need to learn how to perform early stopping in code.

<div align="center">
<img src="../images/Screenshot 2026-02-08 at 22.31.44.png" 
style="width: 80%" alt="Training and Validation Loss/Accuracy">
</div>

#### Learning Rate Scheduler

<div align="center">
<img src="../images/Screenshot 2026-02-08 at 22.31.59.png"
style="width: 80%" alt="Learning Rate Scheduler">
</div>


#### Inferencing on test split

<div align="center">
<img src="../images/Screenshot 2026-02-08 at 22.32.10.png"
style="width: 80%" alt="Inferencing on Test split">
</div>

<details>
<summary>
To read the personal experience with transfer learning, click here
</summary>

### Transer Learning experience

While reproducing a Kaggle notebook, I ran into unexpected performance issues. The original notebook used the RMSProp optimizer along with data transformations, but on my Colab notebook the results were much worse. Training accuracy ranged between 40-60% while validation accuracy stayed around 10-20%. These numbers were reached within the first give epochs and then completely plateaued for the remaining 35 epochs.

At first, I suspected a coding mistake, perphaps a misspelled variable name or assigning the same variable name, an indentation error in training/validation loops or during unpatching, or an issue with how loss or accuracy was calculated. After carefully reviewing the ode and running multiple experiments, I discovered with switching the optimizer from RMSProp to AdamW immediately fixed the problem. Both training and validation accuracy jumped above 90% within just three epochs. It was achieved with transformations being disabled, set to None.

However, once I used the data augmentations while using AdamW, training became less stable. Accuracy improved gradually but fluctuated heavily between epochs - for example, jumping from 60% down to 35%, then back up to 80%. Based on chatbot recommendations, the augmentations were likely too aggressive, making the training process noisy. 

While achieving 99% accuracy was great, another inefficiency became obvious, the model reached peak performance within the first 13 epochs yet continued training until epoch 40 with no meaningful improvements. This showed the need for early stopping with a patience parameters, which would automatically stop training when there is no progress over certain epochs. Implementing this would save both time and computational resources while preventing unnecessary runs or manual interruptions.

Finally, I noticed that training without transformations was significantly faster because the CPU didn't have to spend time augmenting images. Instead, the data was send directly to the GPU, removing preprocessing delays.

Overall this experience reinforced how optimizer choice, augmentation methods, and loss/accuracy calculations can dramatically impact both model performance and training efficiency.

</details>
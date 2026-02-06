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






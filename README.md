# A Flexible Deep Learning Architecture for Temporal Sleep Stage Classification using Accelerometry and Photoplethysmography[^1]
[[Paper](https://ieeexplore.ieee.org/document/9813567)|[Presentation](https://drive.google.com/file/d/1W-SdSQYob1_7alz_Y43W1DgTw4Koo1HV/view?usp=sharing)]

![Conceptual visualization of the proposed Deep Learning Framework for Sleep Stage Classification using Accelerometry and Photoplethysmography acquired from Consumer Sleep Technologies](/resources/images/model_ver15.png)
###### Conceptual representation of the proposed deep neural network (DNN) in an example recording. Two time-aligned spectrograms are firstly concatenated, reshaped, and zero-padded to conform to the subsequent temporal module. Then the segments are processed in the deep convolutional neural network, inspired by U-Net[^2][^3][^4] that consists of 𝑀 encoder and decoder blocks. Finally, the output is segmented into sleep epochs of 30 s duration and classified into 4 classes: wake, light sleep, deep sleep. The classification module is inspired by the segment classifier from U-Sleep[^3]. The argmax of the model predictions is presented along with the ground truth hypnogram for comparison. Periods with data loss are labeled with mask. GELU: Gaussian Error Linear Unit activation function; conv: convolution; convTranspose: transposed convolutional; batch norm: batch normalization; STFT: Short Time Fourier Transform; ACC: Accelerometry; PPG: Photoplethysmography.

[^1]: M. Olsen, J. M. Zeitzer, R. N. Richardson, P. Davidenko, P. J. Jennum, H. B. D. Sørensen, and E. Mignot. "A flexible deep learning architecture for temporal sleep stage classification using accelerometry and photoplethysmography," IEEE Transactions on Biomedical Engineering, 2022.

[^2]: O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” Lect. Notes Comput. Sci. (including Subser. Lect. Notes Artif. Intell. Lect. Notes Bioinformatics), vol. 9351, pp. 234–241, 2015.

[^3]: M. Perslev, S. Darkner, L. Kempfner, M. Nikolic, P. J. Jennum, and C. Igel, “U-Sleep: resilient high-frequency sleep staging,” npj Digit. Med., vol. 4, no. 1, pp. 1–12, 2021.

[^4]: H. Li and Y. Guan, “DeepSleep convolutional neural network allows accurate and fast detection of sleep arousal,” Commun. Biol., vol. 4, no. 1, pp. 1–11, 2021. 

-------------------------------------------------------------------------------------------------------------------------------------------------------------
## Minimal example
Use minimal_example to get started. 


-------------------------------------------------------------------------------------------------------------------------------------------------------------
## Reproduction of all experiments in paper
Updates will be coming soon. 


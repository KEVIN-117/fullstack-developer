One of the great benefits of transformers in this domain is their few-shot and zero-shot learning capabilities. Labeling images is expensive, and often there are not enough labels available, as is the case with cancer detection. Having an image classification or segmentation model capable of performing well with few samples is a significant leap forward. This makes transformers particularly valuable for tasks where data scarcity is a critical issue, a challenge where traditional convolutional neural network (CNN)-based models often fall short.

Transformers have clearly revolutionized NLP. The next domain that transformers are conquering is vision tasks. The vision transformer (ViT)[1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id508) is a landmark in demonstrating the full potential of transformers in computer vision.

In the sections to come, I’ll show you how you can leverage transformers for vision tasks such as classification, image segmentation, instance segmentation, and panoptic segmentation. I’ll explain the challenges you might encounter, how to mitigate them when working with images, and how to monitor the training of your model.

Additionally, I’ll discuss the impact of different loss functions on the quality of the results. For example, in medical imaging, compound loss functions are often the most robust, as they’re better suited for highly imbalanced segmentation tasks. This careful selection of loss functions can significantly enhance model performance, particularly in critical applications like cancer detection.

# Overview of Different Vision Tasks

When it comes to vision, there are several distinctions that are important for understanding the various applications and techniques in computer vision. In this section, I’ll distinguish between the most commonly used ones: classification, image segmentation, instance segmentation and panoptic segmentation. In later chapters, I’ll cover object detection, pose estimation, image captioning, and visual question answering, as they fit better into the video and multimodal transformer model cases:

Classification

_Classification_ is the process of predicting the category or class of an object within an image. This task involves assigning a label to the entire image based on the dominant object or feature present. For instance, in a dataset of animal images, a classification model might categorize each image as “cat,” “dog,” “bird,” etc. The main goal here is to identify the object as a whole without considering its location or specific parts.

Semantic image segmentation

_Semantic image segmentation_ goes a step further into the image by dividing it into multiple segments or regions, each presenting a different object. This approach classifies each pixel in the image into a category. For example, in an image of a street scene, pixels might be classified as “road,” “car,” “pedestrian,” or “building.” The primary objective is to understand the image at a pixel level, where each segment represents a class label.

Instance segmentation

This method dives even deeper, dividing the image not only into multiple segments or regions but even into different parts of an object within an image. That is, _instance segmentation_ distinguishes between different objects of the same category. In the same street-scene example, instance segmentation would not only label pixels as “car” but also differentiate between individual cars. This provides a more detailed understanding of the image by identifying separate instances of objects.

Panoptic segmentation

_Panoptic segmentation_ combines both instance segmentation and semantic image segmentation to offer a comprehensive understanding of an image. It labels each pixel in the image with the class of the object (e.g., “car,” “road,” “pedestrian”) and also distinguishes between different instances of those objects. This approach provides a detailed segmentation of the scene, capturing both the objects and their individual instances coherently. [Figure 3-1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#images_task_distinctions) highlights the differences between semantic image, instance, and panoptic segmentation.

![[../../assets/Pasted image 20260518110327.png]]
Figure 3-1. The left image shows semantic image segmentation, the middle image illustrates instance segmentation, and the right image displays panoptic segmentation, which clearly combines the two segmentation variations into one comprehensive approach.

Now that you have an understanding of the differences in these image tasks, let’s explore how transformers are designed to understand and process images. In the next section, you’ll learn how embeddings and tokenization, which are foundational for enabling transformers to effectively handle various vision tasks, are implemented in vision models.

# Embeddings and Tokenization for Vision Models

Convolutional neural networks (CNNs) have dominated vision models from 2011 to 2020, starting with the combination of GPUs and CNNs winning a series of competitions between 2011 and 2012. However, convolutions usually operate on regular grids, making it challenging to integrate elements like tokens or positional embeddings into these networks. This architectural limitation has been overcome with the introduction of vision transformers in 2020. But what is the difference between vision and language, and why do the tokens and positional embeddings need to be different?

To answer this question, you need to understand the significant difference in information density between language and vision. Languages are human-generated signals that are highly semantic and information-dense. The task of training a model to predict only a few missing words per sentence requires a sophisticated understanding of language.

In contrast, images are natural signals with substantial spatial redundancy. A missing patch in an image can often be reconstructed from neighboring patches with little need for high-level understanding of parts, objects, and scenes.

This difference directly influences why ViTs use patches to process images: to capture the global context of an image rather than relying solely on local pixel continuity. By breaking the image into patches, ViT can process each patch as a token, similar to how language models process words in NLP tasks. This approach allows the model to learn relationships between different parts of the image, effectively “disconnecting” neighboring pixels and enabling a more comprehensive understanding of the image as a whole. [Example 3-1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#Patch_embedding) demonstrates how ViT breaks images into patches.

##### Example 3-1. Patch embedding in ViT

```python
class PatchEmbedding(nn.Module):
    def __init__(self, image_size=28, patch_size=7, channels=1, dim=64):
        super().__init__()
        assert image_size % patch_size == 0, """The image dimension must
        be evenly divisible by the patch size, e.g., image_size=28, patch_size=7."""
        num_patches = (image_size // patch_size) ** 2
        patch_dim = channels * patch_size ** 2

        self.patch_size = patch_size

        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, dim))
        self.patch_to_embedding = nn.Linear(patch_dim, dim)
        self.cls_token = nn.Parameter(torch.randn(1, 1, dim))

    def forward(self, img):
        p = self.patch_size

        # Rearrange the image into patches
        x = rearrange(img, 'b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=p, p2=p) 1
        x = self.patch_to_embedding(x) 2

        # Add classification token and positional embedding
        cls_tokens = self.cls_token.expand(img.shape[0], -1, -1)
        x = torch.cat((cls_tokens, x), dim=1) 3
        x += self.pos_embedding 4
        return x
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO1-1)

The image is divided into patches using the `rearrange` function from the einops library.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO1-2)

Each patch is flattened and passed through a linear layer to obtain patch embeddings.

[![3](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/3.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO1-3)

A learnable classification token (`cls_token`) is prepended to the sequence of patch embeddings.

[![4](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/4.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO1-4)

Positional embeddings are created and added to the patch embeddings to retain information about the position of each patch within the image.

I use the well-known Modified National Institute of Standards and Technology (MNIST) handwritten digit dataset to demonstrate how this works. You can try it yourself by using the plotting function provided in the notebook for this section. You’ll get the output shown in [Figure 3-2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#embedding_patches).

![[../../assets/Pasted image 20260518110358.png]]
Figure 3-2. Left is the original image; on the right, with the dashed lines, is the patched image.

For handling, the ViT reshapes the 2D images, which are , into a sequence of flattened 2D patches, , where  represents the resolution of the original image and  denotes the number of channels. The transformer maintains a constant latent vector size  across all its layers, so the patches are flattened and mapped to  dimensions using a trainable linear projection:

Similar to BERT’s `[class]` token, a learnable embedding is appended to the sequence of embedded patches (), with its state at the output of the transformer encoder () serving as the image representation () in .

During both pretraining and fine-tuning, a classification head is attached to . This classification head is implemented as an MLP with one hidden layer during pre-training and a single linear layer during fine-tuning. To retain positional information, the model adds standard learnable 1D positional embeddings to the patch embeddings. The resulting sequence of embedding vectors serves as input to the encoder.

The methods introduced by the ViT, for handling embeddings or tokens, are still used in vision transformers. In fact, as of now, there are no widely known transformer-based vision models that don’t leverage the techniques established by ViT. [Figure 3-3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#ViT_architecture) shows an overview of this architectural setup.

![[../../assets/Pasted image 20260518110412.png]]

Figure 3-3. An image is split into fixed-size patches, each of which is linearly embedded. Position embeddings are then added, and the resulting sequence of vectors is fed into a standard transformer encoder. For classification, an extra learnable “classification token” is added to the sequence. Image adopted from Alexey Dosovitskiy et al.

The next section takes a short detour to show how you can enhance the generalization of your vision model, before you dive deeper into using vision transformers.

# Key Strategies for Improving the Robustness and Effectiveness of Vision Tasks

When performing vision tasks, the underlying data plays a crucial role. Not only is the variety of the data important but also the quality of the images and the specific task at hand. For instance, segmenting roofs from satellite images is fundamentally different from detecting cancer. Satellite imagery often covers large areas with varying resolutions and requires handling complex backgrounds, whereas medical images demand high precision and are usually high resolution to capture fine details. Depending on your task, you need to choose the appropriate loss function, augmentation techniques, and regularization methods to achieve the best results. Therefore, this section aims to offer some ideas and resources to help you get started and inspire your own projects. To make the differences clearer, I’ll use roof segmentation and cancer detection as examples for comparison:

Data augmentation

Standard methods use data augmentation to flip, rotate, or scale images. These methods help the model to generalize better and are usually sufficient for tasks like segmenting a roof from a satellite image. However, when it comes to cancer detection, you have to apply advanced data-augmentation techniques such as elastic deformations, random cropping, and intensity variations. These techniques help the model generalize better by simulating the variability found in real medical images.[2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id524)

Regularization techniques

Common regularization techniques can be effective for tasks like segmenting roofs from satellite images but may not be as suitable for cancer detection.

_Dropout_ prevents overfitting by ensuring that the model doesn’t rely too heavily on any individual neurons. This method is effective for tasks where the dataset might not be extremely large and overfitting is a common concern.

_L2 regularization_ (weight decay) adds a penalty proportional to the sum of the squared weights of the model. This is particularly helpful if the model has a large number of parameters, because it helps to prevent the weights from becoming too large and thereby reduces overfitting, which is typical in high-resolution image segmentation tasks. _Early stopping_ is another effective regularization technique. It involves monitoring the model’s performance on a validation set and stopping training when performance stops improving, thus preventing overfitting.

Loss functions

Choose loss functions[3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id530) to focus on spatial accuracy and boundary precision, such as _Intersection over Union_ (IoU) loss or _Dice Loss_. These loss functions are tailored to handle large-scale, high-resolution images where the primary challenge is accurately delineating roof boundaries amid varying background conditions. However, medical image datasets are often highly imbalanced: for instance, cancerous regions are rare compared to healthy tissue. Loss functions like _Focal Loss_ or _Compound Loss_ (a combination of Dice Loss and Cross-Entropy Loss) are typically used to address this imbalance and focus the model’s learning on the difficult, minority-class instances. Focal Loss is designed to address the classification of rare classes by introducing a modulation term to the standard Cross-Entropy Loss. This modulation term down-weights the loss assigned to well-classified examples, thereby focusing more on hard, misclassified examples. Dice Loss measures the overlap between predicted and true regions by computing the Dice Coefficient, which ranges from 0 to 1. Dice Loss is 1 minus the Dice Coefficient, emphasizing correct predictions for both foreground and background classes and effectively handling class imbalances by focusing on the overlap between predicted and true regions. _Dice Focal Loss_ puts high emphasis on the segmentation boundaries, ensuring accurate boundary delineation, which can be helpful to distinguish healthy from cancerous tissue.

# Data Augmentation Libraries

For data augmentation tasks like random cropping and flipping, I recommend the [torchvision.transforms library](https://oreil.ly/iXa90). Additionally, libraries such as [Albumentations](https://albumentations.ai/) and [Kornia](https://oreil.ly/rXnmX) perform various augmentation tasks efficiently.

As you’ve learned, you must tailor your choice of loss functions and regularization techniques to the specific characteristics and challenges of the task at hand. The nature of the images, the distribution of the data, and the specific requirements of accuracy and precision dictate these choices, highlighting the need for a customized approach in each scenario.

# Swin Transformer V2

Since the introduction of AlexNet,[4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id539) architectures have grown deeper and larger, significantly advancing various visual tasks and driving the deep learning wave in computer vision, with notable examples such as VGG[5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id541) and ResNet.[6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id543) However, even though CNN architectures have been scaled up to around 1 billion parameters as of this writing in 2025, this increase in size has not necessarily led to proportionate improvements in performance.

Swin Transformer V2[7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id546) is a dense vision model with 3 billion parameters. Its developers had to address several issues. For example, to address instability in training large vision models, they introduced a new normalization configuration called _res-post-norm_. In this approach, each residual block’s output is normalized before merging back into the main branch, preventing amplitude accumulation and incorporating an additional layer normalization every six transformer blocks for further stabilization in large model training.

_Scaled cosine attention_, which computes the attention logit of a pixel pair  and , is used to stabilize attention values. Compare this approach with the original self-attention computation, where similarity terms of pixel pairs are calculated as a dot product of the query and key vectors. This often results in attention maps dominated by a few pixel pairs in large visual models, especially in the _res-post-norm_ configuration. The formula for scaled cosine attention is as follows:

Here,  is the relative position bias between  and , and  is a learnable scalar set larger than 0.01 and not shared across heads and layers. This cosine function is naturally normalized, resulting in more stable attention values.

Additionally, Swin Transformer V2 uses a log-spaced continuous position bias (Log-CPB) to handle variations in window size between low-resolution pretraining and high-resolution fine-tuning. More precisely, continuous relative position bias employs a small meta network on the relative coordinates:

Here,  is a small network, such as a 2-layer MLP with ReLU activation. _ReLU_ outputs the input directly if it’s positive; otherwise, it outputs zero, introducing non-linearity into the model while being computationally efficient. This network generates bias values for arbitrary coordinates, allowing seamless transfer to fine-tuning tasks with varying window sizes. You can precompute and store bias values for efficient inference. Additionally, the network uses log-spaced coordinates to address the extrapolation needed for varying window sizes:

Here, , , and ,  are the linear-scaled and log-spaced coordinates, respectively.

Using log-spaced coordinates reduces the extrapolation ratio significantly compared to linear-spaced coordinates, enhancing the model’s performance across different window resolutions. These adaptations enhance the model’s scalability and effectiveness in transferring across different window resolutions, leading to improved performance and flexibility. [Figure 3-4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#swin_transformer) shows this architecture.

![[../../assets/Pasted image 20260518110427.png]]
Figure 3-4. The Swin Transformer V2 architecture incorporates several adaptations for better scaling of model capacity and window resolution: a res-post-norm configuration, scaled cosine attention, and log-spaced continuous relative position bias approach. Image adapted from Ze Liu et al. (2022).

## Image classification with Swin Transformer V2

Now that the theoretical foundations have been laid out, it’s time to see Swin Transformer V2 in action. This section will guide you through the steps to harness its power for your image-classification projects. I’ll use the [snacks dataset](https://oreil.ly/vV_dW), which is a dataset of 20 different types of snack foods. Feel free to replace it with any other image-classification dataset.

To get an idea what your features are, let’s print the labels in your dataset:

```python
print(dataset["train"].features['label'].names)
```

This will result in:

```python
['apple', 'banana', 'cake', 'candy', 'carrot', 'cookie', 'doughnut', 'grape',
'hot dog', 'ice cream', 'juice', 'muffin', 'orange', 'pineapple', 'popcorn',
'pretzel', 'salad', 'strawberry', 'waffle', 'watermelon']
```

To display an image from the dataset, you can do the following:

```python
dataset['test'][1]['image']
```

This will show you the following image:

![[../../assets/Pasted image 20260518110517.png]]

It’s useful to create dictionaries to decode the `ids` and labels in your dataset (see [Example 3-2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#CreateDictionaries)).

##### Example 3-2. Create dictionaries to decode the `ids` and labels

```python
labels = dataset["train"].features["label"].names
num_labels = len(dataset["train"].features["label"].names)
label2id, id2label = dict(), dict()
for i, label in enumerate(labels):
    label2id[label] = i
    id2label[i] = label
```

Next, let’s load the image processor and model (see [Example 3-3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#InitializeProcessor)).

##### Example 3-3. Initialize processor and model

```python
MODEL_PATH = "microsoft/swinv2-tiny-patch4-window8-256"
image_processor  = AutoImageProcessor.from_pretrained(MODEL_PATH)

model = AutoModelForImageClassification.from_pretrained(
    MODEL_PATH,
    label2id=label2id,
    id2label=id2label,
    ignore_mismatched_sizes = True,
)
```

Before you can use the dataset to train your model, you have to preprocess the data (see [Example 3-4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#CustomImagePreprocessing)).

##### Example 3-4. Custom image preprocessing and dataset transforms

```python
class ImageProcessor:
    def __init__(self, image_processor):
        self.normalize = Normalize(mean=image_processor.image_mean,
                        std=image_processor.image_std)

        if "height" in image_processor.size:
            self.size =
            (image_processor.size["height"],
             image_processor.size["width"])
            self.crop_size = self.size
            self.max_size = None
        elif "shortest_edge" in image_processor.size:
            self.size = image_processor.size["shortest_edge"]
            self.crop_size = (self.size, self.size)
            self.max_size = image_processor.size.get("longest_edge")

        self.transforms = Compose([
            Resize(self.size),
            CenterCrop(self.crop_size),
            ToTensor(),
            self.normalize,
        ])

    def preprocess(self, example_batch):
        example_batch["pixel_values"] = [
            self.transforms(image.convert("RGB")) for image in example_batch["image"]
        ]
        return example_batch

processor = ImageProcessor(image_processor)

train_ds.set_transform(processor.preprocess)
val_ds.set_transform(processor.preprocess)
```

As the next step, you can define your training arguments (see [Example 3-5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#DefineTrainingArguments)).

##### Example 3-5. Define training arguments

```python
args = TrainingArguments(
    f"{model_name}-finetuned-snacks",
    remove_unused_columns=False,
    evaluation_strategy = "epoch",
    save_strategy = "epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=4,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=5,
    warmup_ratio=0.2,
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)
```

Now pass this to the `trainer` class to train your model (see [Example 3-6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#InitializeTrainer)).

##### Example 3-6. Initialize Trainer and start training

```python
trainer = Trainer(
    model,
    args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    tokenizer=image_processor,
    compute_metrics=compute_metrics,
    data_collator=collate_fn,
)

trainer.train()
```

The model achieves an accuracy of 91.41%, using this setup. To evaluate your results, you can do the following (see [Example 3-7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#EvaluateResults)).

##### Example 3-7. Evaluate results

```python
trainer.evaluate()
```

To test the model at inference time, you can use the pipeline functionality from Hugging Face (see [Example 3-8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#RunInferencewithHuggingFace)).

##### Example 3-8. Run inference with the Hugging Face image classification pipeline

```python
image_processor = AutoImageProcessor.from_pretrained(name)
model = AutoModelForImageClassification.from_pretrained(name)

pipe = pipeline("image-classification", model=model, image_processor=image_processor)
pipe(image)
```

This will give you the following classification results:

```python
[{'label': 'apple', 'score': 0.9996001124382019},
 {'label': 'watermelon', 'score': 8.05784366093576e-05},
 {'label': 'banana', 'score': 7.75724183768034e-05},
 {'label': 'juice', 'score': 5.8855093811871484e-05},
 {'label': 'pineapple', 'score': 4.748155697598122e-05}]
```

Looks like the model correctly classified the snacks in the image as apples.

# Finding the Right Labeling Tool

I’ve spent a fair share of my time searching for the optimal labeling tool for segmentation tasks. As a rule of thumb, you should decide whether you want easy integration within your workflow and an extensive Python SDK for your labeling tool. Additionally, consider how many people will be working on labeling the data and whether you want to use the tool to create a feedback loop. This involves completing initial labeling, training the model, and then having the labeling team review the predicted masks to retrain the model based on this feedback.

For the first use case, I recommend looking into [Segments.ai’s labeling platform](https://segments.ai/). For the latter use case, consider [Label Studio](https://labelstud.io/). Label Studio is available as open source software and offers various installation methods, including via Docker.

Now that you know how to use transformers for image-classification tasks, let’s move on to the next section and leverage transformers for segmentation tasks.

# Segment Anything

You learned that image segmentation involves identifying which pixels in an image belong to an object, making it a core task in computer vision. However, developing an accurate segmentation model is challenging due to the need for technical expertise, access to AI training infrastructure, and large volumes of carefully annotated in-domain data, which can be very costly.

This is where the _Segment Anything Model_ (SAM)[8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id560) comes in—it’s a foundation model for image segmentation that can be prompted, similar to how you would prompt a language model. These prompts can be bounding boxes, points, text, or basic masks. The model is then trained to output the appropriate mask for the image and the prompt. Besides being a promptable image segmentation model, it excels at zero-shot segmentation tasks.

SAM has three components: an image encoder, a flexible prompt encoder, and a mask decoder. It’s built on top of different transformer-based vision models. The image encoder, for instance, is motivated by Masked Autoencoders Are Scalable Vision Learners (MAE)[9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id561) and ViT with minimal adaption.

The prompt encoder uses two types of prompts: _sparse_ (points, boxes, text) and _dense_ (masks). Points and boxes are represented by positional encodings combined with learned embeddings for each prompt type, while free-form text is encoded using a text encoder from Contrastive Language-Image Pretraining (CLIP).[10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id566) Dense prompts, such as masks, are embedded with convolutions and combined element-wise with the image embedding.

The _mask decoder_ maps the image embedding, prompt embeddings, and an output token to a mask. Inspired by previous designs, it uses a modified transformer decoder block followed by a dynamic mask prediction head. This decoder block uses prompt self-attention and cross-attention in both directions (prompt-to-image embedding and vice versa) to update all embeddings. After two blocks, the image embedding is upsampled, and an MLP maps the output token to a dynamic linear classifier, which computes the mask foreground probability at each image location. [Figure 3-5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#SAM_architecture) illustrates the model’s architecture.

![[../../assets/Pasted image 20260518110714.png]]

Figure 3-5. Overview of the Segment Anything Model. An image encoder generates an image embedding, which can be queried using various input prompts (mask, points, box, text) through the prompt encoder. The mask decoder processes these embeddings to produce object masks along with their associated confidence scores. Image adapted from Alexander Kirillov et al. (2023).

[Example 3-9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#Prompt_example_SAM) demonstrates how feeding the model a set of 2D points can predict a segmentation mask. The more 2D points you provide, the more accurate the resulting mask will be.

##### Example 3-9. Use 2D points to predict a mask with SAM

```python
input_points = [[[300, 250]]]
show_points_on_image(raw_image, input_points[0])

inputs = processor(raw_image, input_points=input_points,
         return_tensors="pt").to(device)
inputs.pop("pixel_values", None)
inputs.update({"image_embeddings": image_embeddings})

with torch.no_grad(): outputs = model(**inputs)

masks = processor.image_processor.post_process_masks(outputs.pred_masks.cpu(),
        inputs["original_sizes"].cpu(), inputs["reshaped_input_sizes"].cpu())
scores = outputs.iou_scores
```

As illustrated in the final part of the SAM overview, this will produce the following output for the scores:

```python
tensor([[[1.0003, 0.9940, 0.6576]]], device='cuda:0')
```

You can then use the best fitting score as a basis to create the mask for your segmentation task. The following code shows how you can show the mask on the images (see [Example 3-10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#ShowMasksOnImages)).

##### Example 3-10. Show masks on images

```python
def show_masks_on_image(raw_image, masks, scores):
    if len(masks.shape) == 4:
        masks = masks.squeeze() 1
    if scores.ndim > 0 and scores.shape[0] == 1:
        scores = scores.squeeze() 2

    image_array = np.array(raw_image)
    nb_predictions = scores.shape[0] if scores.ndim > 0 else 1
    fig, axes = plt.subplots(1, nb_predictions, figsize=(15, 5 * nb_predictions))
    if nb_predictions == 1:
        axes = [axes]

    for i, mask in enumerate(masks):
        mask = mask.cpu().detach().numpy() 3

        contours, _ = cv2.findContours((mask * 255).astype(np.uint8),
                    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 4

        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            cv2.polylines(image_array, [approx], True, (255, 0, 0), 3) 5

        axes[i].imshow(image_array)

        if scores.ndim == 0:
            score_text = f"{scores.item():.3f}"
        elif scores.ndim > 0 and scores.numel() == 1:
            score_text = f"{scores.item():.3f}"
        elif scores.ndim > 0:
            score_val = scores[i].item() if scores[i].numel() == 1 else scores[i]
            score_text = f"{score_val:.3f}" if
                isinstance(score_val, float) else "Multiple"

        axes[i].set_title(f"Mask {i+1}, Score: {score_text}")
        axes[i].axis("off")
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO2-1)

Remove any extra dimensions from the masks.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO2-2)

Remove any extra dimensions from the scores.

[![3](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/3.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO2-3)

Convert the mask tensor to a NumPy array.

[![4](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/4.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO2-4)

Find contours in the mask.

[![5](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/5.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO2-5)

Draw the contours on the image.

I use OpenCV, which is an open source computer vision library, to get the contours of the mask and draw the polygon lines. If you want to refine your segmentation, I suggest the [segmentation refinement library](https://oreil.ly/2o0Dy).

# Variations of SAM

There are several variations of SAM that can help you develop your model more quickly for your specific task. One version is tailored for medical images, with the [code](https://oreil.ly/la7l0) freely available.[11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id570) Additionally, a [Python package](https://samgeo.gishub.org/) exists for segmenting geospatial data with SAM. [Grounding DINO](https://oreil.ly/gxExM) aims to detect and segment anything using text inputs.

HQ-SAM[12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id571) enhances SAM with the ability to accurately segment any object while preserving its original promptable design, efficiency, and zero-shot generalizability. Another variant is ClassWise-SAM-Adapter (CWSAM),[13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id572) which adapts the high-performing SAM for landcover classification on satellite images. This model could be particularly useful for classifying disaster areas after weather damage.

Now it’s time to dive in and try SAM out for yourself in the next section.

## Fine-Tuning SAM on a Custom Dataset

In this section, you’ll learn how you can fine-tune SAM on your custom dataset. I’ll show you how you can create a study object and specify the direction of the optimization with [Optuna](https://optuna.org/). In addition, you’ll log sample images and masks to [Weights & Biases](https://wandb.ai/). This helps you to compare the ground truth mask and the predicted mask at specified intervals and gives you an additional way to track and improve your model’s performance. I’ll use a [medical image dataset](https://oreil.ly/DOkYK) designed to help detect breast cancer.

### Preparing your data for SAM

It’s important to understand how to properly prepare your data. Each example in your dataset should include the following components:

Pixel values

This is the image data formatted and ready for the model.

Prompt

A mask, points, bounding box, or text that serves as the input prompt for the model.

Ground truth segmentation mask

The actual segmentation mask for validation.

[Example 3-11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#GetBoundingBox) presents a function that shows how you can generate a bounding box prompt based on the ground truth segmentation.

##### Example 3-11. Get bounding box

```python
dedef get_bounding_box(mask):
    y_coords, x_coords = np.nonzero(mask > 0) 1

    x_start, x_end = np.min(x_coords), np.max(x_coords) 2
    y_start, y_end = np.min(y_coords), np.max(y_coords)

    height, width = mask.shape 3
    x_start = max(0, x_start - np.random.randint(0, 20))
    x_end = min(width, x_end + np.random.randint(0, 20))
    y_start = max(0, y_start - np.random.randint(0, 20))
    y_end = min(height, y_end + np.random.randint(0, 20))

    bounding_box = [x_start, y_start, x_end, y_end] 4

    return bounding_box
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO3-1)

Find the indices of nonzero elements in the mask.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO3-2)

Determine the minimum and maximum x and y coordinates.

[![3](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/3.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO3-3)

Apply random perturbation to the bounding box coordinates. _Random perturbation_ applies small, random modifications to data or parameters to enhance robustness and prevent overfitting.

[![4](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/4.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO3-4)

Create the bounding box.

Now, to generate the actual dataset, you can leverage the `Dataset` class from PyTorch (see [Example 3-12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#CreatetheDataset)).

##### Example 3-12. Create the dataset

```
class
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO4-1)

Generate the bounding box from the mask.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO4-2)

Prepare the image and bounding box for the model.

[![3](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/3.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO4-3)

Remove the batch dimension added by the transformer.

[![4](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/4.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO4-4)

Include the ground truth mask.

Next, you can use the `DataLoader` class from PyTorch to retrieve batches from the dataset:

```python
train_dataloader = DataLoader(train_dataset, batch_size=2, shuffle=True)
```

### Setting up the model and logging with Weights & Biases

As a next step, you have to load the SAM model. To ensure that gradients are computed only for the mask decoder, freeze the parameters of the vision encoder and prompt encoder (see [Example 3-13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#LoadSAMandFreezeVision)).

##### Example 3-13. Load SAM and freeze the vision and prompt encoders

```python
model = SamModel.from_pretrained("facebook/sam-vit-base") 1

for param_name, parameter in model.named_parameters(): 2
    if param_name.startswith(
        "vision_encoder") or param_name.startswith("prompt_encoder"):
        parameter.requires_grad = False
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO5-1)

Load SAM from Hugging Face.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO5-2)

Ensure that gradients are computed only for the mask decoder.

Now initialize a new Weights & Biases project (see [Example 3-14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#InitializeWeightsBiasesProject)).

##### Example 3-14. Initialize a Weights & Biases project

```python
wandb.init(project='image segmentation')
```

### Preparing the hyperparameter tuning

Now it’s time to set up the hyperparameter tuning with Optuna (see [Example 3-15](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#DefineOptunaObjective)).

##### Example 3-15. Define the Optuna objective and training loop

```python
def objective(trial):
    lr = trial.suggest_float("lr", 1e-6, 1e-3, log=True) 1
    weight_decay = trial.suggest_float("weight_decay", 0, 1e-3)
    num_epochs = trial.suggest_int("num_epochs", 10, 50)
    sigmoid = trial.suggest_categorical("sigmoid", [True, False])
    squared_pred = trial.suggest_categorical("squared_pred", [True, False])

    model.to(device) 2
    optimizer = Adam(model.mask_decoder.parameters(), lr=lr,
                    weight_decay=weight_decay)
    seg_loss = monai.losses.DiceFocalLoss(sigmoid=sigmoid,
                squared_pred=squared_pred, reduction='mean')

    model.train()
    for epoch in range(num_epochs):
        epoch_losses = []
        for batch_idx, batch in enumerate(tqdm(train_dataloader)):
            # Forward and backward passes
            outputs = model(pixel_values=batch["pixel_values"].to(device),
                            input_boxes=batch["input_boxes"].to(device),
                            multimask_output=False)
            predicted_masks = outputs.pred_masks.squeeze(1)
            ground_truth_masks = batch["ground_truth_mask"].float().to(device)
            loss = seg_loss(predicted_masks, ground_truth_masks.unsqueeze(1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_losses.append(loss.item())

        trial.report(np.mean(epoch_losses), epoch)

        if trial.should_prune(): 3
            raise optuna.exceptions.TrialPruned()

    return np.mean(epoch_losses)
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO6-1)

Suggest values for the hyperparameters.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO6-2)

Set up the model, optimizer, and loss functions.

[![3](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/3.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO6-3)

Handle pruning based on the intermediate value.

After defining the function with your desired hyperparameters, create a new study to run your trials (see [Example 3-16](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#CreateRunOptunaStudy)).

##### Example 3-16. Create and run an Optuna study

```python
study = optuna.create_study(direction="minimize") 1
study.optimize(objective, n_trials=5)

print("Best trial:")
trial = study.best_trial
print(f"  Value: {trial.value}")
print("  Params: ")
for key, value in trial.params.items():
    print(f"    {key}: {value}")
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO7-1)

Create a study object and specify the direction of the optimization.

### Use the best hyperparameters to fine-tune SAM

When the hyperparameter tuning is finished, which usually takes around 4–5 hours, you can access the best parameters directly to fine-tune your model (see [Example 3-17](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#ConfigureOptimizerLoss)).

##### Example 3-17. Configure optimizer and loss with best trial parameters

```python
optimizer = Adam(model.mask_decoder.parameters(),
                lr=trial.params.get("lr"),
                weight_decay=trial.params.get("weight_decay")) 1

seg_loss = monai.losses.DiceFocalLoss(sigmoid=trial.params.get("sigmoid"),
                        squared_pred=trial.params.get("squared_pred"),
                        reduction='mean') 2
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO8-1)

Use the `trial.params.get ("hyperparameter_name")` to get each needed hyperparameter directly for tuning the model.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO8-2)

Use Dice Focal Loss to make sure the model puts high emphasis on the segmentation boundaries, ensuring accurate boundary delineation.

With the optimizer and loss in place, you now can move on to fine-tuning the model (see [Example 3-18](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#FineTuneSAMSelectedHyperparameters)).

##### Example 3-18. Fine-tune SAM with the selected hyperparameters and log results

```python
num_epochs = trial.params.get("num_epochs")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.train()

for epoch in range(num_epochs):
    epoch_losses = []
    for batch_idx, batch in enumerate(tqdm(train_dataloader)):
        outputs = model(pixel_values=batch["pixel_values"].to(device),
                        input_boxes=batch["input_boxes"].to(device),
                        multimask_output=False) 1

        predicted_masks = outputs.pred_masks.squeeze(1)
        ground_truth_masks = batch["ground_truth_mask"].float().to(device)
        loss = seg_loss(predicted_masks, ground_truth_masks.unsqueeze(1)) 2

        optimizer.zero_grad() 3
        loss.backward()

        optimizer.step() 4
        epoch_losses.append(loss.item())

        if batch_idx % 5 == 0: 5
            image_to_log = batch["pixel_values"][0].permute(1, 2, 0).cpu().numpy()6
            predicted_mask_to_log = predicted_masks[0].cpu().detach().numpy() 7
            ground_truth_mask_to_log = ground_truth_masks[0].cpu().detach().numpy()

            wandb.log({
                "Input Image": wandb.Image(image_to_log, caption="Input Image"),
                "Predicted Mask": wandb.Image(predicted_mask_to_log,
                                caption="Predicted Mask"),
                "Ground Truth Mask": wandb.Image(ground_truth_mask_to_log,
                                caption="Ground Truth Mask")
            }, commit=False) 8

    wandb.log({'epoch': epoch, 'mean_loss': mean(epoch_losses)}) 9

    print(f'EPOCH: {epoch}')
    print(f'Mean loss: {mean(epoch_losses)}')
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-1)

Run forward pass.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-2)

Compute loss.

[![3](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/3.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-3)

Run backward pass (compute gradients with respect to loss).

[![4](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/4.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-4)

Optimize.

[![5](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/5.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-5)

Log sample images and masks to Weights & Biases (wandb) at a specified interval.

[![6](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/6.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-6)

Select the first sample in the batch for logging.

[![7](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/7.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-7)

Convert to Height, Width, Channels (HWC) format for wandb.

[![8](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/8.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-8)

Log using wandb, and use `commit=False` to accumulate logs.

[![9](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/9.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO9-9)

Log mean loss for the epoch outside the inner loop.

Logging to Weights & Biases will result in two graphs: one for the mean loss and one for the epochs, as shown in [Figure 3-6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#loss_epochs_wandb).

![[../../assets/Pasted image 20260518111131.png]]

Figure 3-6. Mean loss and epochs of the training.

Logging these metrics is beneficial for several reasons. First, tracking the mean loss and epochs helps you to monitor training progress and identify potential issues, such as overfitting or underfitting. By visualizing these metrics, you can make more informed decisions about adjusting hyperparameters or training duration.

In addition to the graphs, you can create a combined panel for the original image, the predicted mask, and the ground truth mask from the logged training data, as shown in [Figure 3-7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#image_pred_ground_truth_wandb).

![[../../assets/Pasted image 20260518111140.png]]

Figure 3-7. This panel gives you a way of directly stepping through the prediction results of your model.

This combined panel allows you to qualitatively assess the model’s performance. By directly comparing the predictions to the ground truth, you can identify specific areas where the model excels or struggles. This can provide insights into potential improvements in data preprocessing, augmentation strategies, or loss function. Additionally, being able to step through different prediction results helps to ensure that the model’s performance is consistent across various samples in the dataset.

In addition, you can very easily create a report from the logged data and share it with team members and other stakeholders.

# Segment Anything in Images and Videos

Even though this chapter focuses on image-based tasks, we can view videos as sequences of images. From this perspective, models that generalize across both domains can be seen as natural extensions of image-based architectures. Segment Anything Model 2 (SAM 2)[14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id581) is exactly such a case: it builds upon the original SAM architecture I introduced you to in the previous section. It extends the model into the temporal domain, enabling promptable segmentation not only in images but also across video frames. [Figure 3-8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#SAM2Architecture) shows the architecture of SAM 2.

![[../../assets/Pasted image 20260518111150.png]]

Figure 3-8. Segment Anything Model 2 architecture.

The core innovation of SAM 2 is the introduction of a _Promptable Visual Segmentation_ (PVS) task, which unifies the segmentation process across both modalities. In this task, you provide a prompt, such as a click, bounding box, or mask, on any frame of a video. The model then generates a corresponding segmentation mask for that frame and propagates this information temporally to generate a consistent segmentation across the entire video sequence. To achieve this, SAM 2 uses a streaming transformer architecture equipped with a memory. The model processes video frames one at a time. For each frame, the model uses a memory attention mechanism that refers back to previous predictions and prompts to maintain temporal consistency. This memory system is composed of spatial memories from past frames, prompted frame memories with corrective information, and object pointers that summarize the object identity. These are stored in fixed-size memory queues, allowing the model to operate efficiently even on long video sequences.

The core components of SAM 2 resemble those of the original SAM model. The image encoder is based on a hierarchical transformer trained with a masked autoencoding objective. It processes each video frame and produces multiscale feature embeddings. The prompt encoder converts user inputs into embeddings using either positional encoding for sparse prompts or convolutional layers for dense prompts like masks. The mask decoder receives the image features, prompt embeddings, and memory context to produce the segmentation mask for the current frame. This decoder uses two-way attention blocks, similar to the ones in SAM, to refine both prompt and image features. If the object is ambiguous or partially visible, the model predicts multiple candidate masks and ranks them using predicted intersection-over-union scores.

SAM 2 adds a memory encoder that transforms predictions and image features into a representation suitable for storage. These memory entries are used later by the memory attention module to provide context to future frames. When the model encounters frames where the object is no longer visible due to occlusion or motion, it can explicitly predict the absence of the object, avoiding spurious mask generation.

But enough of the theory—let me show you how you can actually use SAM 2 for video segmentation. In the [book’s repo](https://oreil.ly/github-transformers) you find a Jupyter notebook called `segment_videos_with_sam2.ipynb` with all the code. Here, I’ll focus on the important parts.

SAM 2 is available in four model sizes, starting from the lightweight “`sam2_hiera_tiny`” with 38.9 million parameters up to the more powerful “`sam2_hiera_large`” with 224.4 million parameters. In the code example, I’ll use `sam2.1_hiera_large.pt`, which is the checkpoint for the larger model. How to properly load the model is shown in [Example 3-19](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#LoadSAM2).

##### Example 3-19. Load SAM 2

```python
sam2_checkpoint = "../checkpoints/sam2.1_hiera_large.pt"
model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"

sam2_model = build_sam2_video_predictor(model_cfg, sam2_checkpoint, device=device)
```

I have a video prepared for you to test the model out. It’s important for you to know that you need to split the video in separate images before you can use SAM 2. [Figure 3-9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#FirstFrameVideo) shows the first frame of the video.

![[../../assets/Pasted image 20260518111235.png]]

Figure 3-9. First frame of the video.

To convert a video into frames of images, you can use [FFmpeg](https://ffmpeg.org/). FFmpeg is a multimedia framework that handles nearly any video format. It supports decoding, encoding, streaming, and filtering, and it runs on Linux, macOS, and Windows. We’ll run it in Google Colab—that is, in a Linux environment (see [Example 3-20](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#RunLinuxEnvironment)).

##### Example 3-20. Run in Linux environment

```bash
!apt-get update
!apt-get install ffmpeg

!mkdir -p frames
!ffmpeg -i movie_players.mp4 -q:v 2 -start_number 0 frames/%05d.jpg
```

This code first installs the library and then creates a new folder and converts the video into _jpg_ files.

To segment with SAM 2, we need to initialize an inference state for the video, using stateful inference for interactive video segmentation. During this initialization, all _jpg_ frames from your `frames_path` are loaded, and their pixel data is stored in `inference_state = sam2_model.init_state(video_path=video_dir)`.

To make it easier to select an object from the image frame in a Jupyter notebook, you can use [Jupyter BBox Widget](https://oreil.ly/-rXqW). To use this library, you need to create an `object` class, and then you can easily annotate your frame with bounding boxes and convert them into points for SAM 2. This is shown in [Example 3-21](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#BBWidget).

##### Example 3-21. Use BBox Widget for easily creating points

```python
OBJECT = ['ball']

widget = BBoxWidget(classes=OBJECT)
widget.image = encode_image("/content/frames/00000.jpg")

box = widget.bboxes[0] if widget.bboxes else default_box[0]
points = np.array([[box['x'], box['y']]], dtype=np.float32) 1
points
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO10-1)

Convert box to point format expected by the model.

To apply point prompts across all video frames, you need to use the `propagate_in_video` generator. Each iteration yields `frame_idx`, the index of the current frame; `object_ids`, the IDs of detected objects; and `mask_logits`. The associated logit values can then be converted into masks through thresholding. [Example 3-22](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#AddPoints) shows the first step of the process.

##### Example 3-22. Add points to predictor

```python
ann_frame_idx = 0 1
ann_obj_id = 1  2

labels = np.array([1], np.int32)
_, out_obj_ids, out_mask_logits = sam2_model.add_new_points_or_box(
    inference_state=inference_state,
    frame_idx=ann_frame_idx,
    obj_id=ann_obj_id,
    points=points,
    labels=labels,
)
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO11-1)

The frame index to interact with

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO11-2)

Unique ID for each object

Next, you can propagate through the frames, as demonstrated in [Example 3-23](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#propagateFramesSAM2).

##### Example 3-23. Add points to predictor

```
video_segments
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO12-1)

Contains the per-frame segmentation results.

After that, you can simply select frames from the image to plot. The results of the segmentation of the ball in the video at frame 0 and frame 120 is shown in Figures [3-10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#VideoFrame0Seg) and [3-11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#VideoFrame120Seg), respectively.

![[../../assets/Pasted image 20260518111411.png]]

###### Figure 3-10. Video frame 0 with segmented ball.

![[../../assets/Pasted image 20260518111421.png]]

###### Figure 3-11. Video frame 120 with segmented ball.

The result is very good. SAM 2 successfully segmented the ball even in front of one of the players.

However, SAM 2 improved over SAM, and not just in terms of adding video segmentation. It segments images six times faster than SAM and requires three times fewer interactions to reach the same quality. To achieve this performance, the model was trained on a large-scale dataset called _SA-V_. The dataset includes over 35 million masks from more than 50 thousand videos. It was collected using a model-in-the-loop annotation engine that integrates human feedback and iterative prompting to refine annotations.

# SAM 2 Integrations

For a seamless experience, you can try [SAM2 Studio](https://oreil.ly/hqx12), a native macOS app developed by Hugging Face that makes image segmentation fast and intuitive. Popular labeling platforms like [Label Studio](https://oreil.ly/Uq1vy) also offer built-in support for SAM 2. Label Studio is available both as an open source tool and an enterprise solution.

With its universal visual segmentation system, SAM 2 is well-suited for real-world applications such as augmented reality (AR), robotics, autonomous navigation, and video editing. It can be used as a plug-and-play solution for segmentation or fine-tuned for domain-specific tasks.

# Segment Videos and Images with Concept Prompts

SAM 3[15](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id590) introduces a new way of segmenting images and videos with concept prompting. The Segment Anything models evolved across three generations, each building on the strengths of the previous one. Because these capabilities stack rather than replace one another, this chapter covers all three to show how they connect, how they differ, and how to apply them in practical media workflows. [Table 3-1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#sam_evolution_overview) illustrates this evolution.

Table 3-1. SAM model evolution

|Capability/feature|SAM 1|SAM 2|SAM 3|
|---|---|---|---|
|Core purpose|Segment any object from a single click|Segment and track any object in image/video|Detect, segment, and track instances of any category using text or examples|
|Input modalities|Click|Click, box, or mask prompts|Text prompts, example images, clicks, and follow-up guidance|
|Segment an object from a click|✔|✔|✔|
|Track segmented objects in videos|✘|✔|✔|
|Refine prediction with follow-up clicks|✔|✔|✔|
|Detect and segment matching instances from text|✘|✘|✔|
|Refine detection with visual examples (prompt by example)|✘|✘|✔|
|Example-based concept matching|✘|✘|✔|
|Category-agnostic segmentation|✔|✔|✔ (plus text-driven, instance-level detection)|

SAM 3 generalizes SAM 2 by supporting both the traditional _promptable visual segmentation_ (PVS) tasks and the new _promptable concept segmentation_ (PCS) task for concept-based segmentation. It accepts concept prompts like noun phrases or image exemplars, as well as visual prompts such as points, boxes, and masks, to define objects that are segmented across space and time. Prompts can be iteratively added to refine targets, remove false positives, or recover missed objects. The architecture builds on SAM and modulated end-to-end detector ((M)DETR),[16](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id597) combining a dual encoder-decoder detector for image segmentation with a tracker and memory module for video. These components run on top of a shared perception encoder (PE)[17](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id598) backbone that aligns vision and language inputs. [Figure 3-12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#SAM_3_archi) shows an overview of the architecture, as well as the new components of SAM 3.

![[../../assets/Pasted image 20260518111433.png]]

Figure 3-12. SAM 3 architecture. New components are in light gray, SAM 2 components are in dark gray, and components from the perception encoder are in white. Image adapted from Nicolas Carion et al. (2025).

The following section explains each component in more detail, describing how they contribute to the overall system and how SAM 3 extends the SAM 2 pipeline to support PCS:

Detector architecture

The detector follows a DEtection TRansformer (DETR)-style design where image features and prompt tokens are fused to condition object detection on text or exemplar inputs. Learned queries attend to these conditioned features to classify and localize objects, predicting both presence and bounding box adjustments. A mask head and semantic segmentation head generate object masks and pixel labels aligned to the prompt.

Presence token

The presence token separates recognition from localization by predicting whether the target concept exists in the image before localization occurs. This prevents detection queries from being overloaded with both global understanding and local positioning, improving reliability when concepts appear ambiguously or sparsely.

Image exemplars and interactivity

Image exemplars provide a bounding box and positive or negative label to guide detection and can be used with or without text prompts. They allow the model to detect all matching instances rather than just one and can be interactively added to correct false positives or false negatives during refinement.

Tracker and video architecture

For video, SAM 3 combines the detector with a tracker and memory module to maintain consistent object identities across frames. New detections are introduced, while tracked objects are propagated forward as masklets, forming spatial-temporal masks that persist through the sequence.

Tracking an object with SAM 2–style propagation

Propagation predicts updated masklet positions for tracked objects using a mechanism similar to SAM 2, sharing the same image encoder and drawing on a memory bank for appearance cues. The tracker updates masks frame-by-frame based on past context, user prompts, and conditioning frames without re-running full detections each time.

Matching and updating based on detections

Propagated masklets and current detections are aligned with an _intersection over union_ (IoU) based matching function to maintain identity. IoU measures object detection performance by calculating how much the predicted bounding box overlaps with the ground truth bounding box. Masklets that fail to match consistently are suppressed, while new detections spawn new masklets. High-confidence detections periodically reset the tracker to correct drift from occlusions or distractors.

Instance refinement with visual prompts

After initial segmentation, users can refine masks with positive or negative clicks. These prompts guide the mask decoder to adjust object boundaries, and in video the refinement propagates across frames to update the corresponding masklet throughout the sequence.

Using SAM 3 is straightforward. Note that I’ll omit some code here, but you’ll find all code in the notebook of the [book’s repository](https://oreil.ly/github-transformers). [Example 3-24](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#SAM_3_image) walks you through loading the model and processor and how to segment an object with a text prompt. Here, I decided to have the model select the cats in the image.

##### Example 3-24. SAM 3 for image segmentation

```python
model = Sam3VideoModel.from_pretrained(
    "facebook/sam3").to(device, dtype=torch.bfloat16)
processor = Sam3VideoProcessor.from_pretrained("facebook/sam3")

video_url = "/content/movie_players.mp4"
video_frames, _ = load_video(video_url) 1

inference_session = processor.init_video_session(
    video=video_frames,
    inference_device=device,
    processing_device="cpu",
    video_storage_device="cpu",
    dtype=torch.bfloat16,
)

text = "active ball"
inference_session = processor.add_text_prompt(
    inference_session=inference_session,
    text=text,
)

outputs_per_frame = {}
for model_outputs in model.propagate_in_video_iterator(
    inference_session=inference_session, max_frame_num_to_track=50
):
    processed_outputs = processor.postprocess_outputs(
        inference_session, model_outputs)
    outputs_per_frame[model_outputs.frame_idx] = processed_outputs

print(f"Processed {len(outputs_per_frame)} frames")

frame_idx = 0 2
frame_outputs = outputs_per_frame[frame_idx]
masks = frame_outputs["masks"] 3
frame = video_frames[frame_idx] 4

overlay = overlay_masks_on_frame(frame, masks, alpha=0.5)
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO13-1)

Load local image.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO13-2)

Segment using text prompt.

[Figure 3-13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#segmented_image_SAM_3) shows the image and the masks selected by SAM 3.

![A puppy and two kittens running through a garden, overlaid with colored masks highlighting each animal.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/ttdg_0313.png)

###### Figure 3-13. Image with mask overlay.

For SAM 2, I showed you the example of selecting an object in a video and propagating this throughout the video. You can do the same with SAM 3, now just by using the concept prompt “ball.” To demonstrate how you can use SAM 3, let’s reuse the same video, the two basketball players. [Example 3-25](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#SAM_3_video_Segmentation) walks you through the important steps to achieve this.

##### Example 3-25. Use SAM 3 for video segmentation

```
model
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO14-1)

List of frames

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/2.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO14-2)

Visualization of one frame (for example, frame 0)

[![3](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/3.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO14-3)

Shape (`num_objects`, H, W)

[![4](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/4.png)](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#co_transformers_for_vision_tasks_CO14-4)

Python Imaging Library (PIL) image or NumPy array

[Figure 3-14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#SAM_3_balls_selected) depicts one video frame of the segmentation.

![[../../assets/Pasted image 20260518111546.png]]

Figure 3-14. Segmented video frame.

If you look more closely at this frame, you can see a potential issue. When you prompt the model with something simple like “ball,” it will segment every ball it recognizes, including the one lying quietly in the background. If your goal was to select only the active ball the two players are using, the model has no way to infer that nuance from such a minimal prompt. However, there is a way to handle this. By moving beyond basic prompts, you can guide the model with more specific instructions. If you want to see how to take this further, [“Combining Capabilities: SAM 3 Agent”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch12.html#SAM_3_agent_section) demonstrates how to use richer prompts for segmentation, such as “leftmost orange yarn ball.”

# Conclusion

In this chapter, you learned about the game-changing impact of vision transformers, such as Swin Transformer V2 and the Segment Anything Model, and the latest SAM 2 for video segmentation.

You explored the key modifications that enhanced the scalability and performance of Swin Transformer V2, including the introduction of the res-post-norm configuration, scaled cosine attention, and log-spaced continuous position bias. These innovations address the challenges of training instability, effective attention computation, and varying window sizes, leading to better model performance.

You then saw how SAM enables prompt-based segmentation with zero-shot capabilities and how SAM 2 builds on this by extending segmentation into the video domain. With a memory-augmented transformer architecture and a unified promptable visual segmentation task, SAM 2 ensures temporal consistency across frames and supports real-time processing. It significantly improves efficiency, requiring fewer interactions and delivering faster predictions, making it ideal for tasks like AR, robotics, and video editing.

SAM 3 takes this evolution one step further by adding concept prompting. Instead of reacting only to visual cues like clicks or boxes, the model can now respond to text instructions, example images, and combined prompts to segment specific instances, categories, or semantic concepts. This expands the promptable visual segmentation task into promptable concept segmentation, where the user defines what to find and the model aligns language, exemplars, and vision features to execute it. The architecture builds on SAM 2 but replaces simple interaction loops with a detector that fuses prompts and image features, a presence token that separates existence from localization, and a tracker that maintains identities across time.

Throughout the chapter, you also worked with Optuna for hyperparameter tuning, and Weights & Biases for tracking and visualizing experiments. These tools streamline your development workflow and provide insights that support more effective model development and evaluation.

In [Chapter 4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch04.html#chapter_4), we stay in the image domain, but now we don’t segment or classify them; we generate new ones based on a prompt input.

[1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id508-marker) Alexey Dosovitskiy et al. [“An Image Is Worth 16x16 Words: Transformers for Image Recognition at Scale”](https://arxiv.org/abs/2010.11929) (2020).

[2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id524-marker) Manuel Cossio. [“Augmenting Medical Imaging: A Comprehensive Catalogue of 65 Techniques for Enhanced Data Analysis”](https://arxiv.org/pdf/2303.01178) (2023).

[3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id530-marker) Jun Ma et al. [“Loss Odyssey in Medical Image Segmentation”](https://www.sciencedirect.com/science/article/abs/pii/S1361841521000815) (2021).

[4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id539-marker) Alex Krizhevsky et al. [“ImageNet Classification with Deep Convolutional Neural Networks”](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) (2012).

[5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id541-marker) Karen Simonyan et al. [“Very Deep Convolutional Networks for Large-Scale Image Recognition”](https://arxiv.org/abs/1409.1556) (2014).

[6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id543-marker) Kaiming He et al. [“Deep Residual Learning for Image Recognition”](https://arxiv.org/abs/1512.03385) (2015).

[7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id546-marker) Ze Liu et al. [“Swin Transformer V2: Scaling Up Capacity and Resolution”](https://arxiv.org/pdf/2111.09883) (2022).

[8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id560-marker) Alexander Kirillov et al. [“Segment Anything”](https://arxiv.org/pdf/2304.02643) (2023).

[9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id561-marker) Kaiming He et al. [“Masked Autoencoders Are Scalable Vision Learners”](https://arxiv.org/pdf/2111.06377) (2021).

[10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id566-marker) Alec Radford et al. [“Learning Transferable Visual Models from Natural Language Supervision”](https://arxiv.org/abs/2103.00020) (2021).

[11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id570-marker) Jun Ma et al. [“Segment Anything in Medical Images”](https://arxiv.org/abs/2304.12306) (2023).

[12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id571-marker) Lei Ke et al. [“Segment Anything in High Quality”](https://arxiv.org/abs/2306.01567) (2023).

[13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id572-marker) Xinyang Pu et al. [“ClassWise-SAM-Adapter: Parameter Efficient Fine-Tuning Adapts Segment Anything to SAR Domain for Semantic Segmentation”](https://arxiv.org/html/2401.02326v1) (2024).

[14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id581-marker) Nikhila Ravi et al. [“SAM 2: Segment Anything in Images and Videos”](https://arxiv.org/abs/2408.00714) (2024).

[15](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id590-marker) Nicolas Carion et al. [“SAM 3: Segment Anything with Concepts”](https://arxiv.org/abs/2511.16719) (2025).

[16](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id597-marker) Nicolas Carion et al. [“End-to-End Object Detection with Transformers”](https://arxiv.org/abs/2005.12872) (2020).

[17](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#id598-marker) Daniel Bolya et al. [“Perception Encoder: The Best Visual Embeddings Are Not at the Output of the Network”](https://arxiv.org/abs/2504.13181) (2025).
Since its introduction in 2017, the transformer architecture[1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id294) has revolutionized the field of natural language processing (NLP), marking a paradigm shift toward models capable of natural language understanding (NLU). This shift was possible because transformers process sequential data in parallel, enabling a deeper and more contextual understanding of language than was achievable with previous sequential models, like long short-term memory (LSTM) networks.

In recent years, transformers have evolved to impact a wide array of domains, including computer vision, speech recognition, reinforcement learning, and mathematical operations, moving beyond their initial usage within NLP. Their adaptability has led to significant advancements in machine translation, allowing for context-aware translations, and in scientific research, notably in predicting protein structures with remarkable accuracy.

Among the most exciting developments are reasoning models, which are advanced large language models (LLMs) trained with reinforcement learning to perform complex, multi-step reasoning. They generate internal chains of thought before answering, which is inspired by the human thought process. This technique first solves intermediate steps before getting to the final answer.

I assume in this book that you have at least some familiarity with the transformer architecture. Perhaps you’re read the book [_Natural Language Processing with Transformers_](https://learning.oreilly.com/library/view/natural-language-processing/9781098136789) (O’Reilly), or a similar work. Moreover, I take it you’re not just curious about transformers. You’re here because you want to build real applications with transformers, and you want to do it right.

This chapter provides a focused review of the transformer architecture to set the stage for the more advanced and complex models beyond NLP that I’ll cover in later chapters.

I’ll begin with the basic transformer architecture, then explain how longer context becomes possible, and finish with a tour of various attention mechanisms. Throughout this chapter, and the ones that follow, I’ll share practical insights from real deployments so that you can benefit from my experience and learn the patterns, pitfalls, and principles that matter when theory meets the hard surface of production.

# Transformer Basics

This section explains the main architectural components of the original transformer model, such as encoder and decoder, positional embeddings, and attention mechanism.

The transformer architecture was originally developed for machine translation, a challenging sequence-to-sequence task in which the concept of tokenization plays a critical role. _Tokenization_ breaks down sequences like sentences into manageable units, or tokens, that the transformer can effectively process. For example, in the sentence:

The Transformer has revolutionized NLP.

The word _the_ represents a single word-level token.

Before we dive into the architectural components, understanding tokenization is crucial, as it facilitates the transformer’s ability to interpret text. And it sets the foundation for its application to other sequences.

## Tokenizer: Text Representation in the Transformer

A _tokenizer_ is used to tokenize the text. This is the first step to make natural language digestible for the model, before applying token embeddings and finally positional embeddings. The different types of tokenization are:

Character-level tokenization

_Character-level tokenization_ splits the underlying alphabet into each existing character in the sequence. If you used character-level tokenization for:

```
"The Transformer has revolutionized NLP."
```

it would yield:

```
[_T_, _h_, _e_ ,' _, …​ 'N_, _L_, _P_, _._]
```

This will lead to very long sequences, which can increase computational complexity. It can also be challenging for the model to learn long-term dependencies. Nonetheless, this can be helpful if your task requires a fine-grained understanding.

Word-level tokenization

_Word-level tokenization_ would split the example sentence as follows:

```
[_The_, _Transformer_, …​ _NLP_, _._, ]
```

That is, the sequence will be split into its words, plus punctuation. The downside is that this requires a large vocabulary, and if the language changes, this tokenization will not be able to understand new words.

Subword tokenization

Most modern LLMs use _subword tokenization_, in which the word is split into smaller parts. For instance, a subword tokenizer would split the word _hiking_ into:

```
[_h_, _ik_, _ing_ ]
```

and the word _cooking_ into:

```
[_cook_, _ing_]
```

So subword tokenization splits a word (or sequence) into smaller, commonly occurring chunks, like:

```
[_ing_]
```

Single-character words are also included.

Now that you understand the basics of tokenization, let’s move on to token and positional embeddings.

## Token and Positional Embeddings

A part of the transformer architecture that contains learnable parameters is the token and positional embeddings (PEs). The token embedding is tasked with encoding each vocabulary element into a -dimensional vector in the space of  of  (). The token embedding can mathematically be presented as follows:

Let  be the vocabulary with , where each word  in  is assigned a unique token ID, . The token embedding is a function  that maps each token ID to a -dimensional vector. This is achieved through a token embedding matrix , where  is the dimensionality of the embeddings. Here’s how to do it using bidirectional encoder representations from transformers (BERT):

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased') #1
model = AutoModel.from_pretrained('bert-base-uncased')

sentence = "The Transformer has revolutionized NLP."
inputs = tokenizer(sentence, return_tensors='pt') #2
input_ids = inputs['input_ids'] #3

print(input_ids)
outputs = model(input_ids)

embeddings = outputs.last_hidden_state #4
print(embeddings)

```

1. [Load tokenizer and model from Hugging Face.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO1-1)
2. [Tokenize the sentence.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO1-2)
3. [Get the input IDs and pass them through the model to get the embeddings.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO1-3)
4. [Get the last hidden state, to access the embeddings of the tokens.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO1-4)

This will result in the following output for the input IDs of the sentence:

```python
tensor([[ 101, 1996, 10938, 2121, 2038, 4329, 3550, 17953, 2361, 1012, 102]])
```

For the corresponding embeddings, the output is:

```python
tensor([[[–0.5249, –0.2210,  0.2696,  ..., –0.4204,  0.2605,  0.6457],
         [–0.6665, –0.4994,  0.4651,  ..., –0.2517,  0.2334,  0.0176],
         [ 0.8416, –2.0561,  0.8323,  ..., –0.2709, –0.1999, –0.1918],
         ...,
         [–0.4018, –0.6402,  0.7791,  ..., –0.0290, –0.4070,  0.2974],
         [–0.3327, –0.8091, –0.0304,  ...,  0.4745,  0.3230, –0.5991],
         [ 0.4928, –0.0878, –0.0971,  ...,  0.1629, –0.7012, –0.3848]]],
       grad_fn=<NativeLayerNormBackward0>)
```

This representation lacks the position of the word in the sequence. And since the transformer does not have _recurrence_, meaning that it doesn’t need to process the data sequentially as it was originally represented, you need a function to represent the position. This is why you need to add positional embeddings: without them the model treats sequences as unordered collections of words.

The positional-embedding function learns to encode a token’s location within a sequence into a vector in the space $R^{de}$. The original transformer uses for position $p_i$:

$$
p_i,2t = sin(k/10000^{2t/d})
$$
$$
p_i,2{t+1} = sin(k/10000^{2t/d})
$$

Here, $p_{i,2t}$ is $2t^{th}$ the  element of the -dimensional vector $p_{i}$ . This means that the position of the first token is captured by a vector, $p[1]$, while the position of the second token is captured by a different learned vector, $p[2]$, and so on.

This technique enables transformer models to understand the order of words. In the next section you’ll see how the transformer uses this vector representation to understand and learn from the text.

## Attention Mechanism

The attention mechanism is at the core of the transformer’s ability to understand and interpret text. It gives the model the ability to analyze the relevance of a word in a sequence on a token-to-token basis.

In that context, you’ll often hear the term _attribution matrix_, which is computed from the input embeddings. Here the term _attribution_ refers to the significance between different parts of the input. The attribution matrix is computed with the $Q (query)$ and the $K (key)$ matrices. The resulting scores form the $Q$  and $K$ interaction to determine the attention weights, which are then applied to the  $V (value)$ matrix to produce the output of the attention mechanism:

$$
Attetion (Q,K,V) = Softmax(\frac{QK^{T}}{\sqrt{d_k}}) V
$$

This attribution matrix is crucial for understanding how the model interprets and processes the corresponding input sequences. For instance, by analyzing these scores, you can gain insights into the model’s decision-making process, such as which tokens it sees as more relevant than others when generating the output token. Libraries such as [Captum](https://captum.ai/) help make this decision-making process visible.

However, despite the specific roles of $Q$, $K$, and $V$, the initial computation for each of these matrices follows a similar process: a _linear projection_ of the input embeddings. This means that for each of these matrices, the input embeddings are multiplied by a weight matrix. This process can be mathematically described as follows:

- Query matrix Q: $Q = W_qE$
    
- Key matrix K: $K = W_kE$
    
- Value matrix V: $V = W_vE$
    

Here, $E$ represents the input embeddings, and $W_q$, $W_k$ , and $W_v$  are the weight matrices for the query, key and value projections, respectively. Take the dot product of the query and key matrices, followed by the Softmax function and the scaling factor (for scaled dot attention). The result will be a matrix of scores representing self-attention, or how much focus each token should put on each other token by considering its relationship with every other element in the sequence. These scores are then used to weight the values in the  matrix, producing the final weighted-sum output of the attention mechanism:

$$
Output = AttentionScore * V
$$

This dynamic process allows the model to focus on different parts of the input sequences for each input token, making it possible to understand each token’s contextual relevance and information.

### Multi-head attention

The attention mechanism you’ve seen so far represents the computation performed by a single attention head, which is the component responsible for calculating attention in the transformer. However, the original transformer, as well as state-of-the-art (SOTA) models, applies multiple attention heads simultaneously. Each individual attention head has its own learnable parameters, which are then combined into a single output. This allows the model to integrate information from the same sequence and capture a variety of relationships between its words or elements. This approach enhances the model’s ability to understand and represent complex dependencies in the data.

In technical terms, given input sequences $A$, $B$, and $C$, $...$, the multi-head attention mechanism computes new representations for the elements in $A$ by considering information from $B$, $C$, and so on. This process involves several steps: each head computes its own attention scores and output vectors based on the input, then concatenates and linearly transforms these outputs to produce the final output vector $V$.

This process consolidates the contextual information captured by the individual attention heads into one unified output that encapsulates all critical information across the entire input sequence. Since each attention head might focus on different relationships within the input sequence, this is crucial to the model gaining a better language understanding.

### Bidirectional and unidirectional attention

As I mentioned, the first transformer model was used for machine translation. That’s why it uses two distinct types of attention mechanism within the architecture: one for the encoder and another for the decoder.

First, the encoder applies bidirectional self-attention, not just left-to-right processing, as traditional sequence processing methods do. This means it treats all tokens as context, applying attention to each token in the sequence. This gives the model a full understanding of the entire input sequence when it generates representations for each token.

The decoder’s attention is masked (also called _causal attention_) to prevent the model from attending to future tokens (subsequent positions). In practice, this means that for the prediction , the model can attend to the position . With that method in place, the model generates each token based only on the tokens previously created, from left to right, thus preventing it from using future tokens in the sequence. This is important for all tasks where the model must generate one token at a time, as, for instance, for translation.

Now that you understand the two distinct variations of attention used with the first transformer, let’s look at the encoder and decoder.

## Encoder and Decoder Parts

The first transformer model’s architecture ([Figure 1-1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#decoder_encoder)) was characterized by its encoder-decoder structure. Some subsequent models leverage a decoder-only framework, such as GPT, LLaMA, Mistral, and Falcon.

The encoder itself is composed of six identical layers, each containing two principal components: a multi-head self-attention mechanism and a pointwise fully connected feed-forward network. The term _pointwise_ refers to applying the same linear transformation to each sequence element. These components are further refined with residual connections and layer normalization.

The decoder interprets the encoded information, mirroring the encoder’s layered structure, but introduces an essential feature: _masked multi-head self-attention_. This added feature in the decoder prevents the model from accessing subsequent positions in the sequence.

![Encoder (left) and decoder (right) part of the Transformer architecture](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/ttdg_0101.png)

Figure 1-1. Encoder and decoder part of the transformer architecture.

The model maintains a consistent output dimension of 512 across all sub-layers, including the embedding layers, meaning its maximum sequence length is 512 tokens. This limitation comes mostly from the specific architectural setup of the first transformer model, which made it hard to process longer sequences on the available hardware efficiently.

# Enhancements in Transformer Design: Longer Context and Attention Variations

Now it’s time to look into methods by which modern transformer models, like GPT-4.5 and Qwen3, achieve higher levels of performance and flexibility—in particular, the ability to process more information at once, through longer context windows. Attention-mechanism variations such as multi-query and flash attention also increase the efficiency and accuracy of SOTA transformer models.

## Longer Context Windows with Better Performance

A model’s _context window_ refers to the portion of text it can process when making predictions or generating text. A longer context window allows the model to understand more complex narratives and capture nuances better than it could using a chunked version of a text with a small context window.

However, simply extending the context length results in quadratic increases in time complexity and memory usage, which can constrain improvements. Therefore, recent enhancements, such as _rotary positional embedding_ (RoPE),[2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id340) _position interpolation_ (PI),[3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id343) and _Yet another RoPE extensioN method_ (YaRN),[4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id345) are designed to more effectively manage longer contexts during inference.

RoPE brings _absolute_ and _relative_ PEs together. But before I dive deeper into how RoPE works, let’s first look at the key differences between absolute and relative PEs:

- With absolute PEs, for each token embedding, the model adds information about the absolute position of the token. Absolute PEs are simpler and faster to compute.
    
- Relative PEs consider distances between sequence elements and can be shared across sequences, which helps the model understand and interpret the relationships and distances between different tokens within a sequence. Relative PEs result in an increase in performance but are computationally more complex.
    

RoPE combines absolute and relative PEs, representing a significant advancement in the design of transformer models. These models process longer sequences of text more naturally and accurately while maintaining efficiency.

Specifically, RoPE integrates a rotation matrix, , to encode the absolute positions of tokens, incorporating the explicit dependency of relative positions into the self-attention mechanism. To illustrate RoPE’s implementation more concretely, consider a model with dimension , which then can be computed as follows:

$$

R_{\theta, m}^6 =
\begin{pmatrix}
\cos(m\theta_1) & -\sin(m\theta_1) & 0 & 0 & 0 & 0 \\
\sin(m\theta_1) & \cos(m\theta_1) & 0 & 0 & 0 & 0 \\
0 & 0 & \cos(m\theta_2) & -\sin(m\theta_2) & 0 & 0 \\
0 & 0 & \sin(m\theta_2) & \cos(m\theta_2) & 0 & 0 \\
0 & 0 & 0 & 0 & \cos(m\theta_3) & -\sin(m\theta_3) \\
0 & 0 & 0 & 0 & \sin(m\theta_3) & \cos(m\theta_3)
\end{pmatrix}
$$

Higher dimensions are divided into  subspaces, so the dimension number has to be even. Let’s put the math into code to make the theoretical concept more clear:  

```python
def simple_rotary_matrix(d, m, max_len):
    assert d % 2 == 0, "Embedding dimension must be even." #1

    theta = 10000 ** (-2 * torch.arange(d // 2).float() / d) #2
    theta *= m

    cos_theta = torch.cos(theta) #3
    sin_theta = torch.sin(theta)

    R = torch.zeros((d, d)) #4

    R[torch.arange(0, d, 2), torch.arange(0, d, 2)] = cos_theta #5
    R[torch.arange(0, d, 2), torch.arange(1, d, 2)] = -sin_theta
    R[torch.arange(1, d, 2), torch.arange(0, d, 2)] = sin_theta
    R[torch.arange(1, d, 2), torch.arange(1, d, 2)] = cos_theta

    return R
```

1. [To ensure that the dimension  is even (required by the formulation).](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO2-1)
2. [Compute thetas.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO2-2)
3. [Compute sine and cosine values for rotation.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO2-3)
4. [Initialize the rotation matrix.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO2-4)
5. [Compute the rotation matrix.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO2-5)

To use the function, you can simply do the following:

```python
d = 6 #1
max_len = 10 #2
R_matrix = simple_rotary_matrix(d, m=1, max_len=max_len) #3
print(R_matrix)
```

1. [Define the embedding dimension .](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO3-1)
2. [Define the sequence length.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO3-2)
3. [Create the rotation matrix.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO3-3)

This creates the following rotary matrix:

```python
tensor([[ 0.5403, –0.8415,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.8415,  0.5403,  0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.9989, –0.0464,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0464,  0.9989,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0000,  1.0000, –0.0022],
        [ 0.0000,  0.0000,  0.0000,  0.0000,  0.0022,  1.0000]])
```

[Figure 1-2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#RoPE) illustrates the RoPE process.

![[../../assets/Pasted image 20260518091531.png]]
 Figure 1-2. Illustration of rotary positional embedding (RoPE). Image adapted from Jianlin Su et al. (2021).

To apply RoPE in the context of self-attention, define the relationship between the  in position  and key  in position  as:

Here  represents the rotary matrix adapting the relative positions.

RoPE enhances efficiency and accuracy, so it’s used in SOTA models like Qwen3. Even SOTA LLMs have a maximum number of tokens they can process at once. For instance, the Qwen3 models can handle up to 32,768 tokens in a single input.

This limitation becomes a problem in use cases that involve long prompts or extensive document summaries, where LLMs capable of managing more extensive contexts are desirable. However, it would take substantial computational resources to create a new LLM with an expanded context capability from the ground up. This raises an important question: is it possible to increase the context window size of an already pretrained LLM? The good news is: yes! PI and YaRN can extend these pretrained LLMs with minimal fine-tuning. [Figure 1-3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#PI_image) demonstrates the PI technique for a LLaMA model with a 2048 context window.

![[../../assets/Pasted image 20260518091544.png]]

Figure 1-3. How the position interpolation (PI) method works for a LLaMA model with a 2048 context window. The dots stand for the training limit of LLMs; the squares illustrate how models adapt to new positions. The dots and triangles demonstrate how PI scales down from [0, 4096] to [0, 2048] to keep them within the trained range. Image adapted from Shouyuan Chen et al. (2023).

Normally, LLM models use input positions (dots) within their trained range. For length extrapolation, models handle new positions (squares) up to 4096. Position interpolation downscales these indices (dots and triangles) from [0, 4096] to [0, 2048], ensuring that they stay within the pretrained range.

To extend the context window, PI interpolates the position indices within the pre-trained limit, with a small set of fine-tuning applied.

That is, PI extends RoPE’s function  by  as follows:

Here  is a new context window beyond the pretrained one.

Let me take a short step back and explain an important way to evaluate the performance of a model  _perplexity_ (PPL). This is a measure of how “surprised” or “perplexed” a model is about context. That is, perplexity measures how well a probability model predicts a sample, with lower values indicating better predictive accuracy. Let me illustrate this with a concrete coding example:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b")
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b")

wiki_text = tokenizer("Apple Inc. is an American multinational " +
                      "corporation and technology company headquartered " +
                      "in Cupertino, California, in Silicon Valley. ",
                      return_tensors = "pt")

loss = model(input_ids = wiki_text["input_ids"],
             labels = wiki_text["input_ids"]).loss
ppl = torch.exp(loss)
print(ppl)

input_text = tokenizer("A Falcon is a generative transformer "+
                       "model and it can't fly.", return_tensors = "pt")

loss = model(input_ids = input_text["input_ids"],
             labels = input_text["input_ids"]).loss 1
ppl = torch.exp(loss)
print(ppl)
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098167004/files/assets/1.png)]1. [Compute loss.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO4-1)

The `wiki_text`

input yields a score of 5.08, while the

`input_text`

yields 121.19. This significantly higher perplexity score indicates that the model finds this sentence quite surprising or unlikely. This is because the model was most likely just trained on data indicating that a falcon is a bird known for its remarkable flying abilities, not a transformer model.

For evaluating LLM performance with longer context windows, you’ll use _sliding window perplexity_. This metric calculates perplexity over a fixed-size window of tokens, moving across the text, to better handle and evaluate large texts and datasets.

One downside of RoPE is that it expands token positional information into a multidimensional complex vector. It struggles with encoding high-frequency components, because its one-dimensional input limits its ability to distinguish between very similar and proximate tokens.

# Softmax and the Haystack Problem

The attention distributions in transformers are computed using the Softmax function. As the context window grows, Softmax tends to produce flatter distributions. This happens because the denominator (the sum of exponentials across all tokens) increases with context size, while each numerator (the exponential of a token’s score) remains fixed. As a result, the output probabilities shrink, and the model struggles to focus on important tokens.

This is often referred to as the _haystack problem_: relevant signals get diluted among many irrelevant ones. Even with advanced techniques like RoPE, the model’s ability to prioritize key elements across long contexts weakens. To address this, SOTA models like LLaMA 4 apply post-training optimization on long contexts, use inference-time temperature scaling of attention,[5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id356) and introduce architectural changes such as interleaved attention layers without positional embeddings (iRoPE).[6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id359) The usage of these methods increases the supported context to up to 10 million tokens while still performing well on “retrieving the needle in the haystack.”

To address this, practitioners of _neural tangent kernel_ (NTK)[7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id361) theory developed _NTK-aware interpolation_, adjusting the scaling of frequencies differently across dimensions to preserve high-frequency information. One of the applications of NTK theory is identifying and mitigating issues related to training neural networks, such as difficulties in learning high-frequency components or patterns in data with low _intrinsic dimensionality_, as is the case with RoPE. Intrinsic dimensionality refers to the minimum number of parameters needed to accurately describe a dataset without losing significant information, representing the dataset’s inherent complexity.

However, NTK-aware interpolation can stretch some dimensions beyond their bounds, potentially degrading the model’s performance. Additionally, _NTK-by-parts interpolatio_n and _dynamic NTK interpolation_ were introduced as refined strategies, focusing on preserving relative local distances and adapting scale factors dynamically for varying sequence lengths, respectively.

Building upon these NTK techniques, YaRN introduces a temperature  to the attention scores before the attention Softmax, uniformly affecting perplexity across different data samples and token positions. This approach modifies attention weight computation and utilizes a length-scaling technique that adjusts both  and  by a constant factor, enhancing the attention mechanism without altering its underlying code. RoPE embeddings, pregenerated and reused, facilitate this process with no additional computational cost during inference or training. When combined with _NTK-by-parts interpolation_, YaRN performs effectively in models like LLaMA and LLaMA 2 (see [Figure 1-4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#YaRN)).

![[../../assets/Pasted image 20260518091635.png]]

Figure 1-4. How the context window can affect the perplexity. Image adapted from Bowen Peng et al. (2023).

As you’ve seen, the lower the perplexity score, the better the model performs. For instance, LLaMA 7b with YaRN and 128k extrapolation performs well in comparison to LLaMA 7b without YaRN.

I’m sure you would now love to know how you can actually apply techniques like RoPE or YaRN to enhance the context length, to ensure optimal performance on lengthy texts. The great news is that most frameworks allow for easy activation of longer context windows; for instance, vLLM supports YaRN, which can be configured as:

`vllm serve Qwen3/Qwen3-8B --rope-scaling _{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}_ --max-model-len 131072`

Next, let’s move to different attention variations and how they improve the performance.

## Attention Mechanism Variations

Today’s transformers are more efficient than previous models, like LSTMs. That is, the first transformer model achieved a high Bilingual Evaluation Understudy (BLEU) score similar to LSTMs, which needed to be trained for months, after only 3.5 days of training. However, transformers can still be considered memory-hungry, since the time and memory complexity of self-attention grows quadratically with the sequence length. This section explores various improvements on the attention mechanisms used in high-performing SOTA LLMs, including:

- Cross-attention[8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id373)
    
- Multi-query attention (MQA)[9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id374)
    
- Grouped-query attention (GQA)[10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id375)
    
- FlashAttention[11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id376)
    
- FlashAttention-2[12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id377)
    
- FlashAttention-3[13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id378)
    

It’s common for models to combine different attention variations: for instance, Falcon uses multi-query attention and FlashAttention.

### Cross-attention

In _cross-attention_, the inputs from two sequences are combined. Usually this means that the queries come from the decoder and the keys and the values come from the encoder. So, in essence, cross-attention enables the interaction between a set of embeddings. This is important for applications where you want to attend to a source sequence while generating a target sequence, such as translation or question-answering tasks. Let me explain the concept further with code:

```
def
```

In this code, you can see that the input for  comes from  and for  and  from , demonstrating the information flow between sequences. Using multiple information sources, the LLM gets a more sophisticated understanding and better generation results.

### Multi-query attention

_Multi-query attention_ (MQA) uses only a single key-value head, whereas multi-head attention (MHA) uses  number of heads for query, key, and value heads, respectively. Thus, MQA significantly speeds up the decoder’s inference time. [Figure 1-5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#multihead_vs_multiquery) compares the two.

![[../../assets/Pasted image 20260518091657.png]]

Figure 1-5. Comparison of multi-head attention (left) and multi-query attention (right). Where multi-head attention has _h_ number of query, key, and value heads, multi-query shares a single key and value head across all query heads.

To make this difference more tangible, read the following code that computes MHA. Note that there is a letter  for each , , and  to represent the head’s dimension:

```python
def MultiheadAttention(x, M, W_query, W_key, W_value, P_o):

    scaling_factor = W_key.shape[1]**0.5

    #1
    Q = torch.einsum('d,hdk->hk', x, W_query)
    K = torch.einsum('md,hdk->hmk', M, W_key)
    V = torch.einsum('md,hdv->hmv', M, W_value)

    #2
    attn_scores = torch.einsum('hk,hmk->hm', Q, K) / scaling_factor

    #3
    attn_weights = F.softmax(attn_scores, dim=-1)

    #4
    o = torch.einsum('hm,hmv->hv', attn_weights, V)
    y = torch.einsum('hv,hdv->d', o, P_o)

    return y
```

1. [Weight matrices.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO5-1)
2. [Compute attribution matrices using the scaling factor for scaled dot-product attention.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO5-2)
3. [Softmax applied to attention scores.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO5-3)
4. [Final attention weights (context vectors) computed.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#co_from_first_principles_to___span_class__keep_together__state_of_the_art_transformers__span__CO5-4)

With MQA, the letter  is omitted from the  and  matrices:

```python
def MultiqueryAttention(X, M, mask, W_query, W_key, W_value, P_o):

    scaling_factor = W_key.shape[1]**0.5

    Q = torch.einsum('bnd,hdk->bhnk', X, W_query)
    K = torch.einsum('bmd,dk->bmk', M, W_key)
    V = torch.einsum('bmd,dv->bmv', M, W_value)

    attn_scores = torch.einsum('bhnk,bmk->bhnm', Q, K) / scaling_factor
    attn_weights = F.softmax(attn_scores + mask, dim=-1)

    O = torch.einsum('bhnm,bmv->bhnv', attn_weights, V)
    Y = torch.einsum('bhnv,hdv->bnd', O, P_o)

    return Y
```

These two examples make it clear that MQA is identical to MHA, except that in MQA the different  heads share a single set of keys and values. This modification speeds up computation in the decoder but can lead to loss of quality, though it’s still more performant than MHA. GQA was developed to address this.

### Grouped-query attention

_Grouped-query attention_ (GQA) organizes query heads into  number of groups, with each group sharing one key and one value head. [Figure 1-6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#multihead_vs_groupedQuery) compares MHA (left) and GQA (right).

![[../../assets/Pasted image 20260518091851.png]]

Figure 1-6. Comparison of multi-head attention (left) and grouped-query attention (right). Where multi-head attention has _h_ number of query, key, and value heads grouped-query attention instead shares one key and value head for each group of query heads, interpolating between multi-head and multi-query attention.

Comparing MHA to GQA, you can see that GQA consolidates multiple key and value heads into a single key and value head, effectively reducing the key-value (KV) size.

# KV Caching

_KV caching_ optimizes _inference latency_ by storing the computed key and value tensors for previously generated tokens during autoregressive decoding. That is, instead of recalculating the full attention context at every step, the model appends only the new keys and values, which significantly reduces the computational cost of the attention mechanism. However, although KV caching provides substantial improvements in inference speed, it increases memory usage proportionally with the sequence length and the number of layers. In scenarios where memory is a limiting factor, you may have to reduce the model size or limit the context window, which can lead to a drop in model accuracy. Deploying KV caching in large-scale production systems also introduces complexity in managing the cache lifecycle. This includes implementing strategies for cache eviction, dynamic memory allocation, and evaluating strategies for cache reuse across requests or sessions.

This means significantly lesser data to load into memory during computation, decreasing the required bandwidth and capacity by a factor of . The following code illustrates this setup:

```python
def GroupedQueryAttention(Q, K, V, num_heads, group_size):

    batch_size, seq_len, embed_dim = Q.shape
    scaling_factor = (embed_dim // num_heads) ** 0.5

    Q = rearrange(Q, 'b s (h d) -> (b h) s d', h=num_heads)
    K = rearrange(K, 'b s (h d) -> (b h) s d', h=num_heads)
    V = rearrange(V, 'b s (h d) -> (b h) s d', h=num_heads)

    attn_scores = torch.einsum('bid,bjd->bij', Q, K) / scaling_factor
    attn_weights = F.softmax(attn_scores, dim=-1)
    attn_output = torch.einsum('bij,bjd->bid', attn_weights, V)

    Y = rearrange(attn_output, '(b h) s d -> b s (h d)',
    b=batch_size, h=num_heads)

    return Y
```

GQA is specifically beneficial for larger models as they usually expand the number of heads. That said, employing GQA substantially reduces both memory bandwidth and capacity while maintaining performance as models scale up.

Thus, memory bandwidth overhead from attention has less impact in larger models. This is because the key-value cache size increases linearly with the model dimension, whereas the model’s floating-point operations per second (FLOPs) and parameters increase quadratically with the model dimension.

Even given these improvements, there’s still room to optimize how attention leverages the GPU memory. This is where FlashAttention and FlashAttention-2 come in.

### FlashAttention

_FlashAttention_ uses _tiling_ to rearrange how attention calculations are performed. By doing so, it avoids creating an  ×  attention matrix. Tiling involves transferring chunks of input data from GPU high bandwidth memory (HBM) and GPU on-chip SRAM (speedy cache). FlashAttention iterates over sections of the  and  matrices, transferring them to the “speedy cache.” Within each section, it cycles through portions of the  matrix, moving them to SRAM, then saves the results of the attention process back to the HBM (illustrated in [Figure 1-7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#FlashAttention)).

![[../../assets/Pasted image 20260518091918.png]]

Figure 1-7. FlashAttention uses tiling to eliminate the large _N × N_ attention matrix. It works by cycling through segments of the _K_ and _V_ matrices in its outer loop (indicated with red arrows), loading these segments into the fast on-chip SRAM. For each segment, FlashAttention also processes chunks of the _Q_ matrix (denoted by light gray arrows), loading them into SRAM, then saving the attention output back to HBM. Image adapted from Tri Dao et al.

This enhances computation speed while decreasing memory consumption from quadratic to linear, relative to the sequence length. FlashAttention avoids saving the large intermediate attention matrices in HBM, minimizing memory operations and doubling or even quadrupling processing speed. In addition, FlashAttention enables longer context windows in transformers, resulting in better perplexity scores and therefore higher-quality models.

This is impressive, but there’s still room for improvement. The number of non-matmul FLOPs operations can be further reduced, as you’ll see in the next section.

### FlashAttention-2

I mentioned earlier that it’s difficult to increase context window size in transformers. The core attention layer’s runtime and memory demands grow quadratically with the input sequence length. RoPE, PI, and YaRN help improve efficiency and lower the perplexity, as you saw.

FlashAttention-2 reduces the amount of non-_matmul_ FLOPs while not changing the output. Although these non-matrix multiplication FLOPs amount to only a minor portion of the total FLOPs, they are slower to execute. GPUs have specialized units that make matrix multiplication operations run up to 16 times faster than non-matrix multiplication operations. Therefore, minimizing non-matrix multiplication FLOPs and maximizing the time spent on matrix multiplication FLOPs is crucial for speeding up your computations.

FlashAttention-2 achieves this by optimizing GPU resource utilization. It minimizes shared memory access through parallel computation across different thread blocks and work partitioning among warps within a single thread block. A _warp_ is a group of threads that execute computations. These adjustments contribute to a 2–3× speedup.

This approach involves inverting the _loop hierarchy_, focusing first on row segments in the outer loop and column segments in the inner loop. This reverses the original method presented in the FlashAttention and introduces parallel processing along the sequence length dimension. [Figure 1-8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#FlashAttention2_worker) illustrates this.

![[../../assets/Pasted image 20260518091933.png]]

Figure 1-8. In the forward pass (left), the tasks (thread blocks) are distributed in parallel, with each task handling a segment of rows from the attention matrix. In the backward pass (right), each task is responsible for a segment of columns within the attention matrix. Image adapted from Tri Dao et al. (2022, 2023).

[Figure 1-9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#FlashAttention2_warps) compares the work partitioning between different warps in the forward pass in FlashAttention and FlashAttention-2. Efficiently dividing work among warps can significantly impact the performance of parallel computing tasks, including those in deep learning models like transformers.

![[../../assets/Pasted image 20260518091949.png]]

Figure 1-9. Comparison of work partitioning between different warps in the forward pass in FlashAttention (left) and FlashAttention-2 (right). Image adapted from Tri Dao et al. (2022, 2023).

### FlashAttention-3

_FlashAttention-3_ introduces new programming techniques that take full advantage of the Hopper[14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id397) GPU architecture, specifically the NVIDIA H100, to accelerate attention computation beyond the limits of previous methods. While FlashAttention-2 performs well for most GPUs, on newer architectures such as H100, FlashAttention-2 achieves only 35% GPU utilization.

While FlashAttention and FlashAttention-2 focused on reducing memory bandwidth usage and optimizing compute schedules, FlashAttention-3 advances performance by leveraging hardware asynchrony and low-precision formats such as FP8. One of its key innovations is the use of producer-consumer asynchrony, where separate GPU warps are assigned distinct roles: some act as producers loading data (_Q_, _K_, _V_) via the Tensor Memory Accelerator (TMA), while others act as consumers performing matrix multiplications on Tensor Cores. This strategy, often referred to as _pingpong scheduling_, allows data transfer and computation to run concurrently, effectively hiding latency and maximizing throughput.

# PagedAttention for Higher Throughput

While FlashAttention-3 introduces techniques that fully leverage the Hopper architecture and low-precision formats like FP8, it’s optimized for H100 GPUs only. But these GPUs can be expensive to run on cloud services. Therefore, for most teams and production environments, PagedAttention offers a more accessible and cost-effective solution to increase inference throughput without needing specialized hardware. _PagedAttention_ is a memory-efficient attention variant designed to improve throughput during LLM inference. I’m sure you’ve read my note on KV caching earlier in this chapter, and you might have to evaluate strategies to optimize KV caching. This is exactly what PagedAttention[15](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id402) does. PagedAttention stores the KV cache in non-contiguous memory blocks, similar to virtual memory paging in operating systems. These blocks can be dynamically allocated, shared across sequences, and reused with copy-on-write semantics.

PagedAttention is built into the [vLLM serving system](https://oreil.ly/zcq3y) and achieves up to 4× higher throughput by minimizing KV cache waste and enabling batching of more requests. PagedAttention is especially beneficial for workloads with long sequences, variable decoding lengths, and complex algorithms like beam search or parallel sampling. Note that PagedAttention is only available on vLLM. Moreover, vLLM can struggle if you have a lot of concurrent requests, so your throughput could still be better with [Hugging Face’s Text Generation Inference (TGI)](https://oreil.ly/sSDUf), as it’s very reliable on many concurrent requests. I suggest that you use a [TGI benchmarking tool](https://oreil.ly/GC5so) to validate this for your application.

Another innovation is GEMM-Softmax pipelining. _General matrix-matrix multiplication_ (GEMM) is a fundamental operation in deep learning that multiplies two matrices to produce a third, and is heavily optimized on GPUs using specialized hardware like Tensor Cores. In transformers, the Softmax operation depends on the output of GEMM, introducing a sequential dependency. FlashAttention-3 breaks this bottleneck by pipelining GEMM and Softmax across iterations so that while one block performs Softmax, the next GEMM operation can already begin. This overlapping is essential to exploit Hopper’s asynchronous compute capabilities.

FlashAttention-3 also introduces low-precision attention with FP8, which nearly doubles throughput compared to FP16. To achieve this without sacrificing accuracy, it adapts the memory layout of _Q_, _K_, and _V_ to meet Hopper’s FP8 GEMM constraints and applies two techniques to reduce quantization error: block quantization and incoherent processing. The latter involves multiplying _Q_ and _K_ with a random orthogonal matrix constructed from Hadamard transforms before quantization. _Hadamard transforms_ refer to a mathematical operation that maps a vector into a new space using only additions and subtractions. It relies on the _Hadamard matrix_, which is made up entirely of +1 and −1 entries. This transformation is efficient to compute and helps spread information across dimensions, which is useful for reducing the impact of outliers in low-precision quantization.

# Conclusion

This chapter has taken you from the foundational ideas of the original transformer to some of the most powerful architectural and inference-time innovations that define today’s SOTA models. From tokenization and multi-head attention to rotary embeddings, longer context windows, and advanced memory optimizations like PagedAttention and FlashAttention, you’ve seen how the architecture has evolved over time to meet the ever-growing demands of real-world applications.

This progression is a testament to the fact that the transformer is no longer a static blueprint confined to language tasks. It’s a dynamic and extensible framework that continues to improve in both accuracy and efficiency. In the next chapters, we’ll move beyond language and explore how these models, along with the architectural advances introduced here, enable breakthroughs in domains such as vision, time series, reinforcement learning, and structured reasoning. You’ll learn how to apply these tools in practice and how to make architectural choices based on the specific demands of each problem space.

[1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id294-marker) Ashish Vaswani et al. [“Attention Is All You Need”](https://arxiv.org/abs/1706.03762) (2017).

[2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id340-marker) Jianlin Su et al. [“RoFormer: Enhanced Transformer with Rotary Position Embedding”](https://arxiv.org/abs/2104.09864) (2021).

[3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id343-marker) Shouyuan Chen et al. [“Extending Context Window of Large Language Models via Positional Interpolation”](https://arxiv.org/abs/2306.15595) (2023).

[4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id345-marker) Bowen Peng et al. [“YaRN: Efficient Context Window Extension of Large Language Models”](https://arxiv.org/abs/2309.00071) (2023).

[5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id356-marker) Ken M. Nakanishi. [“Scalable-Softmax Is Superior for Attention”](https://arxiv.org/abs/2501.19399) (2025).

[6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id359-marker) Amirhossein Kazemnejad et al. [“The Impact of Positional Encoding on Length Generalization in Transformers"](https://arxiv.org/abs/2305.19466) (2023).

[7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id361-marker) Arthur Jacot et al. [“Neural Tangent Kernel: Convergence and Generalization in Neural Networks”](https://arxiv.org/abs/1806.07572) (2018).

[8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id373-marker) Mozhdeh Gheini et al. [“Cross-Attention Is All You Need: Adapting Pretrained Transformers for Machine Translation”](https://arxiv.org/abs/2104.08771) (2021).

[9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id374-marker) Noam Shazeer. [“Fast Transformer Decoding: One Write-Head Is All You Need”](https://arxiv.org/abs/1911.02150) (2019).

[10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id375-marker) Joshua Ainslie et al. [“GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"](https://arxiv.org/abs/2305.13245) (2023).

[11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id376-marker) Tri Dao et al. [“FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness”](https://arxiv.org/abs/2205.14135) (2022).

[12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id377-marker) Tri Dao. [“FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning”](https://tridao.me/publications/flash2/flash2.pdf) (2023).

[13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id378-marker) Jay Shah et al. [“FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-Precision”](https://arxiv.org/abs/2407.08608) (2024).

[14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id397-marker) The architecture is named after Grace Hopper, a pioneer in computer programming who famously popularized the term _bug_ in 1947. She was known for carrying a piece of wire to illustrate how far light travels in a nanosecond, which she used as a playful response when asked to make things faster. Now she gets her revenge, as we name GPUs after her that can perform nearly two quadrillion operations per second.

[15](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#id402-marker) Woosuk Kwon et al. [“Efficient Memory Management for Large Language Model Serving with PagedAttention"](https://arxiv.org/pdf/2309.06180) (2023).
Transformers have gained popularity for time series modeling due to their ability to capture long-sequence interactions more effectively than recurrent neural network (`RNN`) models. The self-attention mechanism in transformers reduces the maximum length of network signal travel paths to the theoretical minimum of `O(1)` by allowing each element in the sequence to directly attend to every other element. This eliminates the need for recurrent structures and allows for more efficient information flow. As a result, transformers show great potential for long sequence time-series forecasting (`LSTF`) and other domains such as anomaly detection and spatiotemporal time series prediction.

Many real-world applications, such as weather forecasting, traffic prediction, industrial process controls, and electricity consumption planning, require the prediction of long sequence time series. LSTF demands a model with high prediction capacity, capable of efficiently capturing precise long-range dependencies between input and output.

In addition, probabilistic time series forecasting is an important task in many practical applications, from finance and weather forecasting to managing computer system performance. Accurate probabilistic forecasts are essential for making informed decisions in these areas. _Probabilistic time series forecasting_ includes a range of probabilities for all possible future outcomes, rather than identifying a single specific outcome as “the forecast.”

During your exploration of this chapter, you’ll learn key considerations for using time series data. You’ll also acquire a basic understanding of different domains for time series, such as time series forecasting, anomaly detection, and spatiotemporal time series prediction. As the last steps in your journey through this time series chapter, you’ll examine different transformer architectures for these domains, including Chronos, PatchTST, and AnomalyBERT, and learn how you can fine-tune the first two models for your own data.

# Understanding the Intricacies of Time Series Data

When working with time series data, it’s fundamental to consider certain key properties that can significantly impact your analysis and forecasting. This section offers a brief overview of the most common properties you should examine when handling time series data.

## Autocorrelation and Partial Autocorrelation

_Autocorrelation_ is the internal correlation between observations in a time series, often represented as a function of the time interval between observations. The mathematical definition of the autocorrelation at lag $k$, $y(k)$ is as follows:

$$
\gamma(k) = \frac{E\big[(X_t - \mu)(X_{t+k} - \mu)\big]}{E\big[(X_t - \mu)^2\big]}
$$

Here,  represents the series’ values, while  represents the series’ mean. The expected value is denoted by the symbol . The sample statistic for this sample can be computed by the following equation:

$$
\hat{\gamma}(k) = \frac{\sum_{i=1}^{n-k} \big(x_i - \bar{x}\big)\big(x_{i+k} - \bar{x}\big)}{\sum_{i=1}^{n} \big(x_i - \bar{x}\big)^2}
$$

 is the mean of the observed values, , of the time series.

The _partial autocorrelation function_ for  lags is defined as the autocorrelation between  and , and the effect of other variables is shifted by  lags . The autocorrelation function and partial autocorrelation function are often referred to as a correlogram. [Figure 2-1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#correlogramm) shows a _correlogram_ for _the Amazon stock price_.

![[../../assets/Pasted image 20260518092333.png]]

###### Figure 2-1. Correlogram of Amazon stock.

The horizontal axis of the autocorrelation plot (left plot) shows the size of the lag between the elements of the time series. For instance, the autocorrelation with lag 2 is the correlation between the time series and the corresponding elements that were observed two time periods earlier. Examining the autocorrelation plot reveals a high autocorrelation between the actual and the prior timestep of the series, with no decline. Additionally, the partial autocorrelation (right plot) is significant for the first lag. The gray areas are the _confidence bands_, indicating whether the correlations are statistically significant.

## Cointegration

_Cointegration_ refers to a real relationship between two time series. A commonly used example is a drunk pedestrian and their dog. Their individually measured walks might appear random if taken alone, but they never stray too far from each other.

In the case of cointegration, you expect to observe high correlations. The difficulty lies in assessing whether two processes are indeed cointegrated or if you’re looking at a _spurious correlation_. A fun example of a spurious correlation is shown in [Figure 2-2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#spurious_correlation).

The important difference between the two states is that in the case of a spurious correlation, there may not be any relationship between the processes, whereas cointegrated time series are strongly related to one another. You might remember from your statistics class the expression “Correlation is no proof of causation!”

![[../../assets/Pasted image 20260518092346.png]]
Figure 2-2. Example of spurious correlation. The figure is from [Tyler Vigen’s website](https://tylervigen.com/) about spurious correlations. You can find more funny spurious correlations on his site.

## Cross-Correlation

When working with multivariate time series, it’s essential to understand the (inter)dependency between the series. _Cross-correlation_ (also called _cross covariances_) is a measure of the degree of linear dependency between two time series processes. The cross-correlation between two processes  and  is shown in the following equation:

$$
\gamma_{12}(k) = \operatorname{Cov}(X_{1,t+k}, X_{2,t})\gamma_{21}(k) = \operatorname{Cov}(X_{2,t+k}, X_{1,t})
$$

However, high cross-correlation between features can cause issues in predictive modeling, such as multicollinearity, which can distort the model’s estimates and reduce interpretability. _Multicollinearity_ is a statistical phenomenon where multiple independent variables in a model exhibit correlation with one another. It may be beneficial to either remove one of the cross-correlated features or create new features that combine the information from the correlated ones.

## Stationarity

The statistical features of a stationary time series, such as mean, variance, and autocorrelation, are _period-independent_; that is, they don’t change over time. Thus, _stationarity_ implies that a time series is lacking trends or seasonal influences and that descriptive statistics such as the mean or standard deviation are constant or exhibit little variation over time when computed for different rolling windows. Strict stationarity implies that the joint distribution of any subset of time series observations is independent of time in all moments.

## Trend and Seasonality

Industrial time series, such as the time series of stock prices, are expected to exhibit trends or seasonality. To explore these properties, you can use _decomposition_, which involves considering a series in terms of its level, trend, seasonality, and noise components. Decomposition can provide valuable insights for understanding time series analysis and forecasting difficulties. The [Statsmodels package](https://oreil.ly/KZ5pp) offers functions to automatically decompose a given time series. [Figure 2-3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#seasonal_decompostion) shows an example of such a decomposition for Amazon stock pricing data, clearly indicating a continuous upward trend and a seasonal component.

![[../../assets/Pasted image 20260518102110.png]]

Figure 2-3. Seasonal decomposition of Amazon stock.

Typically, you begin by conducting an _exploratory data analysis_ (EDA) to thoroughly examine your data before moving on to time series prediction. This initial step helps identify patterns, trends, and potential anomalies in the data, providing a solid foundation for accurate forecasting. By understanding the underlying structure of your data, you can make more informed decisions on the next steps, such as removing irrelevant features or addressing data quality issues.

## Preparing a Dataset

Data preparation is always a necessary step before using your data for modeling. When working with time series data, it’s essential to consider their sequential nature; you can’t just randomly shuffle your data. You also need to be careful about how you split and scale your data. Standardizing your data is crucial to avoid potential scaling difficulties when fitting your model. If you have more than one feature (covariate), scaling ensures that one feature doesn’t dominate another due to different scales.

To avoid introducing look-ahead bias into your prediction, the training data must be scaled without knowledge of the test set. _Look-ahead bias_ occurs when future information is used to predict past data, leading to overly optimistic and unrealistic model performance. To avoid this, you should standardize the training set using its own mean and standard deviation, not those of the whole dataset. For the validation and test sets, you should apply the same normalization: use the mean and standard deviation of the training set. This approach helps avoid systematic bias. _Systematic bias_ happens when the model consistently overestimates or underestimates due to improper handling of the data during preparation.

Additionally, depending on your data, you might consider performing log transformations to reduce data variability and bring the data closer to a normal distribution. By preparing your dataset in these ways, you can improve the performance and reliability of your time series models.

# Time Series Modeling in Various Application Domains

Time series modeling is an important application area for machine learning. It underpins many aspects of modern operations across various domains, including inventory control, customer management, production, distribution, finance, and marketing. Improvements in these areas can have significant financial impacts, often amounting to millions of dollars for each point of forecasting accuracy gained. Tasks may include anomaly detection, probabilistic time series modeling, spatiotemporal time series prediction, and classification. In this section, I’ll briefly cover the main differences between these tasks and give some examples of their applications:

Time series forecasting

_Time series forecasting_ involves predicting future values based on previously observed data in a time series. This can be applied to both short-term and long-term predictions, each with its own set of challenges and methodologies. _Short-term forecasting_ focuses on immediate future values, so it’s often used for tasks such as inventory management and demand planning. _Long-term forecasting_, on the other hand, aims to predict trends and seasonal patterns over extended periods, which is vital for financial markets, electricity demands, and weather prediction.

Spatiotemporal forecasting

In _spatiotemporal forecasting_, both temporal and spatial dependencies are considered for accurate predictions. _Temporal_ refers to time, while _spatiotemporal_, or _spatial-temporal_, is used when data is collected across both space and time. This approach is essential for describing phenomena at specific locations and times. Examples of spatiotemporal forecasting applications include traffic flow forecasting, wind speed forecasting, weather and climate forecasting, and air quality forecasting.

Event forecasting

_Event forecasting_ aims to predict the timing and characteristics (marks) of future events based on the history of past events, often modeled by _temporal point processes_ (TPP). In TPP, the goal is to predict the times and marks of future events given the sequence of past occurrences. Recommender systems are a recent application area for TPPs, leveraging the temporal dimension of user behavior to provide time-sensitive recommendations, such as optimal timing for promotions. Other applications include clinical event prediction, which involves forecasting sequences of patient interactions with the healthcare system, human activity prediction for assisted living, and demand forecasting.

Anomaly detection

_Anomaly detection_ involves identifying abnormalities in time series data and is a key task in time series analysis. It’s used to detect defects in machines and prevent potential harm, making it essential for many industrial environments, such as monitoring machines, IT devices, spacecrafts, and engines. However, this task is challenging because most datasets don’t provide ground truth labels for the training set. That is, it’s unknown whether any given point is anomalous or not in the training data. As a result, anomaly detection is typically approached as an unsupervised learning task.

Time series classification

_Time series classification_ involves analyzing multiple labeled classes of time series data to determine the class to which a new dataset belongs. This is important in many environments, such as analyzing sensor data or financial data to support business decisions. For instance, in healthcare, time series classification can be used to diagnose medical conditions based on patient data over time. In finance, it can classify stock price movements, where labels like 0 and 1 indicate down and up movements, respectively, to inform trading strategies.

# Tokenizing Time Series Data

Time series forecasting aims to understand the relationships between data points across different timesteps. Unlike words in a sentence, individual timesteps lack inherent semantic meaning, making it important to extract local semantic information to analyze their connections effectively. Some transformer models treat each timestep as a separate token, processing them point by point. This method makes it difficult for the model to learn temporal dependencies when considering only one timestep at a time.

One way to address this is patching. _Patching_ involves grouping multiple time points together before tokenizing and embedding them. This process creates subseries-level patches that serve as input tokens to the transformer. [Figure 2-4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#Patching) illustrates this process.

![[../../assets/Pasted image 20260518102131.png]]

Figure 2-4. Example of time series patching.

Using patches significantly extends the historical time range of the input while maintaining the same token length. This method is similar to the approach used in vision transformers, which you’ll learn about in the next section, but adapted for time series data. Patching offers three key benefits: it preserves local semantic information within the embedding, significantly reduces the computation and memory usage of the attention given the same lookback window, and allows the model to consider a longer historical context. PatchTST[1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id454) introduced this method and significantly improved long-term forecasting accuracy.

The tokenization scheme of Lag-Llama[2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id456) constructs lagged features from prior values of the time series, using specified lag indices (quarterly, monthly, weekly, daily, hourly, and second-level frequencies). Given a sorted set of positive lag indices $\mathcal{L}[j]$, where $\mathcal{L}[j]$  refers to the list of lag indices $L$,  is the last lag index in the sorted list $\mathcal{L}[j]$. The lag operation on a particular time value $x_t$ is defined as $x_t -> k_t$, where each entry  of  is given by

$$
\mathbf{k}_t[j] = x_{t - \mathcal{L}[j]}
$$

To create lag features for a context-length window , a larger window with  more historical points is sampled. [Figure 2-5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#lagLlamaLags) illustrates this tokenization scheme.

![[../../assets/Pasted image 20260518102537.png]]

Figure 2-5. For a time series, tokenization at timestep _t_ of the value includes lag features based on an example set of lag indices _L_, where each value in the vector is from the past of _xt_, and _F_ possible temporal covariates are constructed from timestamp _t_. Image adopted from Kashif Rasul et al. (2024).

In addition to these lagged features, date-time features of various frequencies (second-of-minute, hour-of-day, etc., up to quarter-of-year) from the time index  are added. While these date-time features provide additional information, for any time series, all except one date-time feature remain constant from one timestep to the next, allowing the model to implicitly understand the frequency of the time series. With a total of  $F$ date-time features, each token is then of size $\abs{\mathcal{L}} + f$.

In 2024, LLMTime[3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id458) introduced a new tokenization method that converts real-valued data into strings of digits after fixing numerical precision and scaling the data.

As you know, tokenization is needed as it impacts the formation of patterns within tokenized sequences and the operations that language models can learn. However, common methods like byte-pair encoding (BPE) can tokenize numbers in a way that complicates arithmetic; for instance, the number

```text
42235630
```

might be tokenized as

```python
[422, 35, 630]
```

causing different tokenizations with minor changes.

Newer LLMs like LLaMA tokenize numbers into individual digits by default. To improve tokenization in GPT models, digits in LLMTime are separated with spaces, and commas are used to separate each timestep. Decimal points are dropped for fixed precision. For example:

```python
0.123, 1.23, 12.3, 123.0
```

becomes

```python
"1 2, 1 2 3, 1 2 3 0, 1 2 3 0 0".
```

This encoding prevents unusual tokens in GPT models. However, in LLaMA models, added spaces can be counterproductive, since each digit and space already has its token. Adding spaces can increase sequence length unnecessarily and potentially make the sequence out-of-distribution. [Figure 2-6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#LLMTime) compares the tokenization of GPT-based and LLaMA models.

![[../../assets/Pasted image 20260518102710.png]]

Figure 2-6. GPT-3 and LLaMA-2 tokenizations and their effects on the respective forecasting performance. Adding spaces helps GPT-3 by creating one token per digit, enhancing performance. In contrast, LLaMA-2 tokenizes digits individually, so adding spaces reduces its performance. Image adopted from Nate Gruver et al. (2024).

Chronos[4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id460) tokenizes time series values by scaling and quantizing them into a fixed vocabulary, then trains existing transformer-based language models on these tokenized series using _Cross-Entropy Loss_. [Figure 2-7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#Chronos) shows this process.

_Cross-Entropy Loss_ quantifies the difference between the predicted probability distribution (also called _input logits_) and the true distribution of the target variables.

![[../../assets/Pasted image 20260518102719.png]]

Figure 2-7. To generate a sequence of tokens, the input time series is scaled and quantized. Image adapted from Abdul Fatir Ansari et al. (2024).

Chronos is a framework that adapts existing language model architectures and training procedures to probabilistic time series forecasting. This requires specific tokenization modifications to adapt language models for time series data because while both language and time series are sequential, they differ in representation; natural language uses a finite vocabulary, while time series are continuous. To make this more concrete, consider a time series:

$$
x_{1:C+H} = \lvert x_1, \ldots, x_{C+H} \rvert
$$

Here the initial  steps provide the historical context, and the next  steps represent the forecast horizon. Since language models use a finite vocabulary, adapting them for time series data involves converting observations  into a finite set of tokens. Chronos achieves this by first scaling the observations and then quantizing them into a fixed number of bins.

Now that you know about the complexity of tokenizing time series data and how some time series transformers handle this challenge, let’s move on to the next sections and see how different transformers integrate this into their overall architecture.

# Chronos: Learning the Language of Time Series

Traditionally, forecasting has been dominated by statistical models such as _autoregressive integrated moving average_ (ARIMA) models. However, the zero-shot learning capabilities of LLMs have sparked interest in creating foundation models for time series. Chronos trains standard language models on time series without altering the model architecture. Tokens, as described in the previous section, are input into a language model, which can be either an encoder-decoder or a decoder-only model.

Training is done using Cross-Entropy Loss. The following equations show the loss function for a single tokenized time series including the EOS tokens:

$$
\ell(\theta) = - \sum_{h=1}^{H+1} \sum_{i=1}^{|\mathcal{Y}_h|} 
\mathbf{1}\!\big(z_{C+h+1}=i\big) \, 
\log p_\theta \!\left(z_{C+h+1}=i \mid z_{1:C+h}\right)
$$

Here,  is the categorical distribution predicted by the model parameterized by .  is the Cross-Entropy Loss function parameterized by . The outer summation runs over the prediction horizon and the inner summation over the vocabulary of time series tokens . This loss is then averaged over a batch of time series during training.

During inference, the model autoregressively generates tokens and maps them back (dequantizes) to numerical values, sampled from the predicted distribution:

$$
p_{\theta}\!\left(z_{C+h+1} \mid z_{1:C+h}\right), \quad h \in \{1,2,\ldots,H\}
$$

Multiple trajectories are sampled to derive a predictive distribution. This process is illustrated in [Figure 2-8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ChronosTrainInf).

![[../../assets/Pasted image 20260518103022.png]]

Figure 2-8. On the left is the training process of Chronos, while on the right is the inference of Chronos producing a probabilistic forecast. Image adapted from Abdul Fatir Ansari et al.

Chronos is trained on 13 datasets from various application domains, including nature, energy, transport, and the web, with sampling frequencies ranging from five minutes to monthly. Chronos is based on T5,[5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id467) a text-to-text encoder-decoder transformer. Chronos can perform zero-shot time series prediction. An example performance is shown in [Figure 2-9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#chronosAir).

![[../../assets/Pasted image 20260518103030.png]]

Figure 2-9. Historical data and zero-shot forecast for air passengers time series. Data is from the book [_Practical Time Series Analysis_](https://www.oreilly.com/library/view/practical-time-series/9781492041641/) (O’Reilly).

Depending on your data, you’ll want to fine-tune the model on your own dataset, which you’ll be doing in the next section.

## Fine-Tuning Chronos

For fun, I’ll be using the historical stock price data of Amazon, since this model was developed by Amazon. While the code for fine-tuning and training Chronos is available, I recommend using my [modified version](https://oreil.ly/sIp60), which addresses some errors and includes a _requirements.txt_ file. I won’t show you how to download the stock pricing data here, but you can find all code in the accompanying notebook.

If you want to use Chronos with your time series, you have to convert the data into the Arrow format. [Example 2-1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ChronosDataPrep) shows a Python function to do this conversion.

##### Example 2-1. Function to convert a DataFrame into Arrow format for Chronos

```python
def convert_to_arrow(
    path: Union[str, Path],
    time_series: Union[List[np.ndarray], np.ndarray],
    start_times: Optional[Union[List[np.datetime64], np.ndarray]] = None,
    compression: str = "lz4",
):
    assert len(time_series) == len(start_times)

    dataset = [
        {"start": start, "target": ts} for ts, start in zip(time_series, start_times)
    ]
    ArrowWriter(compression=compression).write_to_file(
        dataset,
        path=path,
    )
```

Now you can use the function to convert the time series data, as shown in [Example 2-2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ChronosConvertData).

##### Example 2-2. Convert the time series data to Arrow format

```python
convert_to_arrow("./amazon_train_data.arrow",
        time_series=train_time_series_list, start_times=train_start_times)
convert_to_arrow("./amazon_test_data.arrow",
        time_series=test_time_series_list, start_times=test_start_times)
```

After converting your data, you can set up your training configurations. The `yaml` file to specify your configuration is located in the [configs folder](https://oreil.ly/Jrw8Z) of the repo in GitHub. Here you can define the training parameters, such as:

```python
context_length
```

Others might include the path to your training data. Alternatively, you can also alter the parameters when you pass your commands into your terminal, as you see in [Example 2-3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ChronosCommandLine).

##### Example 2-3. Command line arguments for fine-tuning Chronos

```python
CUDA_VISIBLE_DEVICES=0 python /chronos-forecasting/scripts/training/train.py
--config /chronos-forecasting/scripts/training/configs/chronos-t5-base.yaml \
--model-id amazon/chronos-t5-base \
--no-random-init \
--max-steps 44600 \
--learning-rate 0.001
```

This command will use one GPU and will train the T5 base model. The training will take around 1 hour in Google Colab and save the model in a folder called

output

which you can also modify in your `yaml` file.

If you train the model on your own data, you might want to push your model to Hugging Face, so you can use it later for your predictions. [Example 2-4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#PushModelToHub) shows you how you can do this.

##### Example 2-4. Push fine-tuned model to Hugging Face hub

```python
os.environ["HF_TOKEN"] = "your_token" 1

pipeline = ChronosPipeline.from_pretrained(
"/content/output/run-3/checkpoint-final")2
pipeline.model.model.push_to_hub("your-model-name"
, use_auth_token=os.getenv("HF_TOKEN")) 3
```

1. [Set your Hugging Face token.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO1-1)
2. [Add your path to your Chronos model.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO1-2)
3. [Add your model name.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO1-3)

Now, you can just load your model from Hugging Face, as shown in [Example 2-5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ChronosPipe), and use it for the forecast.

##### Example 2-5. Chronos pipeline

```python
pipeline = ChronosPipeline.from_pretrained(
    "your-model-name",
    use_auth_token=os.getenv("HF_TOKEN"),
    device_map="cuda",
    torch_dtype=torch.bfloat16,
)
```

If you just want to test the model on the stock price dataset, you can simply use my fine-tuned version of Chronos. To access the model, use the model path _nicolepcx/chronos-t5-base-fine-tuned-AMZN-EOD_.

The model is fine-tuned with a context length of 21 days and has a prediction horizon of 5 days. The result of the forecast is in the circle in [Figure 2-10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ChronosStock).

Overall, the result is not bad for an LLM-based time series prediction.

![[../../assets/Pasted image 20260518103250.png]]

Figure 2-10. Plot of the results for the 5-day stock-price prediction.

# PatchTST: A Time Series Is Worth 64 Words

PatchTST[6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id471) introduced not only patching but also _channel independence_. This means that for multivariate time series, each channel consists of a single univariate time series that uses the same embedding and transformer weights across the series. A _multivariate time series_ is a multi-channel signal where each transformer input token can represent data from either a single channel or multiple channels.

A previous method for multivariate time series was _channel mixing_, which refers to cases where the input token consists of the vector of all time series features and projects it to the embedding space to mix information. With _channel independence_, each input token contains information from only a single channel. Mathematically, you can represent this as follows:

$$
x \in \mathbb{R}^{M \times L}
$$

Here,  is the lookback window , where each  at timestep  is a vector of dimension . Next, you can represent the th univariate series as follows:

$$
x^{(i)} \in \mathbb{R}^{1 \times L}
$$

Here, the series starts with length  at time index 1, which results in $x^{(i)}_{1:L} = \left( x^{(i)}_1, \ldots, x^{(i)}_L \right), \quad i = 1, \ldots, M$, where $i = 1,...,M$ . This means you split the input, , into  univariate series and feed it separately into the transformer. The transformer then provides prediction results in the following form:

$$
\hat{x}^{(i)} = \left( \hat{x}^{(i)}_{L+1}, \ldots, \hat{x}^{(i)}_{L+T} \right) \in \mathbb{R}^{1 \times T}
$$

This process is illustrated in [Figure 2-11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#PatchTST_series).

![[../../assets/Pasted image 20260518103333.png]]

Figure 2-11. Overview of channel independence in PatchTST. Image adapted from Yuqi Nie et al. (2023).

PatchTST uses a transformer encoder to map the observed signals to latent representations. The patches are mapped to the transformer latent space of dimension  via a trainable linear projection and a learnable additive positional encoding, to keep the temporal order of the patches. Each multi-head attention head then transforms these inputs into query, key, and value matrices. The multi-head attention block uses BatchNorm and a feed-forward network with residual connections. The overall architecture is illustrated in [Figure 2-12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#TransformerBackbone).

In the next section, you’ll try out PatchTST with your own data to see how this works.

![[../../assets/Pasted image 20260518103558.png]]

Figure 2-12. Architecture overview of PatchTST. Image adapted from Yuqi Nie et al. (2023).

## Fine-Tuning PatchTST on Historical IBM Stock Prices

Again, I thought it would be fun to predict IBM stock prices using PatchTST, since the model was primarily developed by IBM. I’ll omit downloading the dataset and preparing the dataset here, but it can all be found in the accompanied notebook for this section. I used the following setup for my model parameter initialization, Optuna hyperparameter setup, and trainer construction.

##### Example 2-6. PatchTST setup

```python
context_length = 32
forecast_horizon = 10
patch_length = 8
num_workers = 16
batch_size = 128
```

As a next step, to do the hyperparameter search, you need to set up your study object and specify the direction of the optimization with [Optuna](https://optuna.org/). Optuna is a framework for hyperparameter optimization.

##### Example 2-7. Optuna hyperparameter trial setup

```python
def optuna_hp_space(trial: optuna.Trial):
    return {
        "learning_rate": trial.suggest_loguniform(
        "learning_rate", 1e-8, 1e-2),
        "per_device_train_batch_size": trial.suggest_categorical(
        "per_device_train_batch_size", [16, 32, 64, 128]),
        "num_train_epochs": trial.suggest_int(
        "num_train_epochs", 50, 300, step=20),
        "dataloader_num_workers": trial.suggest_int(
        "dataloader_num_workers", 0, 16, step=4),
        "weight_decay": trial.suggest_float(
        "weight_decay", 0.0, 0.3, step=0.05),
        "per_device_eval_batch_size": trial.suggest_categorical(
        "per_device_eval_batch_size", [16, 32, 64, 128]),
    }
```

Now you need to initialize the trial.

##### Example 2-8. Initialize model for trial

```python
def model_init(trial):
    return PatchTSTForPrediction(config)
```

As the next step, you can initialize your training arguments, as you’re used to with the Hugging Face trainer class.

##### Example 2-9. Initialize training arguments and trainer class

```python
training_args = TrainingArguments(
    output_dir="./checkpoint/output_dir",
    overwrite_output_dir=True,
    do_eval=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    save_total_limit=3,
    logging_dir="./checkpoint/logging_dir",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    num_train_epochs=200,
    label_names=["future_values"],
)

trainer = Trainer(
    model=None,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    model_init=model_init,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=30,
    early_stopping_threshold=0.00001)]
)
```

As the final step, to start your trial with Optuna, you have to start the trial run, as shown in [Example 2-10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#StartTrial).

##### Example 2-10. Start the hyperparameter search

```python
best_run = trainer.hyperparameter_search(
    backend="optuna",
    n_trials=30,
    direction="minimize",
)
```

After your hyperparameter search is done, you can access the found hyperparameter and fine-tune your PatchTST on your data by defining the training arguments from your best run. [Example 2-11](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#UseHyper) shows how you can do this.

##### Example 2-11. Use hyperparameter for fine-tuning

```python
best_hyperparameters = best_run.hyperparameters

training_args = TrainingArguments(
    output_dir="./checkpoint/output_dir",
    overwrite_output_dir=True,
    learning_rate=best_hyperparameters['learning_rate'],
    per_device_train_batch_size=int(
    best_hyperparameters['per_device_train_batch_size']),
    do_eval=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    save_total_limit=3,
    logging_dir="./checkpoint/logging_dir",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    num_train_epochs=200,
    label_names=["future_values"],
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=30,
    early_stopping_threshold=0.00001)]
)

trainer.train()
```

Now you can evaluate your model and print out your results, as detailed in [Example 2-12](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#PrintResultsPatchTST).

##### Example 2-12. Evaluate and print results

```python
results_valid_dataset = trainer.evaluate(valid_dataset)
print("Valid Results:", results_valid_dataset)
results_test_dataset = trainer.evaluate(test_dataset)
print("Test Results:", results_test_dataset)
```

I get the results as shown in [Example 2-13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ResultsPatchTST).

##### Example 2-13. Validation results

```python
Valid Results: {'eval_loss': 0.01785971038043499, 'eval_runtime': 1.0838,
'eval_samples_per_second': 1384.057, 'eval_steps_per_second': 173.468,
'epoch': 34.0}
Test Results: {'eval_loss': 0.04794887453317642, 'eval_runtime': 2.8294,
'eval_samples_per_second': 1086.082, 'eval_steps_per_second': 136.069,
'epoch': 34.0}
```

The results are measured in mean squared error (MSE), and achieving a test set MSE of 0.0479 for a 10-day forecast horizon for a stock can be considered a good result.

# TimesFM: A Decoder-Only Time Series Foundation Model

I’m sure you’ve heard of the scaling law.[7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id479) The _scaling law_ states that model performance improves in a predictable power-law fashion as you increase the amount of data, the number of parameters, and the compute used. Meaning, the sheer volume of data helps the model to generate accurate predictions without using any additional data from the target time series.

This very fact motivated the researchers behind TimesFM[8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id481) to ask themselves a key question: “Can large pretrained models trained on massive amounts of time series data learn temporal patterns that can be useful for time series forecasting on previously unseen datasets?”

Let me just spill the beans here, without making you read through the whole section: the answer is yes! TimesFM demonstrates strong zero-shot capabilities. In some cases, only minimal fine-tuning is required to achieve results comparable to SOTA time series models. This is what you’ll be doing in this section, fine-tuning TimesFM on an [hourly energy consumption dataset](https://oreil.ly/N0Psk). But first, let me explain the architecture in more detail.

The researchers introduce two pivotal ideas. First, they propose a large-scale, heterogeneous time series corpus that includes both real-world data sources, such as Google Trends and Wikipedia page views, and synthetic datasets. In time series, _heterogeneous_ refers to data composed of different types, sources, or temporal patterns, such as varying frequencies, units, or modalities across the series. This variety is essential for learning cross-domain temporal patterns and generalizing across different granularities, from 10-minute weather logs to yearly retail sales. Second, they use a decoder-only transformer with input patching, designed to scale across varying context and forecast lengths while maintaining training efficiency. The key parts of the decoder-only architecture are:

- Patch-based tokenization of time series inputs
    
- Residual multilayer perceptron (MLP) blocks for embedding
    
- Positional encodings to preserve temporal order
    
- Causal self-attention for autoregressive forecasting
    
- Decoupled input and output patch lengths to allow long-horizon forecasting in fewer steps
    

Let me break this down for you and explain each part.

After reading the section on PatchTST, this will already feel familiar. As you learned in [“PatchTST: A Time Series Is Worth 64 Words”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#PatchTSTSection), PatchTST introduced the concept of patching in time series forecasting, treating consecutive timesteps as a single token, similar to how vision transformers treat image patches. This allowed PatchTST to capture local temporal structure, reduce attention complexity, and enable longer historical lookbacks. TimesFM builds on this idea.

Just like in PatchTST, TimesFM treats segments of the time series as patches. The difference is that while PatchTST uses an encoder-based transformer, TimesFM adopts a decoder-only architecture, more similar to language models like GPT or Llama. That is, each input time series is divided into contiguous, nonoverlapping patches of length _p_.

These patches are passed through a residual MLP block with one hidden layer that has a skip connection. The patches are then transformed into fixed-length vectors of model dimension . Positional encodings are added to these patch embeddings to maintain their order in time. This results for the -th input token to the subsequent transformer layers as:

$$
t_j = \operatorname{InputResidualBlock}\!\left(\tilde{y}_j \odot (1 - \hat{m}_j)\right) + PE_j
$$

 $\tilde{y}_j$ is the $j-th$ input patch, defined as $\tilde{y}_j=yp(j-1) + 1:pj.\tilde{m}_j$.  is the corresponding mask, and  denotes element-wise multiplication used to zero out masked values in the input patch, enabling the model to simulate different context lengths during training. This is critical for zero-shot generalization and robustness.  is the positional encoding added to retain the temporal order of the patch token $t_j$.

This transforms a time series of length $L$  into $N = \left\lfloor \frac{L}{p} \right\rfloor$ tokens, just like in PatchTST. However, instead of channel independence and encoder mapping, TimesFM processes these tokens autoregressively (left to right) using causal attention.

The code in Examples [2-14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#ResidualTimesFM) and [2-15](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#MLPTimesFM) shows how the classes work together to support the architectural innovation TimesFM introduces for patching and input layers.

##### Example 2-14. Residual block in TimesFM

```python
class ResidualBlock(nn.Module):

    def __init__(self, input_dims, hidden_dims, output_dims):
        super(ResidualBlock, self).__init__()
        self.input_dims = input_dims
        self.hidden_dims = hidden_dims
        self.output_dims = output_dims

    # Hidden nonlinear transformation
    self.hidden_layer = nn.Sequential(
        nn.Linear(input_dims, hidden_dims),  #1
        nn.SiLU(),                            #2
    )

    # Output projection
    self.output_layer = nn.Linear(hidden_dims, output_dims)  #3

    # Residual connection to project input directly to output_dims
    self.residual_layer = nn.Linear(input_dims, output_dims)  #4

    def forward(self, x):
        hidden = self.hidden_layer(x)          # 5
        output = self.output_layer(hidden)     # 6
        residual = self.residual_layer(x)      # 7
        return output + residual               # 8
```

1. [Projects the input patch (for instance, 32 timesteps) to a hidden representation.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-1)
2. [Applies a non-linear activation to enhance learning capacity.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-2)
3. [Maps the hidden vector to the model’s transformer dimension .](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-3)
4. [Direct residual path ensures that information from the raw patch can bypass transformation.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-4)
5. [Transforms each patch into a learnable high-dimensional embedding for inputs and autoregressive outputs.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-5)
6. [Nonlinear path models complex local dependencies.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-6)
7. [Ensures that even short input patches or sparse data contribute signal.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-7)
8. [Adds the residual and MLP outputs to decode longer output patches with fewer autoregressive steps.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO2-8)

This block is used in two places:

- To convert input patches  into transformer tokens 
    
- To map the decoder output tokens into multi-step predictions over output patches (e.g., 128-step forecasts from 32-step contexts)
    

##### Example 2-15. MLP block in TimesFM

```python
 class TransformerMLP(nn.Module):

      def __init__(
          self,
          hidden_size: int,
          intermediate_size: int,
      ):
        super().__init__()
        self.gate_proj = nn.Linear(hidden_size, intermediate_size) # 1
        self.down_proj = nn.Linear(intermediate_size, hidden_size) # 2
        self.layer_norm = nn.LayerNorm(normalized_shape=hidden_size, eps=1e-6) # 3

      def forward(self, x, paddings=None):
        gate_inp = self.layer_norm(x) # 4
        gate = self.gate_proj(gate_inp) # 5
        gate = F.relu(gate) # 6
        outputs = self.down_proj(gate) # 7
        if paddings is not None:
          outputs = outputs * (1.0 - paddings[:, :, None]) # 8
        return outputs + x # 9
```
1. [Projects the normalized input token to an intermediate feature space.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-1)
2. [Compresses the expanded representation back to the model’s original size .](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-2)
3. [Layer normalization ensures stable learning even across variable-length patch sequences.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-3)
4. [Applies normalization before feeding tokens into the MLP (pre-norm variant).](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-4)
5. [The first linear transformation expands model capacity.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-5)
6. [_Rectified Linear Unit_ (ReLU) introduces nonlinearity to model complex intra-token patterns.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-6)
7. [Projects the output back to the original embedding space.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-7)
8. [Padding-aware masking ensures that masked or padded patches (e.g., partial windows) don’t affect the MLP computation.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO3-8)
9. [Adds a residual connection from the input to the output, preserving information across layers.](![[../../assets/Pasted image 20260518104635.png]])

This MLP is used inside every decoder layer to process each token after causal attention, ensuring that TimesFM can handle:

- Masked input patches during training (to generalize across context lengths)
    
- Long output patches during decoding (to avoid step-by-step generation when possible)
    

These two blocks help avoid full-step autoregressive generation while still maintaining decoder-style generalization and ensuring compatibility with variable-length, masked patch inputs. These input tokens are processed through a stack of  transformer layers using causal self-attention. This ensures that each output token attends to patches only from the past or present, not the future. This can be mathematically formulated as:

This design enables autoregressive forecasting where each prediction depends only on previously observed data, mimicking the LLM-style decoding.

After processing, each output token is mapped to a forecast patch using a second residual MLP block. Importantly, TimesFM supports different lengths for input and output patches (e.g., input length = 32, output length = 128), allowing it to predict longer sequences in fewer steps. This relationship is expressed by the following equation:

This structure enables efficient long-horizon forecasting: rather than generating one step at a time, TimesFM can jump ahead by larger windows. To ensure robustness across varying context lengths, a random patch masking strategy is used during training. This forces the model to learn from incomplete histories, improving its ability to generalize in zero-shot scenarios.

Let’s say patch length  and max context length is 512. During training, the model might randomly mask the first 4 points in the first patch, making it see only 28 steps instead of 32. Repeating this across all windows ensures that the model sees every possible context length up to 512.

## Fine-Tuning TimesFM on Hourly Energy Consumption Data

The TimesFM paper comes with an extensive code repository and even with [checkpoints](https://oreil.ly/wpEoj) for different model sizes on HuggingFace. I cloned the [repository](https://oreil.ly/REDqm) and adjusted the provided fine-tuning code for you a bit. Let’s look at the important steps in [Example 2-16](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#FineTuningTimesFM).

##### Example 2-16. Fine-tuning TimesFM on hourly energy consumption data

```python
def finetune_model():
    model, hparams, tfm_config = get_model(load_weights=True) # 1

    config = FinetuningConfig(
        batch_size=64,
        num_epochs=5,
        learning_rate=1e-4,
        use_wandb=True, # 2
        freq_type=1, # 3
        log_every_n_steps=10,
        val_check_interval=0.5,
        use_quantile_loss=True # 4
    )

    train_dataset, val_dataset = get_data( # 5
        context_len=192,
        horizon_len=tfm_config.horizon_len,
        freq_type=config.freq_type
    )

    finetuner = TimesFMFinetuner(model, config) # 6
    print("Starting finetuning...")

    results = finetuner.finetune( # 7
        train_dataset=train_dataset,
        val_dataset=val_dataset
    )

    print(f"Finetuning completed after {len
    (results['history']['train_loss'])} epochs.")

    mae, ctx, future, preds = evaluate_model(model, val_dataset) # 8
    plot_forecast(ctx, future, preds, save_path="timesfm_predictions.png") # 9

    print(f"Validation MAE: {mae:.4f}")
```

1. [Loads the pretrained TimesFM model along with its hyperparameters and configuration. Set `load_weights=True` to start from the foundation model checkpoint.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-1)
2. [Enables logging to Weights & Biases (optional for experiment tracking).](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-2)
3. [Specifies the frequency encoding type for the time series (e.g., hourly, daily).](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-3)
4. [Uses quantile loss instead of MSE, which is common in probabilistic forecasting tasks.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-4)
5. [Loads the training and validation datasets, specifying context (lookback) length and forecast horizon.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-5)
6. [Initializes the finetuner object that wraps the model and training loop logic.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-5)
7. [Starts the fine-tuning loop using the specified datasets and config. Returns a history object with training stats.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-7)
8. [Evaluates the fine-tuned model on the validation dataset and computes MAE (Mean Absolute Error).](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-8)
9. [Plots a forecast using the last validation sample and saves it to disk for visual inspection.](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#co_transformers_for_time_series_CO4-9)

[Figure 2-13](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#plotPredTimesFM) shows the result of the training.

![[../../assets/Pasted image 20260518105135.png]]

###### Figure 2-13. Fine-tuning result after five epochs.

The result of the fine-tuning doesn’t look so bad considering the fact that I fine-tuned the model for less than 30 minutes on an A100 GPU.

# AnomalyBERT for Self-Supervised Anomaly Detection

AnomalyBERT[9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id485) is capable of detecting anomalies in complex time series data. The model is inspired by BERT[10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id487) from natural language processing (NLP), but modifies the masked language modeling by replacing a random portion of the input data with degraded data and training the model to identify the degraded part. [Figure 2-14](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#AnomalyBERT_degradation) shows the degradation examples, consisting of soft replacement, uniform replacement, peak noise, and length adjustment.

_Soft replacement_ involves substituting the sequence with one sequence fetched from outside the window, representing a weighted sum of the original interval and an external interval. The _uniform replacement_ substitutes the sequence with a constant value, while _length adjustment_ refers to lengthening or shortening the sequence. _Peak noise_ adds a single peak value. This data degradation technique helps in detecting various unnatural patterns in real-world time series.

![[../../assets/Pasted image 20260518105143.png]]

Figure 2-14. Degradation examples from the training data for AnomalyBERT. Image adapted from Yungi Jeong et al. (2023).

AnomalyBERT consists of three components: a linear embedding layer, a transformer body, and a prediction block. A window of multivariate time series  is input into the model, and the linear embedding layer projects each data patch  in the window  to an embedded feature. The transformer body processes all embedded features from , producing latent features that share information and reflect the temporal context. The prediction block outputs anomaly scores for the data points in the window, with higher scores indicating more anomalous points. This architecture is shown in [Figure 2-15](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#AnomalyBERT_archi).

![[../../assets/Pasted image 20260518105149.png]]

Figure 2-15. Architecture of AnomalyBERT, with a transformer body consisting of transformer layers that use 1D relative position bias. Image adapted from Yungi Jeong et al. (2023).

The transformer encoder serves as the main body, with each layer containing a multi-head self-attention (MSA) module and an MLP block. Each module is preceded by a LayerNorm (LN) layer, and the Gaussian Error Linear Unit (GELU) is used for activation. GELU smooths the output using a Gaussian cumulative distribution by retaining input values close to zero and scaling larger values non-linearly. Instead of using sinusoidal positional encodings or absolute position embeddings, one-dimensional relative position bias is added to each attention matrix to consider the relative positions between features. Self-attention in each head with the relative bias is computed as:
![[../../assets/Pasted image 20260518105226.png]]

Here, $Q$ , $K$ , and $V$ are the query, key, and value of input features, respectively, and  is the dimension of features in an attention head.  is the relative position bias:

![[../../assets/Pasted image 20260518105249.png]]

Each element $b_{i,j} = \hat{b}_{j-i}$ is derived from a learnable bias table. A different position bias is applied to each MSA module.

AnomalyBERT was tested on five widely used benchmark datasets, each of which contains an unlabeled training dataset and a labeled test set:

Secure water treatment

_Secure water treatment_ (SWaT) is a dataset generated from a water treatment testbed, designed to simulate a real-world water treatment process. It includes various sensor and actuator data.

Water distribution

_Water distribution_ (WADI) is a dataset collected from a water distribution testbed, capturing the behavior of a water distribution system over time. Like SWaT, it includes sensor and actuator data.

Soil moisture active passive

_Soil moisture active passive_ (SMAP) is a dataset from NASA’s soil moisture active passive satellite mission. It includes time series data from satellite measurements related to soil moisture.

Mars science laboratory

_Mars science laboratory_ (MSL) is a dataset collected from NASA’s Mars rover capturing various telemetry data points to monitor the rover’s health and detect anomalies.

Server machine dataset

_Server machine dataset_ is a dataset collected from servers, recording metrics like CPU usage, memory usage, and network traffic, to simulate real-world issues in server performance.

AnomalyBERT outperforms the previous methods on all datasets.

# Conclusion

In this chapter, you explored the transformative role of transformers in time series modeling and discovered their superiority in capturing long-sequence interactions compared to traditional RNN models.

You delved into key time series concepts such as autocorrelation, cointegration, cross-correlation, and stationarity, understanding their importance in analyzing time series data. Additionally, you learned techniques for handling trends and seasonality and gained insights into the significance of proper data preparation to avoid biases and improve model performance.

You examined different use cases for time series modeling, from forecasting and classification to anomaly detection and spatiotemporal prediction. Along the way, you learned how transformers adapt to these challenges by tokenizing continuous input through techniques like lagged features (Lag-Llama), quantized vocabularies (Chronos), or patch-based segmentation (PatchTST, TimesFM).

You explored how to fine-tune Chronos, PatchTST, and TimesFM. You also looked at how AnomalyBERT uses degraded data to learn robust representations for unsupervised anomaly detection.

From autoregressive decoders to masked transformer encoders, and from quantized digits to continuous patches, this chapter has given you a deep understanding of how transformer-based models are adapted to structured, sequential, and highly temporal data for various domains.

In [Chapter 3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#chapter_3), you’ll learn about transformers for vision tasks, another domain that greatly benefits from foundation models and their few-shot and zero-shot capabilities.

[1](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id454-marker) Yuqi Nie et al. [“A Time Series Is Worth 64 Words: Long-Term Forecasting with Transformers”](https://arxiv.org/pdf/2211.14730) (2023).

[2](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id456-marker) Kashif Rasul et al. [“Lag-Llama: Towards Foundation Models for Probabilistic Time Series Forecasting”](https://arxiv.org/pdf/2310.08278) (2024).

[3](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id458-marker) Nate Gruver et al. [“Large Language Models Are Zero-Shot Time Series Forecasters”](https://arxiv.org/pdf/2310.07820) (2024).

[4](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id460-marker) Abdul Fatir Ansari et al. [“Chronos: Learning the Language of Time Series”](https://arxiv.org/pdf/2403.07815) (2024).

[5](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id467-marker) Colin Raffel et al. [“Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"](https://arxiv.org/abs/1910.10683) (2019).

[6](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id471-marker) Yuqi Nie et al. [“A Time Series Is Worth 64 Words: Long-Term Forecasting with Transformers”](https://arxiv.org/abs/2211.14730) (2023).

[7](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id479-marker) Jared Kaplan et al. [“Scaling Laws for Neural Language Models”](https://arxiv.org/abs/2001.08361) (2020).

[8](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id481-marker) Abhimanyu Das et al. [“A Decoder-Only Foundation Model for Time-Series Forecasting”](https://arxiv.org/abs/2310.10688) (2017).

[9](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id485-marker) Yungi Jeong et al. [“AnomalyBERT: Self-Supervised Transformer for Time Series Anomaly Detection Using Data Degradation Scheme”](https://arxiv.org/abs/2305.04468) (2023).

[10](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#id487-marker) Jacob Devlin et al. [“BERT: Pre-Training of Deep Bidirectional Transformers for Language Understanding"](https://arxiv.org/abs/1810.04805) (2018).
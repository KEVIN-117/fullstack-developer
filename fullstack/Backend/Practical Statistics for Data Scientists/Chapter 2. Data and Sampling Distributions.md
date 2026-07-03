A popular misconception holds that the era of big data means the end of a need for sampling. In fact, the proliferation of data of varying quality and relevance reinforces the need for sampling as a tool to work efficiently with a variety of data and to minimize bias. Even in a big data project, predictive models are typically developed and piloted with samples. Samples are also used in tests of various sorts (e.g., comparing the effect of web page designs on clicks).

[Figure 2-1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#sampling_schematic) shows a schematic that underpins the concepts we will discuss in this chapter—data and sampling distributions. The lefthand side represents a population that, in statistics, is assumed to follow an underlying but _unknown_ distribution. All that is available is the _sample_ data and its empirical distribution, shown on the righthand side. To get from the lefthand side to the righthand side, a _sampling_ procedure is used (represented by an arrow). Traditional statistics focused very much on the lefthand side, using theory based on strong assumptions about the population. Modern statistics has moved to the righthand side, where such assumptions are not needed.

In general, data scientists need not worry about the theoretical nature of the lefthand side and instead should focus on the sampling procedures and the data at hand. There are some notable exceptions. Sometimes data is generated from a physical process that can be modeled. The simplest example is flipping a coin: this follows a binomial distribution. Any real-life binomial situation (buy or don’t buy, fraud or no fraud, click or don’t click) can be modeled effectively by a coin (with modified probability of landing heads, of course). In these cases, we can gain additional insight by using our understanding of the population.

![images/sampling_schematic.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0201.png)

###### Figure 2-1. Population versus sample

# Random Sampling and Sample Bias

A _sample_ is a subset of data from a larger data set; statisticians call this larger data set the _population_. A population in statistics is not the same thing as in biology—it is a large, defined (but sometimes theoretical or imaginary) set of data.

_Random sampling_ is a process in which each available member of the population being sampled has an equal chance of being chosen for the sample at each draw. The sample that results is called a _simple random sample_. Sampling can be done _with replacement_, in which observations are put back in the population after each draw for possible future reselection. Or it can be done _without replacement_, in which case observations, once selected, are unavailable for future draws.

Data quality often matters more than data quantity when making an estimate or a model based on a sample. Data quality in data science involves completeness, consistency of format, cleanliness, and accuracy of individual data points. Statistics adds the notion of _representativeness_.

##### Key Terms for Random Sampling

**_Sample_**

A subset from a larger data set.

**_Population_**

The larger data set or idea of a data set.

**_N_ (_n_)**

The size of the population (sample).

**_Random sampling_**

Drawing elements into a sample at random.

**_Stratified sampling_**

Dividing the population into strata and randomly sampling from each strata.

**_Stratum (pl., strata)_**

A homogeneous subgroup of a population with common characteristics.

**_Simple random sample_**

The sample that results from random sampling without stratifying the population.

**_Bias_**

Systematic error.

**_Sample bias_**

A sample that misrepresents the population.

The classic example is the _Literary Digest_ poll of 1936 that predicted a victory of Alf Landon over Franklin Roosevelt. The _Literary Digest_, a leading periodical of the day, polled its entire subscriber base plus additional lists of individuals, a total of over 10 million people, and predicted a landslide victory for Landon. George Gallup, founder of the Gallup Poll, conducted biweekly polls of just 2,000 people and accurately predicted a Roosevelt victory. The difference lay in the selection of those polled.

The _Literary Digest_ opted for quantity, paying little attention to the method of selection. They ended up polling those with relatively high socioeconomic status (their own subscribers, plus those who, by virtue of owning luxuries like telephones and automobiles, appeared in marketers’ lists). The result was _sample bias_; that is, the sample was different in some meaningful and nonrandom way from the larger population it was meant to represent. The term _nonrandom_ is important—hardly any sample, including random samples, will be exactly representative of the population. Sample bias occurs when the difference is meaningful, and it can be expected to continue for other samples drawn in the same way as the first.

# Self-Selection Sampling Bias

The reviews of restaurants, hotels, cafés, and so on that you read on social media sites like Yelp are prone to bias because the people submitting them are not randomly selected; rather, they themselves have taken the initiative to write. This leads to self-selection bias—the people motivated to write reviews may have had poor experiences, may have an association with the establishment, or may simply be a different type of person from those who do not write reviews. Note that while self-selection samples can be unreliable indicators of the true state of affairs, they may be more reliable in simply comparing one establishment to a similar one; the same self-selection bias might apply to each.

## Bias

Statistical bias refers to measurement or sampling errors that are systematic and produced by the measurement or sampling process. An important distinction should be made between errors due to random chance and errors due to bias. Consider the physical process of a gun shooting at a target. It will not hit the absolute center of the target every time, or even much at all. An unbiased process will produce error, but it is random and does not tend strongly in any direction (see [Figure 2-2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#gun1)). The results shown in [Figure 2-3](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#gun2) show a biased process—there is still random error in both the x and y direction, but there is also a bias. Shots tend to fall in the upper-right quadrant.

![images/Target-scatter.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0202.png)

###### Figure 2-2. Scatterplot of shots from a gun with true aim

![images/Target-scatter-bias.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0203.png)

###### Figure 2-3. Scatterplot of shots from a gun with biased aim

Bias comes in different forms, and may be observable or invisible. When a result does suggest bias (e.g., by reference to a benchmark or actual values), it is often an indicator that a statistical or machine learning model has been misspecified, or an important variable left out.

## Random Selection

To avoid the problem of sample bias that led the _Literary Digest_ to predict Landon over Roosevelt, George Gallup (shown in [Figure 2-4](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#Gallup)) opted for more scientifically chosen methods to achieve a sample that was representative of the US voting electorate. There are now a variety of methods to achieve representativeness, but at the heart of all of them lies _random sampling_.

![Gallup](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0204.png)

###### Figure 2-4. George Gallup, catapulted to fame by the _Literary Digest’s_ “big data” failure

Random sampling is not always easy. Proper definition of an accessible population is key. Suppose we want to generate a representative profile of customers and we need to conduct a pilot customer survey. The survey needs to be representative but is labor intensive.

First, we need to define who a customer is. We might select all customer records where purchase amount > 0. Do we include all past customers? Do we include refunds? Internal test purchases? Resellers? Both billing agent and customer?

Next, we need to specify a sampling procedure. It might be “select 100 customers at random.” Where a sampling from a flow is involved (e.g., real-time customer transactions or web visitors), timing considerations may be important (e.g., a web visitor at 10 a.m. on a weekday may be different from a web visitor at 10 p.m. on a weekend).

In _stratified sampling_, the population is divided up into _strata_, and random samples are taken from each stratum. Political pollsters might seek to learn the electoral preferences of whites, blacks, and Hispanics. A simple random sample taken from the population would yield too few blacks and Hispanics, so those strata could be overweighted in stratified sampling to yield equivalent sample sizes.

## Size Versus Quality: When Does Size Matter?

In the era of big data, it is sometimes surprising that smaller is better. Time and effort spent on random sampling not only reduces bias but also allows greater attention to data exploration and data quality. For example, missing data and outliers may contain useful information. It might be prohibitively expensive to track down missing values or evaluate outliers in millions of records, but doing so in a sample of several thousand records may be feasible. Data plotting and manual inspection bog down if there is too much data.

So when _are_ massive amounts of data needed?

The classic scenario for the value of big data is when the data is not only big but sparse as well. Consider the search queries received by Google, where columns are terms, rows are individual search queries, and cell values are either 0 or 1, depending on whether a query contains a term. The goal is to determine the best predicted search destination for a given query. There are over 150,000 words in the English language, and Google processes over one trillion queries per year. This yields a huge matrix, the vast majority of whose entries are “0.”

This is a true big data problem—only when such enormous quantities of data are accumulated can effective search results be returned for most queries. And the more data accumulates, the better the results. For popular search terms this is not such a problem—effective data can be found fairly quickly for the handful of extremely popular topics trending at a particular time. The real value of modern search technology lies in the ability to return detailed and useful results for a huge variety of search queries, including those that occur with a frequency, say, of only one in a million.

Consider the search phrase “Ricky Ricardo and Little Red Riding Hood.” In the early days of the internet, this query would probably have returned results on the bandleader Ricky Ricardo, the television show _I Love Lucy_ in which that character appeared, and the children’s story _Little Red Riding Hood_. Both of those individual items would have had many searches to refer to, but the combination would have had very few. Later, now that trillions of search queries have been accumulated, this search query returns the exact _I Love Lucy_ episode in which Ricky narrates, in dramatic fashion, the _Little Red Riding Hood_ story to his infant son in a comic mix of English and Spanish.

Keep in mind that the number of actual _pertinent_ records—ones in which this exact search query, or something very similar, appears (together with information on what link people ultimately clicked on)—might need only be in the thousands to be effective. However, many trillions of data points are needed to obtain these pertinent records (and random sampling, of course, will not help). See also [“Long-Tailed Distributions”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#LongTailedData).

## Sample Mean Versus Population Mean

The symbol  (pronounced “x-bar”) is used to represent the mean of a sample from a population, whereas  is used to represent the mean of a population. Why make the distinction? Information about samples is observed, and information about large populations is often inferred from smaller samples. Statisticians like to keep the two things separate in the symbology.

##### Key Ideas

- Even in the era of big data, random sampling remains an important arrow in the data scientist’s quiver.
    
- Bias occurs when measurements or observations are systematically in error because they are not representative of the full population.
    
- Data quality is often more important than data quantity, and random sampling can reduce bias and facilitate quality improvement that would otherwise be prohibitively expensive.
    

## Further Reading

- A useful review of sampling procedures can be found in Ronald Fricker’s chapter “Sampling Methods for Online Surveys” in _The SAGE Handbook of Online Research Methods_, 2nd ed., edited by Nigel G. Fielding, Raymond M. Lee, and Grant Blank (SAGE Publications, 2016). This chapter includes a review of the modifications to random sampling that are often used for practical reasons of cost or feasibility.
    
- The story of the _Literary Digest_ poll failure can be found on the [Capital Century website](https://oreil.ly/iSoQT).
    

# Selection Bias

To paraphrase Yogi Berra: if you don’t know what you’re looking for, look hard enough and you’ll find it.

Selection bias refers to the practice of selectively choosing data—consciously or unconsciously—in a way that leads to a conclusion that is misleading or ephemeral.

##### Key Terms for Selection Bias

**_Selection bias_**

Bias resulting from the way in which observations are selected.

**_Data snooping_**

Extensive hunting through data in search of something interesting.

**_Vast search effect_**

Bias or nonreproducibility resulting from repeated data modeling, or modeling data with large numbers of predictor variables.

If you specify a hypothesis and conduct a well-designed experiment to test it, you can have high confidence in the conclusion. This is frequently not what occurs, however. Often, one looks at available data and tries to discern patterns. But are the patterns real? Or are they just the product of _data snooping_—that is, extensive hunting through the data until something interesting emerges? There is a saying among statisticians: “If you torture the data long enough, sooner or later it will confess.”

The difference between a phenomenon that you verify when you test a hypothesis using an experiment and a phenomenon that you discover by perusing available data can be illuminated with the following thought experiment.

Imagine that someone tells you they can flip a coin and have it land heads on the next 10 tosses. You challenge them (the equivalent of an experiment), and they proceed to toss the coin 10 times, with all flips landing heads. Clearly you ascribe some special talent to this person—the probability that 10 coin tosses will land heads just by chance is 1 in 1,000.

Now imagine that the announcer at a sports stadium asks the 20,000 people in attendance each to toss a coin 10 times, and to report to an usher if they get 10 heads in a row. The chance that _somebody_ in the stadium will get 10 heads is extremely high (more than 99%—it’s 1 minus the probability that nobody gets 10 heads). Clearly, selecting after the fact the person (or persons) who gets 10 heads at the stadium does not indicate they have any special talent—it’s most likely luck.

Since repeated review of large data sets is a key value proposition in data science, selection bias is something to worry about. A form of selection bias of particular concern to data scientists is what John Elder (founder of Elder Research, a respected data mining consultancy) calls the _vast search effect_. If you repeatedly run different models and ask different questions with a large data set, you are bound to find something interesting. But is the result you found truly something interesting, or is it the chance outlier?

We can guard against this by using a holdout set, and sometimes more than one holdout set, against which to validate performance. Elder also advocates the use of what he calls _target shuffling_ (a permutation test, in essence) to test the validity of predictive associations that a data mining model suggests.

Typical forms of selection bias in statistics, in addition to the vast search effect, include nonrandom sampling (see [“Random Sampling and Sample Bias”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#randomSampling_bias)), cherry-picking data, selection of time intervals that accentuate a particular statistical effect, and stopping an experiment when the results look “interesting.”

## Regression to the Mean

_Regression to the mean_ refers to a phenomenon involving successive measurements on a given variable: extreme observations tend to be followed by more central ones. Attaching special focus and meaning to the extreme value can lead to a form of selection bias.

Sports fans are familiar with the “rookie of the year, sophomore slump” phenomenon. Among the athletes who begin their career in a given season (the rookie class), there is always one who performs better than all the rest. Generally, this “rookie of the year” does not do as well in his second year. Why not?

In nearly all major sports, at least those played with a ball or puck, there are two elements that play a role in overall performance:

- Skill
    
- Luck
    

Regression to the mean is a consequence of a particular form of selection bias. When we select the rookie with the best performance, skill and good luck are probably contributing. In his next season, the skill will still be there, but very often the luck will not be, so his performance will decline—it will regress. The phenomenon was first identified by Francis Galton in 1886 [[Galton-1886]](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/bibliography01.html#Galton-1886), who wrote of it in connection with genetic tendencies; for example, the children of extremely tall men tend not to be as tall as their father (see [Figure 2-5](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#Galton)).

![Galton](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0205.png)

###### Figure 2-5. Galton’s study that identified the phenomenon of regression to the mean

###### Warning

Regression to the mean, meaning to “go back,” is distinct from the statistical modeling method of linear regression, in which a linear relationship is estimated between predictor variables and an outcome variable.

##### Key Ideas

- Specifying a hypothesis and then collecting data following randomization and random sampling principles ensures against bias.
    
- All other forms of data analysis run the risk of bias resulting from the data collection/analysis process (repeated running of models in data mining, data snooping in research, and after-the-fact selection of interesting events).
    

## Further Reading

- Christopher J. Pannucci and Edwin G. Wilkins’ article “Identifying and Avoiding Bias in Research” in (surprisingly not a statistics journal) _Plastic and Reconstructive Surgery_ (August 2010) has an excellent review of various types of bias that can enter into research, including selection bias.
    
- Michael Harris’s article [“Fooled by Randomness Through Selection Bias”](https://oreil.ly/v_Q0u) provides an interesting review of selection bias considerations in stock market trading schemes, from the perspective of traders.
    

# Sampling Distribution of a Statistic

The term _sampling distribution_ of a statistic refers to the distribution of some sample statistic over many samples drawn from the same population. Much of classical statistics is concerned with making inferences from (small) samples to (very large) populations.

##### Key Terms for Sampling Distribution

**_Sample statistic_**

A metric calculated for a sample of data drawn from a larger population.

**_Data distribution_**

The frequency distribution of individual _values_ in a data set.

**_Sampling distribution_**

The frequency distribution of a _sample statistic_ over many samples or resamples.

**_Central limit theorem_**

The tendency of the sampling distribution to take on a normal shape as sample size rises.

**_Standard error_**

The variability (standard deviation) of a sample _statistic_ over many samples (not to be confused with _standard deviation_, which by itself, refers to variability of individual data _values_).

Typically, a sample is drawn with the goal of measuring something (with a _sample statistic_) or modeling something (with a statistical or machine learning model). Since our estimate or model is based on a sample, it might be in error; it might be different if we were to draw a different sample. We are therefore interested in how different it might be—a key concern is _sampling variability_. If we had lots of data, we could draw additional samples and observe the distribution of a sample statistic directly. Typically, we will calculate our estimate or model using as much data as is easily available, so the option of drawing additional samples from the population is not readily available.

###### Warning

It is important to distinguish between the distribution of the individual data points, known as _the data distribution_, and the distribution of a sample statistic, known as the _sampling distribution_.

The distribution of a sample statistic such as the mean is likely to be more regular and bell-shaped than the distribution of the data itself. The larger the sample the statistic is based on, the more this is true. Also, the larger the sample, the narrower the distribution of the sample statistic.

This is illustrated in an example using annual income for loan applicants to LendingClub (see [“A Small Example: Predicting Loan Default”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch06.html#LoanExampleKNN) for a description of the data). Take three samples from this data: a sample of 1,000 values, a sample of 1,000 means of 5 values, and a sample of 1,000 means of 20 values. Then plot a histogram of each sample to produce [Figure 2-6](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#loans-mean-hist).

![Loans histogram](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0206.png)

###### Figure 2-6. Histogram of annual incomes of 1,000 loan applicants (top), then 1,000 means of n=5 applicants (middle), and finally 1,000 means of n=20 applicants (bottom)

The histogram of the individual data values is broadly spread out and skewed toward higher values, as is to be expected with income data. The histograms of the means of 5 and 20 are increasingly compact and more bell-shaped. Here is the _R_ code to generate these histograms, using the visualization package `ggplot2`:

```
library
```

The _Python_ code uses `seaborn`’s `FacetGrid` to show the three histograms:

```
import
```

## Central Limit Theorem

The phenomenon we’ve just described is termed the _central limit theorem_. It says that the means drawn from multiple samples will resemble the familiar bell-shaped normal curve (see [“Normal Distribution”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#NormalDist)), even if the source population is not normally distributed, provided that the sample size is large enough and the departure of the data from normality is not too great. The central limit theorem allows normal-approximation formulas like the t-distribution to be used in calculating sampling distributions for inference—that is, confidence intervals and hypothesis tests.

The central limit theorem receives a lot of attention in traditional statistics texts because it underlies the machinery of hypothesis tests and confidence intervals, which themselves consume half the space in such texts. Data scientists should be aware of this role; however, since formal hypothesis tests and confidence intervals play a small role in data science, and the _bootstrap_ (see [“The Bootstrap”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#bootstrap)) is available in any case, the central limit theorem is not so central in the practice of data science.

## Standard Error

The _standard error_ is a single metric that sums up the variability in the sampling distribution for a statistic. The standard error can be estimated using a statistic based on the standard deviation _s_ of the sample values, and the sample size _n_:

As the sample size increases, the standard error decreases, corresponding to what was observed in [Figure 2-6](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#loans-mean-hist). The relationship between standard error and sample size is sometimes referred to as the _square root of n_ rule: to reduce the standard error by a factor of 2, the sample size must be increased by a factor of 4.

The validity of the standard error formula arises from the central limit theorem. In fact, you don’t need to rely on the central limit theorem to understand standard error. Consider the following approach to measuring standard error:

1. Collect a number of brand-new samples from the population.
    
2. For each new sample, calculate the statistic (e.g., mean).
    
3. Calculate the standard deviation of the statistics computed in step 2; use this as your estimate of standard error.
    

In practice, this approach of collecting new samples to estimate the standard error is typically not feasible (and statistically very wasteful). Fortunately, it turns out that it is not necessary to draw brand new samples; instead, you can use _bootstrap_ resamples. In modern statistics, the bootstrap has become the standard way to estimate standard error. It can be used for virtually any statistic and does not rely on the central limit theorem or other distributional assumptions.

# Standard Deviation Versus Standard Error

Do not confuse standard deviation (which measures the variability of individual data points) with standard error (which measures the variability of a sample metric).

##### Key Ideas

- The frequency distribution of a sample statistic tells us how that metric would turn out differently from sample to sample.
    
- This sampling distribution can be estimated via the bootstrap, or via formulas that rely on the central limit theorem.
    
- A key metric that sums up the variability of a sample statistic is its standard error.
    

## Further Reading

David Lane’s [online multimedia resource in statistics](https://oreil.ly/pe7ra) has a useful simulation that allows you to select a sample statistic, a sample size, and the number of iterations and visualize a histogram of the resulting frequency distribution.

# The Bootstrap

One easy and effective way to estimate the sampling distribution of a statistic, or of model parameters, is to draw additional samples, with replacement, from the sample itself and recalculate the statistic or model for each resample. This procedure is called the _bootstrap_, and it does not necessarily involve any assumptions about the data or the sample statistic being normally distributed.

##### Key Terms for the Bootstrap

**_Bootstrap sample_**

A sample taken with replacement from an observed data set.

**_Resampling_**

The process of taking repeated samples from observed data; includes both bootstrap and permutation (shuffling) procedures.

Conceptually, you can imagine the bootstrap as replicating the original sample thousands or millions of times so that you have a hypothetical population that embodies all the knowledge from your original sample (it’s just larger). You can then draw samples from this hypothetical population for the purpose of estimating a sampling distribution; see [Figure 2-7](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#bootstrap-schematic-1).

![images/Bootstrap-schematic-1.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0207.png)

###### Figure 2-7. The idea of the bootstrap

In practice, it is not necessary to actually replicate the sample a huge number of times. We simply replace each observation after each draw; that is, we _sample with replacement_. In this way we effectively create an infinite population in which the probability of an element being drawn remains unchanged from draw to draw. The algorithm for a bootstrap resampling of the mean, for a sample of size _n_, is as follows:

1. Draw a sample value, record it, and then replace it.
    
2. Repeat _n_ times.
    
3. Record the mean of the _n_ resampled values.
    
4. Repeat steps 1–3 _R_ times.
    
5. Use the _R_ results to:
    
    1. Calculate their standard deviation (this estimates sample mean standard error).
        
    2. Produce a histogram or boxplot.
        
    3. Find a confidence interval.
        

_R_, the number of iterations of the bootstrap, is set somewhat arbitrarily. The more iterations you do, the more accurate the estimate of the standard error, or the confidence interval. The result from this procedure is a bootstrap set of sample statistics or estimated model parameters, which you can then examine to see how variable they are.

The _R_ package `boot` combines these steps in one function. For example, the following applies the bootstrap to the incomes of people taking out loans:

```
library
```

The function `stat_fun` computes the median for a given sample specified by the index `idx`. The result is as follows:

```
Bootstrap
```

The original estimate of the median is $62,000. The bootstrap distribution indicates that the estimate has a _bias_ of about –$70 and a standard error of $209. The results will vary slightly between consecutive runs of the algorithm.

The major _Python_ packages don’t provide implementations of the bootstrap approach. It can be implemented using the `scikit-learn` method `resample`:

```
results
```

The bootstrap can be used with multivariate data, where the rows are sampled as units (see [Figure 2-8](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#bootstrap-multivariate)). A model might then be run on the bootstrapped data, for example, to estimate the stability (variability) of model parameters, or to improve predictive power. With classification and regression trees (also called _decision trees_), running multiple trees on bootstrap samples and then averaging their predictions (or, with classification, taking a majority vote) generally performs better than using a single tree. This process is called _bagging_ (short for “bootstrap aggregating”; see [“Bagging and the Random Forest”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch06.html#Bagging)).

![images/Bootstrap-multivariate-schematic.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0208.png)

###### Figure 2-8. Multivariate bootstrap sampling

The repeated resampling of the bootstrap is conceptually simple, and Julian Simon, an economist and demographer, published a compendium of resampling examples, including the bootstrap, in his 1969 text _Basic Research Methods in Social Science_ (Random House). However, it is also computationally intensive and was not a feasible option before the widespread availability of computing power. The technique gained its name and took off with the publication of several journal articles and a book by Stanford statistician Bradley Efron in the late 1970s and early 1980s. It was particularly popular among researchers who use statistics but are not statisticians, and for use with metrics or models where mathematical approximations are not readily available. The sampling distribution of the mean has been well established since 1908; the sampling distribution of many other metrics has not. The bootstrap can be used for sample size determination; experiment with different values for _n_ to see how the sampling distribution is affected.

The bootstrap was met with considerable skepticism when it was first introduced; it had the aura to many of spinning gold from straw. This skepticism stemmed from a misunderstanding of the bootstrap’s purpose.

###### Warning

The bootstrap does not compensate for a small sample size; it does not create new data, nor does it fill in holes in an existing data set. It merely informs us about how lots of additional samples would behave when drawn from a population like our original sample.

## Resampling Versus Bootstrapping

Sometimes the term _resampling_ is used synonymously with the term _bootstrapping_, as just outlined. More often, the term _resampling_ also includes permutation procedures (see [“Permutation Test”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Permutation)), where multiple samples are combined and the sampling may be done without replacement. In any case, the term _bootstrap_ always implies sampling with replacement from an observed data set.

##### Key Ideas

- The bootstrap (sampling with replacement from a data set) is a powerful tool for assessing the variability of a sample statistic.
    
- The bootstrap can be applied in similar fashion in a wide variety of circumstances, without extensive study of mathematical approximations to sampling distributions.
    
- It also allows us to estimate sampling distributions for statistics where no mathematical approximation has been developed.
    
- When applied to predictive models, aggregating multiple bootstrap sample predictions (bagging) outperforms the use of a single model.
    

## Further Reading

- _An Introduction to the Bootstrap_ by Bradley Efron and Robert Tibshirani (Chapman & Hall, 1993) was the first book-length treatment of the bootstrap. It is still widely read.
    
- The retrospective on the bootstrap in the May 2003 issue of _Statistical Science_ (vol. 18, no. 2), discusses (among other antecedents, in Peter Hall’s “A Short Prehistory of the Bootstrap”) Julian Simon’s initial publication of the bootstrap in 1969.
    
- See _An Introduction to Statistical Learning_ by Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani (Springer, 2013) for sections on the bootstrap and, in particular, bagging.
    

# Confidence Intervals

Frequency tables, histograms, boxplots, and standard errors are all ways to understand the potential error in a sample estimate. Confidence intervals are another.

##### Key Terms for Confidence Intervals

**_Confidence level_**

The percentage of confidence intervals, constructed in the same way from the same population, that are expected to contain the statistic of interest.

**_Interval endpoints_**

The top and bottom of the confidence interval.

There is a natural human aversion to uncertainty; people (especially experts) say “I don’t know” far too rarely. Analysts and managers, while acknowledging uncertainty, nonetheless place undue faith in an estimate when it is presented as a single number (a _point estimate_). Presenting an estimate not as a single number but as a range is one way to counteract this tendency. Confidence intervals do this in a manner grounded in statistical sampling principles.

Confidence intervals always come with a coverage level, expressed as a (high) percentage, say 90% or 95%. One way to think of a 90% confidence interval is as follows: it is the interval that encloses the central 90% of the bootstrap sampling distribution of a sample statistic (see [“The Bootstrap”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#bootstrap)). More generally, an _x_% confidence interval around a sample estimate should, on average, contain similar sample estimates _x_% of the time (when a similar sampling procedure is followed).

Given a sample of size _n_, and a sample statistic of interest, the algorithm for a bootstrap confidence interval is as follows:

1. Draw a random sample of size _n_ with replacement from the data (a resample).
    
2. Record the statistic of interest for the resample.
    
3. Repeat steps 1–2 many (_R_) times.
    
4. For an _x_% confidence interval, trim [(100-_x_) / 2]% of the _R_ resample results from either end of the distribution.
    
5. The trim points are the endpoints of an _x_% bootstrap confidence interval.
    

[Figure 2-9](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#bootstrap-ci) shows a 90% confidence interval for the mean annual income of loan applicants, based on a sample of 20 for which the mean was $55,734. Note that this is the mean of the subset of 20 records and not the mean of the bootstrap analysis, $55,836.

![images/bootstrap-CI.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0209.png)

###### Figure 2-9. Bootstrap confidence interval for the annual income of loan applicants, based on a sample of 20

The bootstrap is a general tool that can be used to generate confidence intervals for most statistics, or model parameters. Statistical textbooks and software, with roots in over a half century of computerless statistical analysis, will also reference confidence intervals generated by formulas, especially the t-distribution (see [“Student’s t-Distribution”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#t-distribution)).

###### Note

Of course, what we are really interested in when we have a sample result is, “What is the probability that the true value lies within a certain interval?” This is not really the question that a confidence interval answers, but it ends up being how most people interpret the answer.

The probability question associated with a confidence interval starts out with the phrase “Given a sampling procedure and a population, what is the probability that…” To go in the opposite direction, “Given a sample result, what is the probability that (something is true about the population)?” involves more complex calculations and deeper imponderables.

The percentage associated with the confidence interval is termed the _level of confidence_. The higher the level of confidence, the wider the interval. Also, the smaller the sample, the wider the interval (i.e., the greater the uncertainty). Both make sense: the more confident you want to be, and the less data you have, the wider you must make the confidence interval to be sufficiently assured of capturing the true value.

###### Note

For a data scientist, a confidence interval is a tool that can be used to get an idea of how variable a sample result might be. Data scientists would use this information not to publish a scholarly paper or submit a result to a regulatory agency (as a researcher might) but most likely to communicate the potential error in an estimate, and perhaps to learn whether a larger sample is needed.

##### Key Ideas

- Confidence intervals are the typical way to present estimates as an interval range.
    
- The more data you have, the less variable a sample estimate will be.
    
- The lower the level of confidence you can tolerate, the narrower the confidence interval will be.
    
- The bootstrap is an effective way to construct confidence intervals.
    

## Further Reading

- For a bootstrap approach to confidence intervals, see _Introductory Statistics and Analytics: A Resampling Perspective_ by Peter Bruce (Wiley, 2014) or _Statistics: Unlocking the Power of Data_, 2nd ed., by Robin Lock and four other Lock family members (Wiley, 2016).
    
- Engineers, who have a need to understand the precision of their measurements, use confidence intervals perhaps more than most disciplines, and _Modern Engineering Statistics_ by Thomas Ryan (Wiley, 2007) discusses confidence intervals. It also reviews a tool that is just as useful and gets less attention: _prediction intervals_ (intervals around a single value, as opposed to a mean or other summary statistic).
    

# Normal Distribution

The bell-shaped normal distribution is iconic in traditional statistics.[1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#idm45782047495336) The fact that distributions of sample statistics are often normally shaped has made it a powerful tool in the development of mathematical formulas that approximate those distributions.

##### Key Terms for Normal Distribution

**_Error_**

The difference between a data point and a predicted or average value.

**_Standardize_**

Subtract the mean and divide by the standard deviation.

**_z-score_**

The result of standardizing an individual data point.

**_Standard normal_**

A normal distribution with mean = 0 and standard deviation = 1.

**_QQ-Plot_**

A plot to visualize how close a sample distribution is to a specified distribution, e.g., the normal distribution.

In a normal distribution ([Figure 2-10](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#normal-curve)), 68% of the data lies within one standard deviation of the mean, and 95% lies within two standard deviations.

###### Warning

It is a common misconception that the normal distribution is called that because most data follows a normal distribution—that is, it is the normal thing. Most of the variables used in a typical data science project—in fact, most raw data as a whole—are _not_ normally distributed: see [“Long-Tailed Distributions”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#LongTailedData). The utility of the normal distribution derives from the fact that many statistics _are_ normally distributed in their sampling distribution. Even so, assumptions of normality are generally a last resort, used when empirical probability distributions, or bootstrap distributions, are not available.

![Normal_dist.PNG](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0210.png)

###### Figure 2-10. Normal curve

###### Note

The normal distribution is also referred to as a _Gaussian_ distribution after Carl Friedrich Gauss, a prodigious German mathematician from the late 18th and early 19th centuries. Another name previously used for the normal distribution was the “error” distribution. Statistically speaking, an _error_ is the difference between an actual value and a statistical estimate like the sample mean. For example, the standard deviation (see [“Estimates of Variability”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch01.html#Variability)) is based on the errors from the mean of the data. Gauss’s development of the normal distribution came from his study of the errors of astronomical measurements that were found to be normally distributed.

## Standard Normal and QQ-Plots

A _standard normal_ distribution is one in which the units on the x-axis are expressed in terms of standard deviations away from the mean. To compare data to a standard normal distribution, you subtract the mean and then divide by the standard deviation; this is also called _normalization_ or _standardization_ (see [“Standardization (Normalization, z-Scores)”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch06.html#Standardization)). Note that “standardization” in this sense is unrelated to database record standardization (conversion to a common format). The transformed value is termed a _z-score_, and the normal distribution is sometimes called the _z-distribution_.

A _QQ-Plot_ is used to visually determine how close a sample is to a specified distribution—in this case, the normal distribution. The QQ-Plot orders the _z_-scores from low to high and plots each value’s _z_-score on the y-axis; the x-axis is the corresponding quantile of a normal distribution for that value’s rank. Since the data is normalized, the units correspond to the number of standard deviations away from the mean. If the points roughly fall on the diagonal line, then the sample distribution can be considered close to normal. [Figure 2-11](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#qqnorm) shows a QQ-Plot for a sample of 100 values randomly generated from a normal distribution; as expected, the points closely follow the line. This figure can be produced in _R_ with the `qqnorm` function:

```
norm_samp
```

In _Python_, use the method `scipy.stats.probplot` to create the QQ-Plot:

```
fig
```

![qqnorm.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0211.png)

###### Figure 2-11. QQ-Plot of a sample of 100 values drawn from a standard normal distribution

###### Warning

Converting data to _z_-scores (i.e., standardizing or normalizing the data) does _not_ make the data normally distributed. It just puts the data on the same scale as the standard normal distribution, often for comparison purposes.

##### Key Ideas

- The normal distribution was essential to the historical development of statistics, as it permitted mathematical approximation of uncertainty and variability.
    
- While raw data is typically not normally distributed, errors often are, as are averages and totals in large samples.
    
- To convert data to _z_-scores, you subtract the mean of the data and divide by the standard deviation; you can then compare the data to a normal distribution.
    

# Long-Tailed Distributions

Despite the importance of the normal distribution historically in statistics, and in contrast to what the name would suggest, data is generally not normally distributed.

##### Key Terms for Long-Tailed Distributions

**_Tail_**

The long narrow portion of a frequency distribution, where relatively extreme values occur at low frequency.

**_Skew_**

Where one tail of a distribution is longer than the other.

While the normal distribution is often appropriate and useful with respect to the distribution of errors and sample statistics, it typically does not characterize the distribution of raw data. Sometimes, the distribution is highly _skewed_ (asymmetric), such as with income data; or the distribution can be discrete, as with binomial data. Both symmetric and asymmetric distributions may have _long tails_. The tails of a distribution correspond to the extreme values (small and large). Long tails, and guarding against them, are widely recognized in practical work. Nassim Taleb has proposed the _black swan_ theory, which predicts that anomalous events, such as a stock market crash, are much more likely to occur than would be predicted by the normal distribution.

A good example to illustrate the long-tailed nature of data is stock returns. [Figure 2-12](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#nflx_qnorm) shows the QQ-Plot for the daily stock returns for Netflix (NFLX). This is generated in _R_ by:

```
nflx
```

The corresponding _Python_ code is:

```
nflx
```

![nflx_qnorm.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0212.png)

###### Figure 2-12. QQ-Plot of the returns for Netflix (NFLX)

In contrast to [Figure 2-11](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#qqnorm), the points are far below the line for low values and far above the line for high values, indicating the data are not normally distributed. This means that we are much more likely to observe extreme values than would be expected if the data had a normal distribution. [Figure 2-12](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#nflx_qnorm) shows another common phenomenon: the points are close to the line for the data within one standard deviation of the mean. Tukey refers to this phenomenon as data being “normal in the middle” but having much longer tails (see [[Tukey-1987]](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/bibliography01.html#Tukey-1987)).

###### Note

There is much statistical literature about the task of fitting statistical distributions to observed data. Beware an excessively data-centric approach to this job, which is as much art as science. Data is variable, and often consistent, on its face, with more than one shape and type of distribution. It is typically the case that domain and statistical knowledge must be brought to bear to determine what type of distribution is appropriate to model a given situation. For example, we might have data on the level of internet traffic on a server over many consecutive five-second periods. It is useful to know that the best distribution to model “events per time period” is the Poisson (see [“Poisson Distributions”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#Poisson)).

##### Key Ideas

- Most data is not normally distributed.
    
- Assuming a normal distribution can lead to underestimation of extreme events (“black swans”).
    

## Further Reading

- _The Black Swan_, 2nd ed., by Nassim Nicholas Taleb (Random House, 2010)
    
- _Handbook of Statistical Distributions with Applications_, 2nd ed., by K. Krishnamoorthy (Chapman & Hall/CRC Press, 2016)
    

# Student’s t-Distribution

The _t-distribution_ is a normally shaped distribution, except that it is a bit thicker and longer on the tails. It is used extensively in depicting distributions of sample statistics. Distributions of sample means are typically shaped like a t-distribution, and there is a family of t-distributions that differ depending on how large the sample is. The larger the sample, the more normally shaped the t-distribution becomes.

##### Key Terms for Student’s t-Distribution

**_n_**

Sample size.

**_Degrees of freedom_**

A parameter that allows the t-distribution to adjust to different sample sizes, statistics, and numbers of groups.

The t-distribution is often called _Student’s t_ because it was published in 1908 in _Biometrika_ by W. S. Gosset under the name “Student.” Gosset’s employer, the Guinness brewery, did not want competitors to know that it was using statistical methods, so it insisted that Gosset not use his name on the article.

Gosset wanted to answer the question “What is the sampling distribution of the mean of a sample, drawn from a larger population?” He started out with a resampling experiment—drawing random samples of 4 from a data set of 3,000 measurements of criminals’ height and left-middle-finger length. (This being the era of eugenics, there was much interest in data on criminals, and in discovering correlations between criminal tendencies and physical or psychological attributes.) Gosset plotted the standardized results (the _z_-scores) on the x-axis and the frequency on the y-axis. Separately, he had derived a function, now known as _Student’s t_, and he fit this function over the sample results, plotting the comparison (see [Figure 2-13](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#Gosset-curve)).

![Gosset-curve](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0213.png)

###### Figure 2-13. Gosset’s resampling experiment results and fitted t-curve (from his 1908 _Biometrika_ paper)

A number of different statistics can be compared, after standardization, to the t-distribution, to estimate confidence intervals in light of sampling variation. Consider a sample of size _n_ for which the sample mean  has been calculated. If _s_ is the sample standard deviation, a 90% confidence interval around the sample mean is given by:

where  is the value of the t-statistic, with (_n_ – 1) degrees of freedom (see [“Degrees of Freedom”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#DOF)), that “chops off” 5% of the t-distribution at either end. The t-distribution has been used as a reference for the distribution of a sample mean, the difference between two sample means, regression parameters, and other statistics.

Had computing power been widely available in 1908, statistics would no doubt have relied much more heavily on computationally intensive resampling methods from the start. Lacking computers, statisticians turned to mathematics and functions such as the t-distribution to approximate sampling distributions. Computer power enabled practical resampling experiments in the 1980s, but by then, use of the t-distribution and similar distributions had become deeply embedded in textbooks and software.

The t-distribution’s accuracy in depicting the behavior of a sample statistic requires that the distribution of that statistic for that sample be shaped like a normal distribution. It turns out that sample statistics _are_ often normally distributed, even when the underlying population data is not (a fact which led to widespread application of the t-distribution). This brings us back to the phenomenon known as the _central limit theorem_ (see [“Central Limit Theorem”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#central-limit-theorem)).

###### Note

What do data scientists need to know about the t-distribution and the central limit theorem? Not a whole lot. The t-distribution is used in classical statistical inference but is not as central to the purposes of data science. Understanding and quantifying uncertainty and variation are important to data scientists, but empirical bootstrap sampling can answer most questions about sampling error. However, data scientists will routinely encounter t-statistics in output from statistical software and statistical procedures in _R_—for example, in A/B tests and regressions—so familiarity with its purpose is helpful.

##### Key Ideas

- The t-distribution is actually a family of distributions resembling the normal distribution but with thicker tails.
    
- The t-distribution is widely used as a reference basis for the distribution of sample means, differences between two sample means, regression parameters, and more.
    

## Further Reading

- The original W.S. Gosset paper as published in _Biometrika_ in 1908 is available [as a PDF](https://oreil.ly/J6gDg).
    
- A standard treatment of the t-distribution can be found in David Lane’s [online resource](https://oreil.ly/QxUkA).
    

# Binomial Distribution

Yes/no (binomial) outcomes lie at the heart of analytics since they are often the culmination of a decision or other process; buy/don’t buy, click/don’t click, survive/die, and so on. Central to understanding the binomial distribution is the idea of a set of _trials_, each trial having two possible outcomes with definite probabilities.

For example, flipping a coin 10 times is a binomial experiment with 10 trials, each trial having two possible outcomes (heads or tails); see [Figure 2-14](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#nickel). Such yes/no or 0/1 outcomes are termed _binary_ outcomes, and they need not have 50/50 probabilities. Any probabilities that sum to 1.0 are possible. It is conventional in statistics to term the “1” outcome the _success_ outcome; it is also common practice to assign “1” to the more rare outcome. Use of the term _success_ does not imply that the outcome is desirable or beneficial, but it does tend to indicate the outcome of interest. For example, loan defaults or fraudulent transactions are relatively uncommon events that we may be interested in predicting, so they are termed “1s” or “successes.”

![images/Indian_Head_Buffalo_Nickel.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0214.png)

###### Figure 2-14. The tails side of a buffalo nickel

##### Key Terms for Binomial Distribution

**_Trial_**

An event with a discrete outcome (e.g., a coin flip).

**_Success_**

The outcome of interest for a trial.

Synonym

“1” (as opposed to “0”)

**_Binomial_**

Having two outcomes.

Synonyms

yes/no, 0/1, binary

**_Binomial trial_**

A trial with two outcomes.

Synonym

Bernoulli trial

**_Binomial distribution_**

Distribution of number of successes in _x_ trials.

Synonym

Bernoulli distribution

The binomial distribution is the frequency distribution of the number of successes (_x_) in a given number of trials (_n_) with specified probability (_p_) of success in each trial. There is a family of binomial distributions, depending on the values of _n_ and _p_. The binomial distribution would answer a question like:

> If the probability of a click converting to a sale is 0.02, what is the probability of observing 0 sales in 200 clicks?

The _R_ function `dbinom` calculates binomial probabilities. For example:

```
dbinom
```

would return 0.0729, the probability of observing exactly _x_ = 2 successes in _size_ = 5 trials, where the probability of success for each trial is _p_ = 0.1. For our example above, we use _x_ = 0, _size_ = 200, and _p_ = 0.02. With these arguments, `dbinom` returns a probability of 0.0176.

Often we are interested in determining the probability of _x_ or fewer successes in _n_ trials. In this case, we use the function `pbinom`:

```
pbinom
```

This would return 0.9914, the probability of observing two or fewer successes in five trials, where the probability of success for each trial is 0.1.

The `scipy.stats` module implements a large variety of statistical distributions. For the binomial distribution, use the functions `stats.binom.pmf` and `stats.binom.cdf`:

```
stats
```

The mean of a binomial distribution is ; you can also think of this as the expected number of successes in _n_ trials, for success probability = _p_.

The variance is . With a large enough number of trials (particularly when _p_ is close to 0.50), the binomial distribution is virtually indistinguishable from the normal distribution. In fact, calculating binomial probabilities with large sample sizes is computationally demanding, and most statistical procedures use the normal distribution, with mean and variance, as an approximation.

##### Key Ideas

- Binomial outcomes are important to model, since they represent, among other things, fundamental decisions (buy or don’t buy, click or don’t click, survive or die, etc.).
    
- A binomial trial is an experiment with two possible outcomes: one with probability _p_ and the other with probability _1 – p_.
    
- With large _n_, and provided _p_ is not too close to 0 or 1, the binomial distribution can be approximated by the normal distribution.
    

## Further Reading

- Read about [the “quincunx”](https://oreil.ly/nmkcs), a pinball-like simulation device for illustrating the binomial distribution.
    
- The binomial distribution is a staple of introductory statistics, and all introductory statistics texts will have a chapter or two on it.
    

# Chi-Square Distribution

An important idea in statistics is _departure from expectation_, especially with respect to category counts. Expectation is defined loosely as “nothing unusual or of note in the data” (e.g., no correlation between variables or predictable patterns). This is also termed the “null hypothesis” or “null model” (see [“The Null Hypothesis”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Null_hypothesis)). For example, you might want to test whether one variable (say, a row variable representing gender) is independent of another (say, a column variable representing “was promoted in job”), and you have counts of the number in each of the cells of the data table. The statistic that measures the extent to which results depart from the null expectation of independence is the chi-square statistic. It is the difference between the observed and expected values, divided by the square root of the expected value, squared, then summed across all categories. This process standardizes the statistic so it can be compared to a reference distribution. A more general way of putting this is to note that the chi-square statistic is a measure of the extent to which a set of observed values “fits” a specified distribution (a “goodness-of-fit” test). It is useful for determining whether multiple treatments (an “A/B/C… test”) differ from one another in their effects.

The chi-square distribution is the distribution of the chi-square statistic under repeated resampled draws from the null model—see [“Chi-Square Test”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#chi-square) for a detailed algorithm, and the chi-square formula for a data table. A low chi-square value for a set of counts indicates that they closely follow the expected distribution. A high chi-square indicates that they differ markedly from what is expected. There are a variety of chi-square distributions associated with different degrees of freedom (e.g., number of observations—see [“Degrees of Freedom”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#DOF)).

##### Key Ideas

- The chi-square distribution is typically concerned with counts of subjects or items falling into categories.
    
- The chi-square statistic measures the extent of departure from what you would expect in a null model.
    

## Further Reading

- The chi-square distribution owes its place in modern statistics to the great statistician Karl Pearson and the birth of hypothesis testing—read about this and more in David Salsburg’s _The Lady Tasting Tea: How Statistics Revolutionized Science in the Twentieth Century_ (W. H. Freeman, 2001).
    
- For a more detailed exposition, see the section in this book on the chi-square test ([“Chi-Square Test”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#chi-square)).
    

# F-Distribution

A common procedure in scientific experimentation is to test multiple treatments across groups—say, different fertilizers on different blocks of a field. This is similar to the A/B/C test referred to in the chi-square distribution (see [“Chi-Square Distribution”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#chi-square-dist)), except we are dealing with measured continuous values rather than counts. In this case we are interested in the extent to which differences among group means are greater than we might expect under normal random variation. The F-statistic measures this and is the ratio of the variability among the group means to the variability within each group (also called residual variability). This comparison is termed an _analysis of variance_ (see [“ANOVA”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#ANOVA)). The distribution of the F-statistic is the frequency distribution of all the values that would be produced by randomly permuting data in which all the group means are equal (i.e., a null model). There are a variety of F-distributions associated with different degrees of freedom (e.g., numbers of groups—see [“Degrees of Freedom”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#DOF)). The calculation of F is illustrated in the section on ANOVA. The F-statistic is also used in linear regression to compare the variation accounted for by the regression model to the overall variation in the data. F-statistics are produced automatically by _R_ and _Python_ as part of regression and ANOVA routines.

##### Key Ideas

- The F-distribution is used with experiments and linear models involving measured data.
    
- The F-statistic compares variation due to factors of interest to overall variation.
    

## Further Reading

George Cobb’s _Introduction to Design and Analysis of Experiments_ (Wiley, 2008) contains an excellent exposition of the decomposition of variance components, which helps in understanding ANOVA and the F-statistic.

# Poisson and Related Distributions

Many processes produce events randomly at a given overall rate—visitors arriving at a website, or cars arriving at a toll plaza (events spread over time); imperfections in a square meter of fabric, or typos per 100 lines of code (events spread over space).

##### Key Terms for Poisson and Related Distributions

**_Lambda_**

The rate (per unit of time or space) at which events occur.

**_Poisson distribution_**

The frequency distribution of the number of events in sampled units of time or space.

**_Exponential distribution_**

The frequency distribution of the time or distance from one event to the next event.

**_Weibull distribution_**

A generalized version of the exponential distribution in which the event rate is allowed to shift over time.

## Poisson Distributions

From prior aggregate data (for example, number of flu infections per year), we can estimate the average number of events per unit of time or space (e.g., infections per day, or per census unit). We might also want to know how different this might be from one unit of time/space to another. The Poisson distribution tells us the distribution of events per unit of time or space when we sample many such units. It is useful when addressing queuing questions such as “How much capacity do we need to be 95% sure of fully processing the internet traffic that arrives on a server in any five-second period?”

The key parameter in a Poisson distribution is , or lambda. This is the mean number of events that occurs in a specified interval of time or space. The variance for a Poisson distribution is also .

A common technique is to generate random numbers from a Poisson distribution as part of a queuing simulation. The `rpois` function in _R_ does this, taking only two arguments—the quantity of random numbers sought, and lambda:

```
rpois
```

The corresponding `scipy` function is `stats.poisson.rvs`:

```
stats
```

This code will generate 100 random numbers from a Poisson distribution with  = 2. For example, if incoming customer service calls average two per minute, this code will simulate 100 minutes, returning the number of calls in each of those 100 minutes.

## Exponential Distribution

Using the same parameter  that we used in the Poisson distribution, we can also model the distribution of the time between events: time between visits to a website or between cars arriving at a toll plaza. It is also used in engineering to model time to failure, and in process management to model, for example, the time required per service call. The _R_ code to generate random numbers from an exponential distribution takes two arguments: `n` (the quantity of numbers to be generated) and `rate` (the number of events per time period). For example:

```
rexp
```

The `scipy` implementation in `Python` specifies the exponential distribution using `scale` instead of rate. With scale being the inverse of rate, the corresponding command in Python is:

```
stats
```

This code would generate 100 random numbers from an exponential distribution where the mean number of events per time period is 0.2. So you could use it to simulate 100 intervals, in minutes, between service calls, where the average rate of incoming calls is 0.2 per minute.

A key assumption in any simulation study for either the Poisson or exponential distribution is that the rate, , remains constant over the period being considered. This is rarely reasonable in a global sense; for example, traffic on roads or data networks varies by time of day and day of week. However, the time periods, or areas of space, can usually be divided into segments that are sufficiently homogeneous so that analysis or simulation within those periods is valid.

## Estimating the Failure Rate

In many applications, the event rate, , is known or can be estimated from prior data. However, for rare events, this is not necessarily so. Aircraft engine failure, for example, is sufficiently rare (thankfully) that, for a given engine type, there may be little data on which to base an estimate of time between failures. With no data at all, there is little basis on which to estimate an event rate. However, you can make some guesses: if no events have been seen after 20 hours, you can be pretty sure that the rate is not 1 per hour. Via simulation, or direct calculation of probabilities, you can assess different hypothetical event rates and estimate threshold values below which the rate is very unlikely to fall. If there is some data but not enough to provide a precise, reliable estimate of the rate, a goodness-of-fit test (see [“Chi-Square Test”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#chi-square)) can be applied to various rates to determine how well they fit the observed data.

## Weibull Distribution

In many cases, the event rate does not remain constant over time. If the period over which it changes is much longer than the typical interval between events, there is no problem; you just subdivide the analysis into the segments where rates are relatively constant, as mentioned before. If, however, the event rate changes over the time of the interval, the exponential (or Poisson) distributions are no longer useful. This is likely to be the case in mechanical failure—the risk of failure increases as time goes by. The _Weibull_ distribution is an extension of the exponential distribution in which the event rate is allowed to change, as specified by a _shape parameter_, . If  > 1, the probability of an event increases over time; if  < 1, the probability decreases. Because the Weibull distribution is used with time-to-failure analysis instead of event rate, the second parameter is expressed in terms of characteristic life, rather than in terms of the rate of events per interval. The symbol used is , the Greek letter eta. It is also called the _scale_ parameter.

With the Weibull, the estimation task now includes estimation of both parameters,  and . Software is used to model the data and yield an estimate of the best-fitting Weibull distribution.

The _R_ code to generate random numbers from a Weibull distribution takes three arguments: `n` (the quantity of numbers to be generated), `shape`, and `scale`. For example, the following code would generate 100 random numbers (lifetimes) from a Weibull distribution with shape of 1.5 and characteristic life of 5,000:

```
rweibull
```

To achieve the same in _Python_, use the function `stats.weibull_min.rvs`:

```
stats
```

##### Key Ideas

- For events that occur at a constant rate, the number of events per unit of time or space can be modeled as a Poisson distribution.
    
- You can also model the time or distance between one event and the next as an exponential distribution.
    
- A changing event rate over time (e.g., an increasing probability of device failure) can be modeled with the Weibull distribution.
    

## Further Reading

- _Modern Engineering Statistics_ by Thomas Ryan (Wiley, 2007) has a chapter devoted to the probability distributions used in engineering applications.
    
- Read an engineering-based perspective on the use of the Weibull distribution [here](https://oreil.ly/1x-ga) and [here](https://oreil.ly/9bn-U).
    

# Summary

In the era of big data, the principles of random sampling remain important when accurate estimates are needed. Random selection of data can reduce bias and yield a higher quality data set than would result from just using the conveniently available data. Knowledge of various sampling and data-generating distributions allows us to quantify potential errors in an estimate that might be due to random variation. At the same time, the bootstrap (sampling with replacement from an observed data set) is an attractive “one size fits all” method to determine possible error in sample estimates.

[1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#idm45782047495336-marker) The bell curve is iconic but perhaps overrated. George W. Cobb, the Mount Holyoke statistician noted for his contribution to the philosophy of teaching introductory statistics, argued in a November 2015 editorial in the _American Statistician_ that the “standard introductory course, which puts the normal distribution at its center, had outlived the usefulness of its centrality.”
Design of experiments is a cornerstone of the practice of statistics, with applications in virtually all areas of research. The goal is to design an experiment in order to confirm or reject a hypothesis. Data scientists often need to conduct continual experiments, particularly regarding user interface and product marketing. This chapter reviews traditional experimental design and discusses some common challenges in data science. It also covers some oft-cited concepts in statistical inference and explains their meaning and relevance (or lack of relevance) to data science.

Whenever you see references to statistical significance, t-tests, or p-values, it is typically in the context of the classical statistical inference “pipeline” (see [Figure 3-1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#fig0301)). This process starts with a hypothesis (“drug A is better than the existing standard drug,” or “price A is more profitable than the existing price B”). An experiment (it might be an A/B test) is designed to test the hypothesis—designed in such a way that it hopefully will deliver conclusive results. The data is collected and analyzed, and then a conclusion is drawn. The term _inference_ reflects the intention to apply the experiment results, which involve a limited set of data, to a larger process or population.

![images/Inference-pipeline.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0301.png)

###### Figure 3-1. The classical statistical inference pipeline

# A/B Testing

An A/B test is an experiment with two groups to establish which of two treatments, products, procedures, or the like is superior. Often one of the two treatments is the standard existing treatment, or no treatment. If a standard (or no) treatment is used, it is called the _control_. A typical hypothesis is that a new treatment is better than the control.

##### Key Terms for A/B Testing

**_Treatment_**

Something (drug, price, web headline) to which a subject is exposed.

**_Treatment group_**

A group of subjects exposed to a specific treatment.

**_Control group_**

A group of subjects exposed to no (or standard) treatment.

**_Randomization_**

The process of randomly assigning subjects to treatments.

**_Subjects_**

The items (web visitors, patients, etc.) that are exposed to treatments.

**_Test statistic_**

The metric used to measure the effect of the treatment.

A/B tests are common in web design and marketing, since results are so readily measured. Some examples of A/B testing include:

- Testing two soil treatments to determine which produces better seed germination
    
- Testing two therapies to determine which suppresses cancer more effectively
    
- Testing two prices to determine which yields more net profit
    
- Testing two web headlines to determine which produces more clicks ([Figure 3-2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#fig0302))
    
- Testing two web ads to determine which generates more conversions
    

![images/Web-test-A-B.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0302.png)

###### Figure 3-2. Marketers continually test one web presentation against another

A proper A/B test has _subjects_ that can be assigned to one treatment or another. The subject might be a person, a plant seed, a web visitor; the key is that the subject is exposed to the treatment. Ideally, subjects are _randomized_ (assigned randomly) to treatments. In this way, you know that any difference between the treatment groups is due to one of two things:

- The effect of the different treatments
    
- Luck of the draw in which subjects are assigned to which treatments (i.e., the random assignment may have resulted in the naturally better-performing subjects being concentrated in A or B)
    

You also need to pay attention to the _test statistic_ or metric you use to compare group A to group B. Perhaps the most common metric in data science is a binary variable: click or no-click, buy or don’t buy, fraud or no fraud, and so on. Those results would be summed up in a 2×2 table. [Table 3-1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#two_by_two) is a 2×2 table for an actual price test (see [“Statistical Significance and p-Values”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Significance) for further discussion of these results).

Table 3-1. 2×2 table for ecommerce experiment results
|Outcome|Price A|Price B|
|---|---|---|
|Conversion|200|182|
|No conversion|23,539|22,406|

If the metric is a continuous variable (purchase amount, profit, etc.) or a count (e.g., days in hospital, pages visited), the result might be displayed differently. If one were interested not in conversion but in revenue per page view, the results of the price test in [Table 3-1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#two_by_two) might look like this in typical default software output:

> Revenue/page view with price A: mean = 3.87, SD = 51.10
> 
> Revenue/page view with price B: mean = 4.11, SD = 62.98

“SD” refers to the standard deviation of the values within each group.

###### Warning

Just because statistical software—including _R_ and _Python_—generates output by default does not mean that all the output is useful or relevant. You can see that the preceding standard deviations are not that useful; on their face they suggest that numerous values might be negative, when negative revenue is not feasible. This data consists of a small set of relatively high values (page views with conversions) and a huge number of 0-values (page views with no conversion). It is difficult to sum up the variability of such data with a single number, though the mean absolute deviation from the mean (7.68 for A and 8.15 for B) is more reasonable than the standard deviation.

## Why Have a Control Group?

Why not skip the control group and just run an experiment applying the treatment of interest to only one group, and compare the outcome to prior experience?

Without a control group, there is no assurance that “all other things are equal” and that any difference is really due to the treatment (or to chance). When you have a control group, it is subject to the same conditions (except for the treatment of interest) as the treatment group. If you simply make a comparison to “baseline” or prior experience, other factors, besides the treatment, might differ.

# Blinding in studies

A _blind study_ is one in which the subjects are unaware of whether they are getting treatment A or treatment B. Awareness of receiving a particular treatment can affect response. A _double-blind_ study is one in which the investigators and facilitators (e.g., doctors and nurses in a medical study) also are unaware which subjects are getting which treatment. Blinding is not possible when the nature of the treatment is transparent—for example, cognitive therapy from a computer versus a psychologist.

A/B testing in data science is typically used in a web context. Treatments might be the design of a web page, the price of a product, the wording of a headline, or some other item. Some thought is required to preserve the principles of randomization. Typically the subject in the experiment is the web visitor, and the outcomes we are interested in measuring are clicks, purchases, visit duration, number of pages visited, whether a particular page is visited, and the like. In a standard A/B experiment, you need to decide on one metric ahead of time. Multiple behavior metrics might be collected and be of interest, but if the experiment is expected to lead to a decision between treatment A and treatment B, a single metric, or _test statistic_, needs to be established beforehand. Selecting a test statistic _after_ the experiment is conducted opens the door to researcher bias.

## Why Just A/B? Why Not C, D,…?

A/B tests are popular in the marketing and ecommerce worlds, but are far from the only type of statistical experiment. Additional treatments can be included. Subjects might have repeated measurements taken. Pharmaceutical trials where subjects are scarce, expensive, and acquired over time are sometimes designed with multiple opportunities to stop the experiment and reach a conclusion.

Traditional statistical experimental designs focus on answering a static question about the efficacy of specified treatments. Data scientists are less interested in the question:

> Is the difference between price A and price B statistically significant?

than in the question:

> Which, out of multiple possible prices, is best?

For this, a relatively new type of experimental design is used: the _multi-arm bandit_ (see [“Multi-Arm Bandit Algorithm”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#bandits)).

# Getting Permission

In scientific and medical research involving human subjects, it is typically necessary to get their permission, as well as obtain the approval of an institutional review board. Experiments in business that are done as a part of ongoing operations almost never do this. In most cases (e.g., pricing experiments, or experiments about which headline to show or which offer should be made), this practice is widely accepted. Facebook, however, ran afoul of this general acceptance in 2014 when it experimented with the emotional tone in users’ newsfeeds. Facebook used sentiment analysis to classify newsfeed posts as positive or negative, and then altered the positive/negative balance in what it showed users. Some randomly selected users experienced more positive posts, while others experienced more negative posts. Facebook found that the users who experienced a more positive newsfeed were more likely to post positively themselves, and vice versa. The magnitude of the effect was small, however, and Facebook faced much criticism for conducting the experiment without users’ knowledge. Some users speculated that Facebook might have pushed some extremely depressed users over the edge if they got the negative version of their feed.

##### Key Ideas

- Subjects are assigned to two (or more) groups that are treated exactly alike, except that the treatment under study differs from one group to another.
    
- Ideally, subjects are assigned randomly to the groups.
    

## Further Reading

- Two-group comparisons (A/B tests) are a staple of traditional statistics, and just about any introductory statistics text will have extensive coverage of design principles and inference procedures. For a discussion that places A/B tests in more of a data science context and uses resampling, see _Introductory Statistics and Analytics: A Resampling Perspective_ by Peter Bruce (Wiley, 2014).
    
- For web testing, the logistical aspects of testing can be just as challenging as the statistical ones. A good place to start is the [Google Analytics help section on experiments](https://oreil.ly/mAbqF).
    
- Beware advice found in the ubiquitous guides to A/B testing that you see on the web, such as these words in one such guide: “Wait for about 1,000 total visitors and make sure you run the test for a week.” Such general rules of thumb are not statistically meaningful; see [“Power and Sample Size”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#PowerSampleSize) for more detail.
    

# Hypothesis Tests

Hypothesis tests, also called _significance tests_, are ubiquitous in the traditional statistical analysis of published research. Their purpose is to help you learn whether random chance might be responsible for an observed effect.

##### Key Terms for Hypothesis Tests

**_Null hypothesis_**

The hypothesis that chance is to blame.

**_Alternative hypothesis_**

Counterpoint to the null (what you hope to prove).

**_One-way test_**

Hypothesis test that counts chance results only in one direction.

**_Two-way test_**

Hypothesis test that counts chance results in two directions.

An A/B test (see [“A/B Testing”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#A-B-test)) is typically constructed with a hypothesis in mind. For example, the hypothesis might be that price B produces higher profit. Why do we need a hypothesis? Why not just look at the outcome of the experiment and go with whichever treatment does better?

The answer lies in the tendency of the human mind to underestimate the scope of natural random behavior. One manifestation of this is the failure to anticipate extreme events, or so-called “black swans” (see [“Long-Tailed Distributions”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#LongTailedData)). Another manifestation is the tendency to misinterpret random events as having patterns of some significance. Statistical hypothesis testing was invented as a way to protect researchers from being fooled by random chance.

##### Misinterpreting Randomness

You can observe the human tendency to underestimate randomness in this experiment. Ask several friends to invent a series of 50 coin flips: have them write down a series of random Hs and Ts. Then ask them to actually flip a coin 50 times and write down the results. Have them put the real coin flip results in one pile, and the made-up results in another. It is easy to tell which results are real: the real ones will have longer runs of Hs or Ts. In a set of 50 _real_ coin flips, it is not at all unusual to see five or six Hs or Ts in a row. However, when most of us are inventing random coin flips and we have gotten three or four Hs in a row, we tell ourselves that, for the series to look random, we had better switch to T.

The other side of this coin, so to speak, is that when we _do_ see the real-world equivalent of six Hs in a row (e.g., when one headline outperforms another by 10%), we are inclined to attribute it to something real, not just to chance.

In a properly designed A/B test, you collect data on treatments A and B in such a way that any observed difference between A and B must be due to either:

- Random chance in assignment of subjects
    
- A true difference between A and B
    

A statistical hypothesis test is further analysis of an A/B test, or any randomized experiment, to assess whether random chance is a reasonable explanation for the observed difference between groups A and B.

## The Null Hypothesis

Hypothesis tests use the following logic: “Given the human tendency to react to unusual but random behavior and interpret it as something meaningful and real, in our experiments we will require proof that the difference between groups is more extreme than what chance might reasonably produce.” This involves a baseline assumption that the treatments are equivalent, and any difference between the groups is due to chance. This baseline assumption is termed the _null hypothesis_. Our hope, then, is that we can in fact prove the null hypothesis _wrong_ and show that the outcomes for groups A and B are more different than what chance might produce.

One way to do this is via a resampling permutation procedure, in which we shuffle together the results from groups A and B and then repeatedly deal out the data in groups of similar sizes, and then observe how often we get a difference as extreme as the observed difference. The combined shuffled results from groups A and B, and the procedure of resampling from them, embodies the null hypothesis of groups A and B being equivalent and interchangeable and is termed the null model. See [“Resampling”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Resampling) for more detail.

## Alternative Hypothesis

Hypothesis tests by their nature involve not just a null hypothesis but also an offsetting alternative hypothesis. Here are some examples:

- Null = “no difference between the means of group A and group B”; alternative = “A is different from B” (could be bigger or smaller)
    
- Null = “A  B”; alternative = “A > B”
    
- Null = “B is not X% greater than A”; alternative = “B is X% greater than A”
    

Taken together, the null and alternative hypotheses must account for all possibilities. The nature of the null hypothesis determines the structure of the hypothesis test.

## One-Way Versus Two-Way Hypothesis Tests

Often in an A/B test, you are testing a new option (say, B) against an established default option (A), and the presumption is that you will stick with the default option unless the new option proves itself definitively better. In such a case, you want a hypothesis test to protect you from being fooled by chance in the direction favoring B. You don’t care about being fooled by chance in the other direction, because you would be sticking with A unless B proves definitively better. So you want a _directional_ alternative hypothesis (B is better than A). In such a case, you use a _one-way_ (or one-tail) hypothesis test. This means that extreme chance results in only one direction count toward the p-value.

If you want a hypothesis test to protect you from being fooled by chance in either direction, the alternative hypothesis is _bidirectional_ (A is different from B; could be bigger or smaller). In such a case, you use a _two-way_ (or two-tail) hypothesis. This means that extreme chance results in either direction count toward the p-value.

A one-tail hypothesis test often fits the nature of A/B decision making, in which a decision is required and one option is typically assigned “default” status unless the other proves better. Software, however, including _R_ and `scipy` in _Python_, typically provides a two-tail test in its default output, and many statisticians opt for the more conservative two-tail test just to avoid argument. One-tail versus two-tail is a confusing subject, and not that relevant for data science, where the precision of p-value calculations is not terribly important.

##### Key Ideas

- A null hypothesis is a logical construct embodying the notion that nothing special has happened, and any effect you observe is due to random chance.
    
- The hypothesis test assumes that the null hypothesis is true, creates a “null model” (a probability model), and tests whether the effect you observe is a reasonable outcome of that model.
    

## Further Reading

- _The Drunkard’s Walk_ by Leonard Mlodinow (Pantheon, 2008) is a readable survey of the ways in which “randomness rules our lives.”
    
- David Freedman, Robert Pisani, and Roger Purves’s classic statistics text _Statistics_, 4th ed. (W. W. Norton, 2007), has excellent nonmathematical treatments of most statistics topics, including hypothesis testing.
    
- _Introductory Statistics and Analytics: A Resampling Perspective_ by Peter Bruce (Wiley, 2014) develops hypothesis testing concepts using resampling.
    

# Resampling

_Resampling_ in statistics means to repeatedly sample values from observed data, with a general goal of assessing random variability in a statistic. It can also be used to assess and improve the accuracy of some machine-learning models (e.g., the predictions from decision tree models built on multiple bootstrapped data sets can be averaged in a process known as _bagging_—see [“Bagging and the Random Forest”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch06.html#Bagging)).

There are two main types of resampling procedures: the _bootstrap_ and _permutation_ tests. The bootstrap is used to assess the reliability of an estimate; it was discussed in the previous chapter (see [“The Bootstrap”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#bootstrap)). Permutation tests are used to test hypotheses, typically involving two or more groups, and we discuss those in this section.

##### Key Terms for Resampling

**_Permutation test_**

The procedure of combining two or more samples together and randomly (or exhaustively) reallocating the observations to resamples.

_Synonyms_

Randomization test, random permutation test, exact test

**_Resampling_**

Drawing additional samples (“resamples”) from an observed data set.

**_With or without replacement_**

In sampling, whether or not an item is returned to the sample before the next draw.

## Permutation Test

In a _permutation_ procedure, two or more samples are involved, typically the groups in an A/B or other hypothesis test. _Permute_ means to change the order of a set of values. The first step in a _permutation test_ of a hypothesis is to combine the results from groups A and B (and, if used, C, D,…). This is the logical embodiment of the null hypothesis that the treatments to which the groups were exposed do not differ. We then test that hypothesis by randomly drawing groups from this combined set and seeing how much they differ from one another. The permutation procedure is as follows:

1. Combine the results from the different groups into a single data set.
    
2. Shuffle the combined data and then randomly draw (without replacement) a resample of the same size as group A (clearly it will contain some data from the other groups).
    
3. From the remaining data, randomly draw (without replacement) a resample of the same size as group B.
    
4. Do the same for groups C, D, and so on. You have now collected one set of resamples that mirror the sizes of the original samples.
    
5. Whatever statistic or estimate was calculated for the original samples (e.g., difference in group proportions), calculate it now for the resamples, and record; this constitutes one permutation iteration.
    
6. Repeat the previous steps _R_ times to yield a permutation distribution of the test statistic.
    

Now go back to the observed difference between groups and compare it to the set of permuted differences. If the observed difference lies well within the set of permuted differences, then we have not proven anything—the observed difference is within the range of what chance might produce. However, if the observed difference lies outside most of the permutation distribution, then we conclude that chance is _not_ responsible. In technical terms, the difference is _statistically significant_. (See [“Statistical Significance and p-Values”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Significance).)

## Example: Web Stickiness

A company selling a relatively high-value service wants to test which of two web presentations does a better selling job. Due to the high value of the service being sold, sales are infrequent and the sales cycle is lengthy; it would take too long to accumulate enough sales to know which presentation is superior. So the company decides to measure the results with a proxy variable, using the detailed interior page that describes the service.

###### Tip

A _proxy_ variable is one that stands in for the true variable of interest, which may be unavailable, too costly, or too time-consuming to measure. In climate research, for example, the oxygen content of ancient ice cores is used as a proxy for temperature. It is useful to have at least _some_ data on the true variable of interest, so the strength of its association with the proxy can be assessed.

One potential proxy variable for our company is the number of clicks on the detailed landing page. A better one is how long people spend on the page. It is reasonable to think that a web presentation (page) that holds people’s attention longer will lead to more sales. Hence, our metric is average time on the page, comparing page A to page B.

Due to the fact that this is an interior, special-purpose page, it does not receive a huge number of visitors. Also note that Google Analytics, which is how we measure average time on page, cannot measure the time spent on the last page within a session. Google Analytics will set the time spent on the last page in a session to zero, unless the user interacts with the page (e.g., clicks or scrolls). This is also the case for single-page sessions. The data requires additional processing to take this into account. The result is a total of 36 times for the two different presentations, 21 for page A and 15 for page B. Using `ggplot`, we can visually compare the times using side-by-side boxplots (we call these page times “session_times” in the code, though that has a slightly different meaning for Google):

```
ggplot
```

The `pandas` `boxplot` command uses the keyword argument `by` to create the figure:

```
ax
```

The boxplot, shown in [Figure 3-3](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#SessionTimesBoxplot), indicates that page B leads to longer sessions than page A. The means for each group can be computed in _R_ as follows:

```
mean_a
```

In _Python_, we filter the `pandas` data frame first by page and then determine the mean of the `Time` column:

```
mean_a
```

Page B has times that are greater than those of page A by 35.67 seconds, on average. The question is whether this difference is within the range of what random chance might produce, i.e., is statistically significant. One way to answer this is to apply a permutation test—combine all the times together and then repeatedly shuffle and divide them into groups of 21 (recall that  for page A) and 15 ( for page B).

To apply a permutation test, we need a function to randomly assign the 36 times to a group of 21 (page A) and a group of 15 (page B). The _R_ version of this function is:

```
perm_fun
```

The _Python_ version of this permutation test is the following:

```
def
```

![Session times for different presentations of a web page.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0303.png)

###### Figure 3-3. Session times for web pages A and B

This function works by sampling (without replacement)  indices and assigning them to the B group; the remaining  indices are assigned to group A. The difference between the two means is returned. Calling this function _R_ = 1,000 times and specifying  and  leads to a distribution of differences in the page times that can be plotted as a histogram. In _R_ this is done as follows using the `hist` function:

```
perm_diffs
```

In _Python_, we can create a similar graph using `matplotlib`:

```
perm_diffs
```

The histogram, in [Figure 3-4](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#SessionTimesPerm) shows that mean difference of random permutations often exceeds the observed difference in times (the vertical line). For our results, this happens in 12.6% of the cases:

```
mean
```

As the simulation uses random numbers, the percentage will vary. For example, in the _Python_ version, we got 12.1%:

```
np
```

This suggests that the observed difference in time between page A and page B is well within the range of chance variation and thus is not statistically significant.

![Histogram of the difference in session times from the permutation procedure.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0304.png)

###### Figure 3-4. Frequency distribution for time differences between pages A and B; the vertical line shows the observed difference

## Exhaustive and Bootstrap Permutation Tests

In addition to the preceding random shuffling procedure, also called a _random permutation test_ or a _randomization test_, there are two variants of the permutation test:

- An _exhaustive permutation test_
    
- A _bootstrap permutation test_
    

In an exhaustive permutation test, instead of just randomly shuffling and dividing the data, we actually figure out all the possible ways it could be divided. This is practical only for relatively small sample sizes. With a large number of repeated shufflings, the random permutation test results approximate those of the exhaustive permutation test, and approach them in the limit. Exhaustive permutation tests are also sometimes called _exact tests_, due to their statistical property of guaranteeing that the null model will not test as “significant” more than the alpha level of the test (see [“Statistical Significance and p-Values”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Significance)).

In a bootstrap permutation test, the draws outlined in steps 2 and 3 of the random permutation test are made _with replacement_ instead of without replacement. In this way the resampling procedure models not just the random element in the assignment of treatment to subject but also the random element in the selection of subjects from a population. Both procedures are encountered in statistics, and the distinction between them is somewhat convoluted and not of consequence in the practice of data science.

## Permutation Tests: The Bottom Line for Data Science

Permutation tests are useful heuristic procedures for exploring the role of random variation. They are relatively easy to code, interpret, and explain, and they offer a useful detour around the formalism and “false determinism” of formula-based statistics, in which the precision of formula “answers” tends to imply unwarranted certainty.

One virtue of resampling, in contrast to formula approaches, is that it comes much closer to a one-size-fits-all approach to inference. Data can be numeric or binary. Sample sizes can be the same or different. Assumptions about normally distributed data are not needed.

##### Key Ideas

- In a permutation test, multiple samples are combined and then shuffled.
    
- The shuffled values are then divided into resamples, and the statistic of interest is calculated.
    
- This process is then repeated, and the resampled statistic is tabulated.
    
- Comparing the observed value of the statistic to the resampled distribution allows you to judge whether an observed difference between samples might occur by chance.
    

## Further Reading

- _Randomization Tests_, 4th ed., by Eugene Edgington and Patrick Onghena (Chapman & Hall/CRC Press, 2007)—but don’t get too drawn into the thicket of nonrandom sampling
    
- _Introductory Statistics and Analytics: A Resampling Perspective_ by Peter Bruce (Wiley, 2014)
    

# Statistical Significance and p-Values

Statistical significance is how statisticians measure whether an experiment (or even a study of existing data) yields a result more extreme than what chance might produce. If the result is beyond the realm of chance variation, it is said to be statistically significant.

##### Key Terms for Statistical Significance and p-Values

**_p-value_**

Given a chance model that embodies the null hypothesis, the p-value is the probability of obtaining results as unusual or extreme as the observed results.

**_Alpha_**

The probability threshold of “unusualness” that chance results must surpass for actual outcomes to be deemed statistically significant.

**_Type 1 error_**

Mistakenly concluding an effect is real (when it is due to chance).

**_Type 2 error_**

Mistakenly concluding an effect is due to chance (when it is real).

Consider in [Table 3-2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#dataframe2) the results of the web test shown earlier.

Table 3-2. 2×2 table for ecommerce experiment results
|Outcome|Price A|Price B|
|---|---|---|
|Conversion|200|182|
|No conversion|23,539|22,406|

Price A converts almost 5% better than price B (0.8425% = 200/(23539+200)*100, versus 0.8057% = 182/(22406+182)*100—a difference of 0.0368 percentage points), big enough to be meaningful in a high-volume business. We have over 45,000 data points here, and it is tempting to consider this as “big data,” not requiring tests of statistical significance (needed mainly to account for sampling variability in small samples). However, the conversion rates are so low (less than 1%) that the actual meaningful values—the conversions—are only in the 100s, and the sample size needed is really determined by these conversions. We can test whether the difference in conversions between prices A and B is within the range of _chance variation_, using a resampling procedure. By chance variation, we mean the random variation produced by a probability model that embodies the null hypothesis that there is no difference between the rates (see [“The Null Hypothesis”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Null_hypothesis)). The following permutation procedure asks, “If the two prices share the same conversion rate, could chance variation produce a difference as big as 5%?”

1. Put cards labeled 1 and 0 in a box: this represents the supposed shared conversion rate of 382 ones and 45,945 zeros = 0.008246 = 0.8246%.
    
2. Shuffle and draw out a resample of size 23,739 (same _n_ as price A), and record how many 1s.
    
3. Record the number of 1s in the remaining 22,588 (same _n_ as price B).
    
4. Record the difference in proportion of 1s.
    
5. Repeat steps 2–4.
    
6. How often was the difference >= 0.0368?
    

Reusing the function `perm_fun` defined in [“Example: Web Stickiness”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#PermutationExample), we can create a histogram of randomly permuted differences in conversion rate in _R_:

```
obs_pct_diff
```

The corresponding _Python_ code is:

```
obs_pct_diff
```

See the histogram of 1,000 resampled results in [Figure 3-5](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#conversion-rates-histogram): as it happens, in this case the observed difference of 0.0368% is well within the range of chance variation.

![Histogram of the difference in conversion rates from the permutation procedure.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0305.png)

###### Figure 3-5. Frequency distribution for the difference in conversion rates between prices A and B

## p-Value

Simply looking at the graph is not a very precise way to measure statistical significance, so of more interest is the _p-value_. This is the frequency with which the chance model produces a result more extreme than the observed result. We can estimate a p-value from our permutation test by taking the proportion of times that the permutation test produces a difference equal to or greater than the observed difference:

```
mean
```

```
np
```

Here, both _R_ and _Python_ use the fact that true is interpreted as 1 and false as 0.

The p-value is 0.308, which means that we would expect to achieve a result as extreme as this, or a more extreme result, by random chance over 30% of the time.

In this case, we didn’t need to use a permutation test to get a p-value. Since we have a binomial distribution, we can approximate the p-value. In _R_ code, we do this using the function `prop.test`:

```
>
```

The argument `x` is the number of successes for each group, and the argument `n` is the number of trials.

The method `scipy.stats.chi2_contingency` takes the values as shown in [Table 3-2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#dataframe2):

```
survivors
```

The normal approximation yields a p-value of 0.3498, which is close to the p-value obtained from the permutation test.

## Alpha

Statisticians frown on the practice of leaving it to the researcher’s discretion to determine whether a result is “too unusual” to happen by chance. Rather, a threshold is specified in advance, as in “more extreme than 5% of the chance (null hypothesis) results”; this threshold is known as _alpha_. Typical alpha levels are 5% and 1%. Any chosen level is an arbitrary decision—there is nothing about the process that will guarantee correct decisions x% of the time. This is because the probability question being answered is _not_ “What is the probability that this happened by chance?” but rather “Given a chance model, what is the probability of a result this extreme?” We then deduce backward about the appropriateness of the chance model, but that judgment does not carry a probability. This point has been the subject of much confusion.

### p-value controversy

Considerable controversy has surrounded the use of the p-value in recent years. One psychology journal has gone so far as to “ban” the use of p-values in submitted papers on the grounds that publication decisions based solely on the p-value were resulting in the publication of poor research. Too many researchers, only dimly aware of what a p-value really means, root around in the data, and among different possible hypotheses to test, until they find a combination that yields a significant p-value and, hence, a paper suitable for publication.

The real problem is that people want more meaning from the p-value than it contains. Here’s what we would _like_ the p-value to convey:

> The probability that the result is due to chance.

We hope for a low value, so we can conclude that we’ve proved something. This is how many journal editors were interpreting the p-value. But here’s what the p-value _actually_ represents:

> The probability that, _given a chance model_, results as extreme as the observed results could occur.

The difference is subtle but real. A significant p-value does not carry you quite as far along the road to “proof” as it seems to promise. The logical foundation for the conclusion “statistically significant” is somewhat weaker when the real meaning of the p-value is understood.

In March 2016, the American Statistical Association, after much internal deliberation, revealed the extent of misunderstanding about p-values when it issued a cautionary statement regarding their use. The [ASA statement](https://oreil.ly/WVfYU) stressed six principles for researchers and journal editors:

> 1. P-values can indicate how incompatible the data are with a specified statistical model.
>     
> 2. P-values do not measure the probability that the studied hypothesis is true, or the probability that the data were produced by random chance alone.
>     
> 3. Scientific conclusions and business or policy decisions should not be based only on whether a p-value passes a specific threshold.
>     
> 4. Proper inference requires full reporting and transparency.
>     
> 5. A p-value, or statistical significance, does not measure the size of an effect or the importance of a result.
>     
> 6. By itself, a p-value does not provide a good measure of evidence regarding a model or hypothesis.
>     

### Practical significance

Even if a result is statistically significant, that does not mean it has practical significance. A small difference that has no practical meaning can be statistically significant if it arose from large enough samples. Large samples ensure that small, non-meaningful effects can nonetheless be big enough to rule out chance as an explanation. Ruling out chance does not magically render important a result that is, in its essence, unimportant.

## Type 1 and Type 2 Errors

In assessing statistical significance, two types of error are possible:

- A Type 1 error, in which you mistakenly conclude an effect is real, when it is really just due to chance
    
- A Type 2 error, in which you mistakenly conclude that an effect is not real (i.e., due to chance), when it actually is real
    

Actually, a Type 2 error is not so much an error as a judgment that the sample size is too small to detect the effect. When a p-value falls short of statistical significance (e.g., it exceeds 5%), what we are really saying is “effect not proven.” It could be that a larger sample would yield a smaller p-value.

The basic function of significance tests (also called _hypothesis tests_) is to protect against being fooled by random chance; thus they are typically structured to minimize Type 1 errors.

## Data Science and p-Values

The work that data scientists do is typically not destined for publication in scientific journals, so the debate over the value of a p-value is somewhat academic. For a data scientist, a p-value is a useful metric in situations where you want to know whether a model result that appears interesting and useful is within the range of normal chance variability. As a decision tool in an experiment, a p-value should not be considered controlling, but merely another point of information bearing on a decision. For example, p-values are sometimes used as intermediate inputs in some statistical or machine learning models—a feature might be included in or excluded from a model depending on its p-value.

##### Key Ideas

- Significance tests are used to determine whether an observed effect is within the range of chance variation for a null hypothesis model.
    
- The p-value is the probability that results as extreme as the observed results might occur, given a null hypothesis model.
    
- The alpha value is the threshold of “unusualness” in a null hypothesis chance model.
    
- Significance testing has been much more relevant for formal reporting of research than for data science (but has been fading recently, even for the former).
    

## Further Reading

- Stephen Stigler, “Fisher and the 5% Level,” _Chance_ 21, no. 4 (2008): 12. This article is a short commentary on Ronald Fisher’s 1925 book _Statistical Methods for Research Workers_ (Oliver & Boyd), and on Fisher’s emphasis on the 5% level of significance.
    
- See also [“Hypothesis Tests”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Hypothesis_test) and the further reading mentioned there.
    

# t-Tests

There are numerous types of significance tests, depending on whether the data comprises count data or measured data, how many samples there are, and what’s being measured. A very common one is the _t-test_, named after Student’s t-distribution, originally developed by W. S. Gosset to approximate the distribution of a single sample mean (see [“Student’s t-Distribution”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#t-distribution)).

##### Key Terms for t-Tests

**_Test statistic_**

A metric for the difference or effect of interest.

**_t-statistic_**

A standardized version of common test statistics such as means.

**_t-distribution_**

A reference distribution (in this case derived from the null hypothesis), to which the observed t-statistic can be compared.

All significance tests require that you specify a _test statistic_ to measure the effect you are interested in and help you determine whether that observed effect lies within the range of normal chance variation. In a resampling test (see the discussion of permutation in [“Permutation Test”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Permutation)), the scale of the data does not matter. You create the reference (null hypothesis) distribution from the data itself and use the test statistic as is.

In the 1920s and 1930s, when statistical hypothesis testing was being developed, it was not feasible to randomly shuffle data thousands of times to do a resampling test. Statisticians found that a good approximation to the permutation (shuffled) distribution was the t-test, based on Gosset’s t-distribution. It is used for the very common two-sample comparison—A/B test—in which the data is numeric. But in order for the t-distribution to be used without regard to scale, a standardized form of the test statistic must be used.

A classic statistics text would at this stage show various formulas that incorporate Gosset’s distribution and demonstrate how to standardize your data to compare it to the standard t-distribution. These formulas are not shown here because all statistical software, as well as _R_ and _Python_, includes commands that embody the formula. In _R_, the function is `t.test`:

```
>
```

The function `scipy.stats.ttest_ind` can be used in _Python_:

```
res
```

The alternative hypothesis is that the page time mean for page A is less than that for page B. The p-value of 0.1408 is fairly close to the permutation test p-values of 0.121 and 0.126 (see [“Example: Web Stickiness”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#PermutationExample)).

In a resampling mode, we structure the solution to reflect the observed data and the hypothesis to be tested, not worrying about whether the data is numeric or binary, whether or not sample sizes are balanced, sample variances, or a variety of other factors. In the formula world, many variations present themselves, and they can be bewildering. Statisticians need to navigate that world and learn its map, but data scientists do not—they are typically not in the business of sweating the details of hypothesis tests and confidence intervals the way a researcher preparing a paper for presentation might.

##### Key Ideas

- Before the advent of computers, resampling tests were not practical, and statisticians used standard reference distributions.
    
- A test statistic could then be standardized and compared to the reference distribution.
    
- One such widely used standardized statistic is the t-statistic.
    

## Further Reading

- Any introductory statistics text will have illustrations of the t-statistic and its uses; two good ones are _Statistics_, 4th ed., by David Freedman, Robert Pisani, and Roger Purves (W. W. Norton, 2007), and _The Basic Practice of Statistics_, 8th ed., by David S. Moore, William I. Notz, and Michael A. Fligner (W. H. Freeman, 2017).
    
- For a treatment of both the t-test and resampling procedures in parallel, see _Introductory Statistics and Analytics: A Resampling Perspective_ by Peter Bruce (Wiley, 2014) or _Statistics: Unlocking the Power of Data_, 2nd ed., by Robin Lock and four other Lock family members (Wiley, 2016).
    

# Multiple Testing

As we’ve mentioned previously, there is a saying in statistics: “Torture the data long enough, and it will confess.” This means that if you look at the data through enough different perspectives and ask enough questions, you almost invariably will find a statistically significant effect.

For example, if you have 20 predictor variables and one outcome variable, all _randomly_ generated, the odds are pretty good that at least one predictor will (falsely) turn out to be statistically significant if you do a series of 20 significance tests at the alpha = 0.05 level. As previously discussed, this is called a _Type 1 error_. You can calculate this probability by first finding the probability that all will _correctly_ test nonsignificant at the 0.05 level. The probability that _one_ will correctly test nonsignificant is 0.95, so the probability that all 20 will correctly test nonsignificant is 0.95 × 0.95 × 0.95…, or 0.9520 = 0.36.[1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#idm45782043484424) The probability that at least one predictor will (falsely) test significant is the flip side of this probability, or 1 – (_probability that all will be nonsignificant_) = 0.64. This is known as _alpha inflation_.

This issue is related to the problem of overfitting in data mining, or “fitting the model to the noise.” The more variables you add, or the more models you run, the greater the probability that something will emerge as “significant” just by chance.

##### Key Terms for Multiple Testing

**_Type 1 error_**

Mistakenly concluding that an effect is statistically significant.

**_False discovery rate_**

Across multiple tests, the rate of making a Type 1 error.

**_Alpha inflation_**

The multiple testing phenomenon, in which _alpha_, the probability of making a Type 1 error, increases as you conduct more tests.

**_Adjustment of p-values_**

Accounting for doing multiple tests on the same data.

**_Overfitting_**

Fitting the noise.

In supervised learning tasks, a holdout set where models are assessed on data that the model has not seen before mitigates this risk. In statistical and machine learning tasks not involving a labeled holdout set, the risk of reaching conclusions based on statistical noise persists.

In statistics, there are some procedures intended to deal with this problem in very specific circumstances. For example, if you are comparing results across multiple treatment groups, you might ask multiple questions. So, for treatments A–C, you might ask:

- Is A different from B?
    
- Is B different from C?
    
- Is A different from C?
    

Or, in a clinical trial, you might want to look at results from a therapy at multiple stages. In each case, you are asking multiple questions, and with each question, you are increasing the chance of being fooled by chance. Adjustment procedures in statistics can compensate for this by setting the bar for statistical significance more stringently than it would be set for a single hypothesis test. These adjustment procedures typically involve “dividing up the alpha” according to the number of tests. This results in a smaller alpha (i.e., a more stringent bar for statistical significance) for each test. One such procedure, the Bonferroni adjustment, simply divides the alpha by the number of comparisons. Another, used in comparing multiple group means, is Tukey’s “honest significant difference,” or _Tukey’s HSD_. This test applies to the maximum difference among group means, comparing it to a benchmark based on the _t-distribution_ (roughly equivalent to shuffling all the values together, dealing out resampled groups of the same sizes as the original groups, and finding the maximum difference among the resampled group means).

However, the problem of multiple comparisons goes beyond these highly structured cases and is related to the phenomenon of repeated data “dredging” that gives rise to the saying about torturing the data. Put another way, given sufficiently complex data, if you haven’t found something interesting, you simply haven’t looked long and hard enough. More data is available now than ever before, and the number of journal articles published nearly doubled between 2002 and 2010. This gives rise to lots of opportunities to find something interesting in the data, including multiplicity issues such as:

- Checking for multiple pairwise differences across groups
    
- Looking at multiple subgroup results (“we found no significant treatment effect overall, but we did find an effect for unmarried women younger than 30”)
    
- Trying lots of statistical models
    
- Including lots of variables in models
    
- Asking a number of different questions (i.e., different possible outcomes)
    

# False Discovery Rate

The term _false discovery rate_ was originally used to describe the rate at which a given set of hypothesis tests would falsely identify a significant effect. It became particularly useful with the advent of genomic research, in which massive numbers of statistical tests might be conducted as part of a gene sequencing project. In these cases, the term applies to the testing protocol, and a single false “discovery” refers to the outcome of a hypothesis test (e.g., between two samples). Researchers sought to set the parameters of the testing process to control the false discovery rate at a specified level. The term has also been used for classification in data mining; it is the misclassification rate within the class 1 predictions. Or, put another way, it is the probability that a “discovery” (labeling a record as a “1”) is false. Here we typically are dealing with the case where 0s are abundant and 1s are interesting and rare (see [Chapter 5](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch05.html#Classification) and [“The Rare Class Problem”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch05.html#RareClassProblem)).

For a variety of reasons, including especially this general issue of “multiplicity,” more research does not necessarily mean better research. For example, the pharmaceutical company Bayer found in 2011 that when it tried to replicate 67 scientific studies, it could fully replicate only 14 of them. Nearly two-thirds could not be replicated at all.

In any case, the adjustment procedures for highly defined and structured statistical tests are too specific and inflexible to be of general use to data scientists. The bottom line for data scientists on multiplicity is:

- For predictive modeling, the risk of getting an illusory model whose apparent efficacy is largely a product of random chance is mitigated by cross-validation (see [“Cross-Validation”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#CrossValidation)) and use of a holdout sample.
    
- For other procedures without a labeled holdout set to check the model, you must rely on:
    
    - Awareness that the more you query and manipulate the data, the greater the role that chance might play.
        
    - Resampling and simulation heuristics to provide random chance benchmarks against which observed results can be compared.
        

##### Key Ideas

- Multiplicity in a research study or data mining project (multiple comparisons, many variables, many models, etc.) increases the risk of concluding that something is significant just by chance.
    
- For situations involving multiple statistical comparisons (i.e., multiple tests of significance), there are statistical adjustment procedures.
    
- In a data mining situation, use of a holdout sample with labeled outcome variables can help avoid misleading results.
    

## Further Reading

- For a short exposition of one procedure (Dunnett’s test) to adjust for multiple comparisons, see David Lane’s [online statistics text](https://oreil.ly/hd_62).
    
- Megan Goldman offers a [slightly longer treatment of the Bonferroni adjustment procedure](https://oreil.ly/Dt4Vi).
    
- For an in-depth treatment of more flexible statistical procedures for adjusting p-values, see _Resampling-Based Multiple Testing_ by Peter Westfall and Stanley Young (Wiley, 1993).
    
- For a discussion of data partitioning and the use of holdout samples in predictive modeling, see Chapter 2 of _Data Mining for Business Analytics_, by Galit Shmueli, Peter Bruce, Nitin Patel, Peter Gedeck, Inbal Yahav, and Kenneth Lichtendahl (Wiley, 2007–2020, with editions for _R_, _Python_, Excel, and JMP).
    

# Degrees of Freedom

In the documentation and settings for many statistical tests and probability distributions, you will see a reference to “degrees of freedom.” The concept is applied to statistics calculated from sample data, and refers to the number of values free to vary. For example, if you know the mean for a sample of 10 values, there are 9 degrees of freedom (once you know 9 of the sample values, the 10th can be calculated and is not free to vary). The degrees of freedom parameter, as applied to many probability distributions, affects the shape of the distribution.

The number of degrees of freedom is an input to many statistical tests. For example, degrees of freedom is the name given to the _n_ – 1 denominator seen in the calculations for variance and standard deviation. Why does it matter? When you use a sample to estimate the variance for a population, you will end up with an estimate that is slightly biased downward if you use _n_ in the denominator. If you use _n_ – 1 in the denominator, the estimate will be free of that bias.

##### Key Terms for Degrees of Freedom

**_n or sample size_**

The number of observations (also called _rows_ or _records_) in the data.

**_d.f._**

Degrees of freedom.

A large share of a traditional statistics course or text is consumed by various standard tests of hypotheses (t-test, F-test, etc.). When sample statistics are standardized for use in traditional statistical formulas, degrees of freedom is part of the standardization calculation to ensure that your standardized data matches the appropriate reference distribution (t-distribution, F-distribution, etc.).

Is it important for data science? Not really, at least in the context of significance testing. For one thing, formal statistical tests are used only sparingly in data science. For another, the data size is usually large enough that it rarely makes a real difference for a data scientist whether, for example, the denominator has _n_ or _n_ – 1. (As _n_ gets large, the bias that would come from using _n_ in the denominator disappears.)

There is one context, though, in which it is relevant: the use of factored variables in regression (including logistic regression). Some regression algorithms choke if exactly redundant predictor variables are present. This most commonly occurs when factoring categorical variables into binary indicators (dummies). Consider the variable “day of week.” Although there are seven days of the week, there are only six degrees of freedom in specifying day of week. For example, once you know that day of week is not Monday through Saturday, you know it must be Sunday. Inclusion of the Mon–Sat indicators thus means that _also_ including Sunday would cause the regression to fail, due to a _multicollinearity_ error.

##### Key Ideas

- The number of degrees of freedom (d.f.) forms part of the calculation to standardize test statistics so they can be compared to reference distributions (t-distribution, F-distribution, etc.).
    
- The concept of degrees of freedom lies behind the factoring of categorical variables into _n_ – 1 indicator or dummy variables when doing a regression (to avoid multicollinearity).
    

## Further Reading

There are [several web tutorials on degrees of freedom](https://oreil.ly/VJyts).

# ANOVA

Suppose that, instead of an A/B test, we had a comparison of multiple groups, say A/B/C/D, each with numeric data. The statistical procedure that tests for a statistically significant difference among the groups is called _analysis of variance_, or _ANOVA_.

##### Key Terms for ANOVA

**_Pairwise comparison_**

A hypothesis test (e.g., of means) between two groups among multiple groups.

**_Omnibus test_**

A single hypothesis test of the overall variance among multiple group means.

**_Decomposition of variance_**

Separation of components contributing to an individual value (e.g., from the overall average, from a treatment mean, and from a residual error).

**_F-statistic_**

A standardized statistic that measures the extent to which differences among group means exceed what might be expected in a chance model.

**_SS_**

“Sum of squares,” referring to deviations from some average value.

[Table 3-3](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#FourSessionsData) shows the stickiness of four web pages, defined as the number of seconds a visitor spent on the page. The four pages are switched out so that each web visitor receives one at random. There are a total of five visitors for each page, and in [Table 3-3](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#FourSessionsData), each column is an independent set of data. The first viewer for page 1 has no connection to the first viewer for page 2. Note that in a web test like this, we cannot fully implement the classic randomized sampling design in which each visitor is selected at random from some huge population. We must take the visitors as they come. Visitors may systematically differ depending on time of day, time of week, season of the year, conditions of their internet, what device they are using, and so on. These factors should be considered as potential bias when the experiment results are reviewed.

Table 3-3. Stickiness (in seconds) of four web pages
||Page 1|Page 2|Page 3|Page 4|
|---|---|---|---|---|
||164|178|175|155|
||172|191|193|166|
||177|182|171|164|
||156|185|163|170|
||195|177|176|168|
|Average|172|185|176|162|
|Grand average||||173.75|

Now we have a conundrum (see [Figure 3-6](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#FourGroups)). When we were comparing just two groups, it was a simple matter; we merely looked at the difference between the means of each group. With four means, there are six possible comparisons between groups:

- Page 1 compared to page 2
    
- Page 1 compared to page 3
    
- Page 1 compared to page 4
    
- Page 2 compared to page 3
    
- Page 2 compared to page 4
    
- Page 3 compared to page 4
    

The more such _pairwise_ comparisons we make, the greater the potential for being fooled by random chance (see [“Multiple Testing”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#MultipleTesting)). Instead of worrying about all the different comparisons between individual pages we could possibly make, we can do a single overall test that addresses the question, “Could all the pages have the same underlying stickiness, and the differences among them be due to the random way in which a common set of page times got allocated among the four pages?”

![Session times across four different web pages.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0306.png)

###### Figure 3-6. Boxplots of the four groups show considerable differences among them

The procedure used to test this is ANOVA. The basis for it can be seen in the following resampling procedure (specified here for the A/B/C/D test of web page stickiness):

1. Combine all the data together in a single box.
    
2. Shuffle and draw out four resamples of five values each.
    
3. Record the mean of each of the four groups.
    
4. Record the variance among the four group means.
    
5. Repeat steps 2–4 many (say, 1,000) times.
    

What proportion of the time did the resampled variance exceed the observed variance? This is the p-value.

This type of permutation test is a bit more involved than the type used in [“Permutation Test”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#Permutation). Fortunately, the `aovp` function in the `lmPerm` package computes a permutation test for this case:

```
>
```

The p-value, given by `Pr(Prob)`, is 0.09278. In other words, given the same underlying stickiness, 9.3% of the time the response rate among four pages might differ as much as was actually observed, just by chance. This degree of improbability falls short of the traditional statistical threshold of 5%, so we conclude that the difference among the four pages could have arisen by chance.

The column `Iter` lists the number of iterations taken in the permutation test. The other columns correspond to a traditional ANOVA table and are described next.

In _Python_, we can compute the permutation test using the following code:

```
observed_variance
```

## F-Statistic

Just like the t-test can be used instead of a permutation test for comparing the mean of two groups, there is a statistical test for ANOVA based on the _F-statistic_. The F-statistic is based on the ratio of the variance across group means (i.e., the treatment effect) to the variance due to residual error. The higher this ratio, the more statistically significant the result. If the data follows a normal distribution, then statistical theory dictates that the statistic should have a certain distribution. Based on this, it is possible to compute a p-value.

In _R_, we can compute an _ANOVA table_ using the `aov` function:

```
>
```

The `statsmodels` package provides an ANOVA implementation in _Python_:

```
model
```

The output from the _Python_ code is almost identical to that from _R_.

`Df` is “degrees of freedom,” `Sum Sq` is “sum of squares,” `Mean Sq` is “mean squares” (short for mean-squared deviations), and `F value` is the F-statistic. For the grand average, sum of squares is the departure of the grand average from 0, squared, times 20 (the number of observations). The degrees of freedom for the grand average is 1, by definition.

For the treatment means, the degrees of freedom is 3 (once three values are set, and then the grand average is set, the other treatment mean cannot vary). Sum of squares for the treatment means is the sum of squared departures between the treatment means and the grand average.

For the residuals, degrees of freedom is 16 (20 observations, 16 of which can vary after the the grand mean and the treatment means are set), and SS is the sum of squared difference between the individual observations and the treatment means. Mean squares (MS) is the sum of squares divided by the degrees of freedom.

The F-statistic is MS(treatment)/MS(error). The F value thus depends only on this ratio and can be compared to a standard F-distribution to determine whether the differences among treatment means are greater than would be expected in random chance variation.

# Decomposition of Variance

Observed values in a data set can be considered sums of different components. For any observed data value within a data set, we can break it down into the grand average, the treatment effect, and the residual error. We call this a “decomposition of variance”:

1. Start with grand average (173.75 for web page stickiness data).
    
2. Add treatment effect, which might be negative (independent variable = web page).
    
3. Add residual error, which might be negative.
    

Thus the decomposition of the variance for the top-left value in the A/B/C/D test table is as follows:

1. Start with grand average: 173.75.
    
2. Add treatment (group) effect: –1.75 (172 – 173.75).
    
3. Add residual: –8 (164 – 172).
    
4. Equals: 164.
    

## Two-Way ANOVA

The A/B/C/D test just described is a “one-way” ANOVA, in which we have one factor (group) that is varying. We could have a second factor involved—say, “weekend versus weekday”—with data collected on each combination (group A weekend, group A weekday, group B weekend, etc.). This would be a “two-way ANOVA,” and we would handle it in similar fashion to the one-way ANOVA by identifying the “interaction effect.” After identifying the grand average effect and the treatment effect, we then separate the weekend and weekday observations for each group and find the difference between the averages for those subsets and the treatment average.

You can see that ANOVA and then two-way ANOVA are the first steps on the road toward a full statistical model, such as regression and logistic regression, in which multiple factors and their effects can be modeled (see [Chapter 4](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#Regression)).

##### Key Ideas

- ANOVA is a statistical procedure for analyzing the results of an experiment with multiple groups.
    
- It is the extension of similar procedures for the A/B test, used to assess whether the overall variation among groups is within the range of chance variation.
    
- A useful outcome of ANOVA is the identification of variance components associated with group treatments, interaction effects, and errors.
    

## Further Reading

- _Introductory Statistics and Analytics: A Resampling Perspective_ by Peter Bruce (Wiley, 2014) has a chapter on ANOVA.
    
- _Introduction to Design and Analysis of Experiments_ by George Cobb (Wiley, 2008) is a comprehensive and readable treatment of its subject.
    

# Chi-Square Test

Web testing often goes beyond A/B testing and tests multiple treatments at once. The chi-square test is used with count data to test how well it fits some expected distribution. The most common use of the _chi-square_ statistic in statistical practice is with  contingency tables, to assess whether the null hypothesis of independence among variables is reasonable (see also [“Chi-Square Distribution”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#chi-square-dist)).

The chi-square test was [originally developed by Karl Pearson in 1900](https://oreil.ly/cEubO). The term _chi_ comes from the Greek letter Χ used by Pearson in the article.

##### Key Terms for Chi-Square Test

**_Chi-square statistic_**

A measure of the extent to which some observed data departs from expectation.

**_Expectation_ or _expected_**

How we would expect the data to turn out under some assumption, typically the null hypothesis.

###### Note

 means “rows by columns”—a 2 × 3 table has two rows and three columns.

## Chi-Square Test: A Resampling Approach

Suppose you are testing three different headlines—A, B, and C—and you run them each on 1,000 visitors, with the results shown in [Table 3-4](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#table0304).

Table 3-4. Web testing results for three different headlines
||Headline A|Headline B|Headline C|
|---|---|---|---|
|Click|14|8|12|
|No-click|986|992|988|

The headlines certainly appear to differ. Headline A returns nearly twice the click rate of B. The actual numbers are small, though. A resampling procedure can test whether the click rates differ to an extent greater than chance might cause. For this test, we need to have the “expected” distribution of clicks, and in this case, that would be under the null hypothesis assumption that all three headlines share the same click rate, for an overall click rate of 34/3,000. Under this assumption, our contingency table would look like [Table 3-5](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#table0305).

Table 3-5. Expected if all three headlines have the same click rate (null hypothesis)
||Headline A|Headline B|Headline C|
|---|---|---|---|
|Click|11.33|11.33|11.33|
|No-click|988.67|988.67|988.67|

The _Pearson residual_ is defined as:

_R_ measures the extent to which the actual counts differ from these expected counts (see [Table 3-6](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#table0306)).

Table 3-6. Pearson residuals
||Headline A|Headline B|Headline C|
|---|---|---|---|
|Click|0.792|–0.990|0.198|
|No-click|–0.085|0.106|–0.021|

The chi-square statistic is defined as the sum of the squared Pearson residuals:

where _r_ and _c_ are the number of rows and columns, respectively. The chi-square statistic for this example is 1.666. Is that more than could reasonably occur in a chance model?

We can test with this resampling algorithm:

1. Constitute a box with 34 ones (clicks) and 2,966 zeros (no clicks).
    
2. Shuffle, take three separate samples of 1,000, and count the clicks in each.
    
3. Find the squared differences between the shuffled counts and the expected counts and sum them.
    
4. Repeat steps 2 and 3, say, 1,000 times.
    
5. How often does the resampled sum of squared deviations exceed the observed? That’s the p-value.
    

The function `chisq.test` can be used to compute a resampled chi-square statistic in _R_. For the click data, the chi-square test is:

```
>
```

The test shows that this result could easily have been obtained by randomness.

To run a permutation test in _Python_, use the following implementation:

```
box
```

## Chi-Square Test: Statistical Theory

Asymptotic statistical theory shows that the distribution of the chi-square statistic can be approximated by a _chi-square distribution_ (see [“Chi-Square Distribution”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#chi-square-dist)). The appropriate standard chi-square distribution is determined by the _degrees of freedom_ (see [“Degrees of Freedom”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#DOF)). For a contingency table, the degrees of freedom are related to the number of rows (_r_) and columns (_c_) as follows:

The chi-square distribution is typically skewed, with a long tail to the right; see [Figure 3-7](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#ChiSquareDist) for the distribution with 1, 2, 5, and 20 degrees of freedom. The further out on the chi-square distribution the observed statistic is, the lower the p-value.

The function `chisq.test` can be used to compute the p-value using the chi-square distribution as a reference:

```
>
```

In _Python_, use the function `scipy.stats.chi2_contingency`:

```
chisq
```

The p-value is a little less than the resampling p-value; this is because the chi-square distribution is only an approximation of the actual distribution of the statistic.

![Chi-square distribution for 1, 2, 5 and 20 degrees of freedom](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0307.png)

###### Figure 3-7. Chi-square distribution with various degrees of freedom

## Fisher’s Exact Test

The chi-square distribution is a good approximation of the shuffled resampling test just described, except when counts are extremely low (single digits, especially five or fewer). In such cases, the resampling procedure will yield more accurate p-values. In fact, most statistical software has a procedure to actually enumerate _all_ the possible rearrangements (permutations) that can occur, tabulate their frequencies, and determine exactly how extreme the observed result is. This is called _Fisher’s exact test_ after the great statistician R. A. Fisher. _R_ code for Fisher’s exact test is simple in its basic form:

```
>
```

The p-value is very close to the p-value of 0.4853 obtained using the resampling method.

Where some counts are very low but others are quite high (e.g., the denominator in a conversion rate), it may be necessary to do a shuffled permutation test instead of a full exact test, due to the difficulty of calculating all possible permutations. The preceding _R_ function has several arguments that control whether to use this approximation (`simulate.p.value=TRUE or FALSE`), how many iterations should be used (`B=...`), and a computational constraint (`workspace=...`) that limits how far calculations for the _exact_ result should go.

There is no implementation of Fisher’s exact test easily available in _Python_.

##### Detecting Scientific Fraud

An interesting example is provided by the case of Tufts University researcher Thereza Imanishi-Kari, who was accused in 1991 of fabricating data in her research. Congressman John Dingell became involved, and the case eventually led to the resignation of her colleague, David Baltimore, from the presidency of Rockefeller University.

One element in the case rested on statistical evidence regarding the expected distribution of digits in her laboratory data, where each observation had many digits. Investigators focused on the _interior_ digits (ignoring the first digit and last digit of a number), which would be expected to follow a _uniform random_ distribution. That is, they would occur randomly, with each digit having equal probability of occurring (the lead digit might be predominantly one value, and the final digits might be affected by rounding). [Table 3-7](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#table0307) lists the frequencies of interior digits from the actual data in the case.

Table 3-7. Frequency of interior digits in laboratory data
|Digit|Frequency|
|---|---|
|0|14|
|1|71|
|2|7|
|3|65|
|4|23|
|5|19|
|6|12|
|7|45|
|8|53|
|9|6|

The distribution of the 315 digits, shown in [Figure 3-8](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#ImanishiHist), certainly looks nonrandom.

Investigators calculated the departure from expectation (31.5—that’s how often each digit would occur in a strictly uniform distribution) and used a chi-square test (a resampling procedure could equally have been used) to show that the actual distribution was well beyond the range of normal chance variation, indicating the data might have been fabricated. (Note: Imanishi-Kari was ultimately exonerated after a lengthy proceeding.)

![A histogram of the interior digits from data in the case involving Imanishi-Kari.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0308.png)

###### Figure 3-8. Frequency histogram for Imanishi-Kari lab data

## Relevance for Data Science

The chi-square test, or Fisher’s exact test, is used when you want to know whether an effect is for real or might be the product of chance. In most classical statistical applications of the chi-square test, its role is to establish statistical significance, which is typically needed before a study or an experiment can be published. This is not so important for data scientists. In most data science experiments, whether A/B or A/B/C…, the goal is not simply to establish statistical significance but rather to arrive at the best treatment. For this purpose, multi-armed bandits (see [“Multi-Arm Bandit Algorithm”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#bandits)) offer a more complete solution.

One data science application of the chi-square test, especially Fisher’s exact version, is in determining appropriate sample sizes for web experiments. These experiments often have very low click rates, and despite thousands of exposures, count rates might be too small to yield definitive conclusions in an experiment. In such cases, Fisher’s exact test, the chi-square test, and other tests can be useful as a component of power and sample size calculations (see [“Power and Sample Size”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#PowerSampleSize)).

Chi-square tests are used widely in research by investigators in search of the elusive statistically significant p-value that will allow publication. Chi-square tests, or similar resampling simulations, are used in data science applications more as a filter to determine whether an effect or a feature is worthy of further consideration than as a formal test of significance. For example, they are used in spatial statistics and mapping to determine whether spatial data conforms to a specified null distribution (e.g., are crimes concentrated in a certain area to a greater degree than random chance would allow?). They can also be used in automated feature selection in machine learning, to assess class prevalence across features and identify features where the prevalence of a certain class is unusually high or low, in a way that is not compatible with random variation.

##### Key Ideas

- A common procedure in statistics is to test whether observed data counts are consistent with an assumption of independence (e.g., propensity to buy a particular item is independent of gender).
    
- The chi-square distribution is the reference distribution (which embodies the assumption of independence) to which the observed calculated chi-square statistic must be compared.
    

## Further Reading

- R. A. Fisher’s famous “Lady Tasting Tea” example from the beginning of the 20th century remains a simple and effective illustration of his exact test. Google “Lady Tasting Tea,” and you will find a number of good writeups.
    
- Stat Trek offers a [good tutorial on the chi-square test](https://oreil.ly/77DUf).
    

# Multi-Arm Bandit Algorithm

Multi-arm bandits offer an approach to testing, especially web testing, that allows explicit optimization and more rapid decision making than the traditional statistical approach to designing experiments.

##### Key Terms for Multi-Arm Bandits

**_Multi-arm bandit_**

An imaginary slot machine with multiple arms for the customer to choose from, each with different payoffs, here taken to be an analogy for a multitreatment experiment.

**_Arm_**

A treatment in an experiment (e.g., “headline A in a web test”).

**_Win_**

The experimental analog of a win at the slot machine (e.g., “customer clicks on the link”).

A traditional A/B test involves data collected in an experiment, according to a specified design, to answer a specific question such as, “Which is better, treatment A or treatment B?” The presumption is that once we get an answer to that question, the experimenting is over and we proceed to act on the results.

You can probably perceive several difficulties with that approach. First, our answer may be inconclusive: “effect not proven.” In other words, the results from the experiment may suggest an effect, but if there is an effect, we don’t have a big enough sample to prove it (to the satisfaction of the traditional statistical standards). What decision do we take? Second, we might want to begin taking advantage of results that come in prior to the conclusion of the experiment. Third, we might want the right to change our minds or to try something different based on additional data that comes in after the experiment is over. The traditional approach to experiments and hypothesis tests dates from the 1920s and is rather inflexible. The advent of computer power and software has enabled more powerful flexible approaches. Moreover, data science (and business in general) is not so worried about statistical significance, but concerned more with optimizing overall effort and results.

Bandit algorithms, which are very popular in web testing, allow you to test multiple treatments at once and reach conclusions faster than traditional statistical designs. They take their name from slot machines used in gambling, also termed one-armed bandits (since they are configured in such a way that they extract money from the gambler in a steady flow). If you imagine a slot machine with more than one arm, each arm paying out at a different rate, you would have a multi-armed bandit, which is the full name for this algorithm.

Your goal is to win as much money as possible and, more specifically, to identify and settle on the winning arm sooner rather than later. The challenge is that you don’t know at what overall rate the arms pay out—you only know the results of individual pulls on the arms. Suppose each “win” is for the same amount, no matter which arm. What differs is the probability of a win. Suppose further that you initially try each arm 50 times and get the following results:

- Arm A: 10 wins out of 50
- Arm B: 2 win out of 50
- Arm C: 4 wins out of 50

One extreme approach is to say, “Looks like arm A is a winner—let’s quit trying the other arms and stick with A.” This takes full advantage of the information from the initial trial. If A is truly superior, we get the benefit of that early on. On the other hand, if B or C is truly better, we lose any opportunity to discover that. Another extreme approach is to say, “This all looks to be within the realm of chance—let’s keep pulling them all equally.” This gives maximum opportunity for alternates to A to show themselves. However, in the process, we are deploying what seem to be inferior treatments. How long do we permit that? Bandit algorithms take a hybrid approach: we start pulling A more often, to take advantage of its apparent superiority, but we don’t abandon B and C. We just pull them less often. If A continues to outperform, we continue to shift resources (pulls) away from B and C and pull A more often. If, on the other hand, C starts to do better, and A starts to do worse, we can shift pulls from A back to C. If one of them turns out to be superior to A and this was hidden in the initial trial due to chance, it now has an opportunity to emerge with further testing.

Now think of applying this to web testing. Instead of multiple slot machine arms, you might have multiple offers, headlines, colors, and so on being tested on a website. Customers either click (a “win” for the merchant) or don’t click. Initially, the offers are shown randomly and equally. If, however, one offer starts to outperform the others, it can be shown (“pulled”) more often. But what should the parameters of the algorithm that modifies the pull rates be? What “pull rates” should we change to, and when should we change?

Here is one simple algorithm, the epsilon-greedy algorithm for an A/B test:

1. Generate a uniformly distributed random number between 0 and 1.
    
2. If the number lies between 0 and epsilon (where epsilon is a number between 0 and 1, typically fairly small), flip a fair coin (50/50 probability), and:
    
    1. If the coin is heads, show offer A.
        
    2. If the coin is tails, show offer B.
        
3. If the number is ≥ epsilon, show whichever offer has had the highest response rate to date.
    

Epsilon is the single parameter that governs this algorithm. If epsilon is 1, we end up with a standard simple A/B experiment (random allocation between A and B for each subject). If epsilon is 0, we end up with a purely _greedy_ algorithm—one that chooses the best available immediate option (a local optimum). It seeks no further experimentation, simply assigning subjects (web visitors) to the best-performing treatment.

A more sophisticated algorithm uses “Thompson’s sampling.” This procedure “samples” (pulls a bandit arm) at each stage to maximize the probability of choosing the best arm. Of course you don’t know which is the best arm—that’s the whole problem!—but as you observe the payoff with each successive draw, you gain more information. Thompson’s sampling uses a Bayesian approach: some prior distribution of rewards is assumed initially, using what is called a _beta distribution_ (this is a common mechanism for specifying prior information in a Bayesian problem). As information accumulates from each draw, this information can be updated, allowing the selection of the next draw to be better optimized as far as choosing the right arm.

Bandit algorithms can efficiently handle 3+ treatments and move toward optimal selection of the “best.” For traditional statistical testing procedures, the complexity of decision making for 3+ treatments far outstrips that of the traditional A/B test, and the advantage of bandit algorithms is much greater.

##### Key Ideas

- Traditional A/B tests envision a random sampling process, which can lead to excessive exposure to the inferior treatment.
    
- Multi-arm bandits, in contrast, alter the sampling process to incorporate information learned during the experiment and reduce the frequency of the inferior treatment.
    
- They also facilitate efficient treatment of more than two treatments.
    
- There are different algorithms for shifting sampling probability away from the inferior treatment(s) and to the (presumed) superior one.
    

## Further Reading

- An excellent short treatment of multi-arm bandit algorithms is found in _Bandit Algorithms for Website Optimization_, by John Myles White (O’Reilly, 2012). White includes _Python_ code, as well as the results of simulations to assess the performance of bandits.
    
- For more (somewhat technical) information about Thompson sampling, see [“Analysis of Thompson Sampling for the Multi-armed Bandit Problem”](https://oreil.ly/OgWrG) by Shipra Agrawal and Navin Goyal.
    

# Power and Sample Size

If you run a web test, how do you decide how long it should run (i.e., how many impressions per treatment are needed)? Despite what you may read in many guides to web testing, there is no good general guidance—it depends, mainly, on the frequency with which the desired goal is attained.

##### Key Terms for Power and Sample Size

**_Effect size_**

The minimum size of the effect that you hope to be able to detect in a statistical test, such as “a 20% improvement in click rates.”

**_Power_**

The probability of detecting a given effect size with a given sample size.

**_Significance level_**

The statistical significance level at which the test will be conducted.

One step in statistical calculations for sample size is to ask “Will a hypothesis test actually reveal a difference between treatments A and B?” The outcome of a hypothesis test—the p-value—depends on what the real difference is between treatment A and treatment B. It also depends on the luck of the draw—who gets selected for the groups in the experiment. But it makes sense that the bigger the actual difference between treatments A and B, the greater the probability that our experiment will reveal it; and the smaller the difference, the more data will be needed to detect it. To distinguish between a .350 hitter and a .200 hitter in baseball, not that many at-bats are needed. To distinguish between a .300 hitter and a .280 hitter, a good many more at-bats will be needed.

_Power_ is the probability of detecting a specified _effect size_ with specified sample characteristics (size and variability). For example, we might say (hypothetically) that the probability of distinguishing between a .330 hitter and a .200 hitter in 25 at-bats is 0.75. The effect size here is a difference of .130. And “detecting” means that a hypothesis test will reject the null hypothesis of “no difference” and conclude there is a real effect. So the experiment of 25 at-bats (_n_ = 25) for two hitters, with an effect size of 0.130, has (hypothetical) power of 0.75, or 75%.

You can see that there are several moving parts here, and it is easy to get tangled up in the numerous statistical assumptions and formulas that will be needed (to specify sample variability, effect size, sample size, alpha-level for the hypothesis test, etc., and to calculate power). Indeed, there is special-purpose statistical software to calculate power. Most data scientists will not need to go through all the formal steps needed to report power, for example, in a published paper. However, they may face occasions where they want to collect some data for an A/B test, and collecting or processing the data involves some cost. In that case, knowing approximately how much data to collect can help avoid the situation where you collect data at some effort, and the result ends up being inconclusive. Here’s a fairly intuitive alternative approach:

1. Start with some hypothetical data that represents your best guess about the data that will result (perhaps based on prior data)—for example, a box with 20 ones and 80 zeros to represent a .200 hitter, or a box with some observations of “time spent on website.”
    
2. Create a second sample simply by adding the desired effect size to the first sample—for example, a second box with 33 ones and 67 zeros, or a second box with 25 seconds added to each initial “time spent on website.”
    
3. Draw a bootstrap sample of size _n_ from each box.
    
4. Conduct a permutation (or formula-based) hypothesis test on the two bootstrap samples and record whether the difference between them is statistically significant.
    
5. Repeat the preceding two steps many times and determine how often the difference was significant—that’s the estimated power.
    

## Sample Size

The most common use of power calculations is to estimate how big a sample you will need.

For example, suppose you are looking at click-through rates (clicks as a percentage of exposures), and testing a new ad against an existing ad. How many clicks do you need to accumulate in the study? If you are interested only in results that show a huge difference (say, a 50% difference), a relatively small sample might do the trick. If, on the other hand, even a minor difference would be of interest, then a much larger sample is needed. A standard approach is to establish a policy that a new ad must do better than an existing ad by some percentage, say, 10%; otherwise, the existing ad will remain in place. This goal, the “effect size,” then drives the sample size.

For example, suppose current click-through rates are about 1.1%, and you are seeking a 10% boost to 1.21%. So we have two boxes: box A with 1.1% ones (say, 110 ones and 9,890 zeros), and box B with 1.21% ones (say, 121 ones and 9,879 zeros). For starters, let’s try 300 draws from each box (this would be like 300 “impressions” for each ad). Suppose our first draw yields the following:

- Box A: 3 ones
- Box B: 5 ones

Right away we can see that any hypothesis test would reveal this difference (5 versus 3) to be well within the range of chance variation. This combination of sample size (_n_ = 300 in each group) and effect size (10% difference) is too small for any hypothesis test to reliably show a difference.

So we can try increasing the sample size (let’s try 2,000 impressions), and require a larger improvement (50% instead of 10%).

For example, suppose current click-through rates are still 1.1%, but we are now seeking a 50% boost to 1.65%. So we have two boxes: box A still with 1.1% ones (say, 110 ones and 9,890 zeros), and box B with 1.65% ones (say, 165 ones and 9,868 zeros). Now we’ll try 2,000 draws from each box. Suppose our first draw yields the following:

- Box A: 19 ones
- Box B: 34 ones

A significance test on this difference (34–19) shows it still registers as “not significant” (though much closer to significance than the earlier difference of 5–3). To calculate power, we would need to repeat the previous procedure many times, or use statistical software that can calculate power, but our initial draw suggests to us that even detecting a 50% improvement will require several thousand ad impressions.

In summary, for calculating power or required sample size, there are four moving parts:

- Sample size
    
- Effect size you want to detect
    
- Significance level (alpha) at which the test will be conducted
    
- Power
    

Specify any three of them, and the fourth can be calculated. Most commonly, you would want to calculate sample size, so you must specify the other three. With _R_ and _Python_, you also have to specify the alternative hypothesis as “greater” or “larger” to get a one-sided test; see [“One-Way Versus Two-Way Hypothesis Tests”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#directional) for more discussion of one-way versus two-way tests. Here is _R_ code for a test involving two proportions, where both samples are the same size (this uses the `pwr` package):

```
effect_size
```

The function `ES.h` calculates the effect size. We see that if we want a power of 80%, we require a sample size of almost 120,000 impressions. If we are seeking a 50% boost (`p1=0.0165`), the sample size is reduced to 5,500 impressions.

The `statsmodels` package contains several methods for power calculation. Here, we use `proportion_effectsize` to calculate the effect size and `TTestIndPower` to solve for the sample size:

```
effect_size
```

##### Key Ideas

- Finding out how big a sample size you need requires thinking ahead to the statistical test you plan to conduct.
    
- You must specify the minimum size of the effect that you want to detect.
    
- You must also specify the required probability of detecting that effect size (power).
    
- Finally, you must specify the significance level (alpha) at which the test will be conducted.
    

## Further Reading

- _Sample Size Determination and Power_ by Thomas Ryan (Wiley, 2013) is a comprehensive and readable review of this subject.
    
- Steve Simon, a statistical consultant, has written a [very engaging narrative-style post on the subject](https://oreil.ly/18mtp).
    

# Summary

The principles of experimental design—randomization of subjects into two or more groups receiving different treatments—allow us to draw valid conclusions about how well the treatments work. It is best to include a control treatment of “making no change.” The subject of formal statistical inference—hypothesis testing, p-values, t-tests, and much more along these lines—occupies much time and space in a traditional statistics course or text, and the formality is mostly unneeded from a data science perspective. However, it remains important to recognize the role that random variation can play in fooling the human brain. Intuitive resampling procedures (permutation and bootstrap) allow data scientists to gauge the extent to which chance variation can play a role in their data analysis.

[1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#idm45782043484424-marker) The multiplication rule states that the probability of _n_ independent events all happening is the product of the individual probabilities. For example, if you and I each flip a coin once, the probability that your coin and my coin will both land heads is 0.5 × 0.5 = 0.25.
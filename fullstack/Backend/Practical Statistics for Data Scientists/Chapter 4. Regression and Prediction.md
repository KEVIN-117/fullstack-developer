Perhaps the most common goal in statistics is to answer the question “Is the variable _X_ (or more likely, $X_1, ..., X_p$) associated with a variable _Y_, and if so, what is the relationship and can we use it to predict _Y_?”

Nowhere is the nexus between statistics and data science stronger than in the realm of prediction—specifically, the prediction of an outcome (target) variable based on the values of other “predictor” variables. This process of training a model on data where the outcome is known, for subsequent application to data where the outcome is not known, is termed _supervised learning_. Another important connection between data science and statistics is in the area of _anomaly detection_, where regression diagnostics originally intended for data analysis and improving the regression model can be used to detect unusual records.

# Simple Linear Regression

Simple linear regression provides a model of the relationship between the magnitude of one variable and that of a second—for example, as _X_ increases, _Y_ also increases. Or as _X_ increases, _Y_ decreases.[1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782041795848) Correlation is another way to measure how two variables are related—see the section [“Correlation”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch01.html#Correlations). The difference is that while correlation measures the _strength_ of an association between two variables, regression quantifies the _nature_ of the relationship.

##### Key Terms for Simple Linear Regression

- **_Response_**

	The variable we are trying to predict.

	- Synonyms

		dependent variable, _Y_ variable, target, outcome

- **_Independent variable_**

	The variable used to predict the response.

	- Synonyms

		_X_ variable, feature, attribute, predictor

- **_Record_**

	The vector of predictor and outcome values for a specific individual or case.

	- Synonyms

		row, case, instance, example

- **_Intercept_**

	The intercept of the regression line—that is, the predicted value when $X=0$ .

	- Synonyms

, 

**_Regression coefficient_**

The slope of the regression line.

Synonyms

slope, , , parameter estimates, weights

**_Fitted values_**

The estimates  obtained from the regression line.

Synonym

predicted values

**_Residuals_**

The difference between the observed values and the fitted values.

Synonym

errors

**_Least squares_**

The method of fitting a regression by minimizing the sum of squared residuals.

Synonyms

ordinary least squares, OLS

## The Regression Equation

Simple linear regression estimates how much _Y_ will change when _X_ changes by a certain amount. With the correlation coefficient, the variables _X_ and _Y_ are interchangeable. With regression, we are trying to predict the _Y_ variable from _X_ using a linear relationship (i.e., a line):

We read this as “Y equals b1 times X, plus a constant b0.” The symbol  is known as the _intercept_ (or constant), and the symbol  as the _slope_ for _X_. Both appear in _R_ output as _coefficients_, though in general use the term _coefficient_ is often reserved for . The _Y_ variable is known as the _response_ or _dependent_ variable since it depends on _X_. The _X_ variable is known as the _predictor_ or _independent_ variable. The machine learning community tends to use other terms, calling _Y_ the _target_ and _X_ a _feature_ vector. Throughout this book, we will use the terms _predictor_ and _feature_ interchangeably.

Consider the scatterplot in [Figure 4-1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#cotton) displaying the number of years a worker was exposed to cotton dust (`Exposure`) versus a measure of lung capacity (`PEFR` or “peak expiratory flow rate”). How is `PEFR` related to `Exposure`? It’s hard to tell based just on the picture.

![images/lung_scatter.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0401.png)

###### Figure 4-1. Cotton exposure versus lung capacity

Simple linear regression tries to find the “best” line to predict the response `PEFR` as a function of the predictor variable `Exposure`:

The `lm` function in _R_ can be used to fit a linear regression:

```
model
```

`lm` stands for _linear model_, and the `~` symbol denotes that `PEFR` is predicted by `Exposure`. With this model definition, the intercept is automatically included and fitted. If you want to exclude the intercept from the model, you need to write the model definition as follows:

```
PEFR
```

Printing the `model` object produces the following output:

```
Call
```

The intercept, or , is 424.583 and can be interpreted as the predicted `PEFR` for a worker with zero years exposure. The regression coefficient, or , can be interpreted as follows: for each additional year that a worker is exposed to cotton dust, the worker’s `PEFR` measurement is reduced by –4.185.

In _Python_, we can use `LinearRegression` from the `scikit-learn` package. (the `statsmodels` package has a linear regression implementation that is more similar to _R_ (`sm.OLS`); we will use it later in this chapter):

```
predictors
```

The regression line from this model is displayed in [Figure 4-2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#lung_model).

![images/lung_model.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0402.png)

###### Figure 4-2. Slope and intercept for the regression fit to the lung data

## Fitted Values and Residuals

Important concepts in regression analysis are the _fitted values_ (the predictions) and _residuals_ (prediction errors). In general, the data doesn’t fall exactly on a line, so the regression equation should include an explicit error term :

The fitted values, also referred to as the _predicted values_, are typically denoted by  (Y-hat). These are given by:

The notation  and  indicates that the coefficients are estimated versus known.

# Hat Notation: Estimates Versus Known Values

The “hat” notation is used to differentiate between estimates and known values. So the symbol  (“b-hat”) is an estimate of the unknown parameter . Why do statisticians differentiate between the estimate and the true value? The estimate has uncertainty, whereas the true value is fixed.[2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782041419496)

We compute the residuals  by subtracting the _predicted_ values from the original data:

In _R_, we can obtain the fitted values and residuals using the functions `predict` and `residuals`:

```
fitted
```

With `scikit-learn`’s `LinearRegression` model, we use the `predict` method on the training data to get the `fitted` values and subsequently the `residuals`. As we will see, this is a general pattern that all models in `scikit-learn` follow:

```
fitted
```

[Figure 4-3](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#residuals) illustrates the residuals from the regression line fit to the lung data. The residuals are the length of the vertical dashed lines from the data to the line.

![images/lung_residuals.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0403.png)

###### Figure 4-3. Residuals from a regression line (to accommodate all the data, the y-axis scale differs from [Figure 4-2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#lung_model), hence the apparently different slope)

## Least Squares

How is the model fit to the data? When there is a clear relationship, you could imagine fitting the line by hand. In practice, the regression line is the estimate that minimizes the sum of squared residual values, also called the _residual sum of squares_ or _RSS_:

The estimates  and  are the values that minimize RSS.

The method of minimizing the sum of the squared residuals is termed _least squares_ regression, or _ordinary least squares_ (OLS) regression. It is often attributed to Carl Friedrich Gauss, the German mathematician, but was first published by the French mathematician Adrien-Marie Legendre in 1805. Least squares regression can be computed quickly and easily with any standard statistical software.

Historically, computational convenience is one reason for the widespread use of least squares in regression. With the advent of big data, computational speed is still an important factor. Least squares, like the mean (see [“Median and Robust Estimates”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch01.html#Median)), are sensitive to outliers, although this tends to be a significant problem only in small or moderate-sized data sets. See [“Outliers”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#regression_outliers) for a discussion of outliers in regression.

# Regression Terminology

When analysts and researchers use the term _regression_ by itself, they are typically referring to linear regression; the focus is usually on developing a linear model to explain the relationship between predictor variables and a numeric outcome variable. In its formal statistical sense, regression also includes nonlinear models that yield a functional relationship between predictors and outcome variables. In the machine learning community, the term is also occasionally used loosely to refer to the use of any predictive model that produces a predicted numeric outcome (as opposed to classification methods that predict a binary or categorical outcome).

## Prediction Versus Explanation (Profiling)

Historically, a primary use of regression was to illuminate a supposed linear relationship between predictor variables and an outcome variable. The goal has been to understand a relationship and explain it using the data that the regression was fit to. In this case, the primary focus is on the estimated slope of the regression equation, . Economists want to know the relationship between consumer spending and GDP growth. Public health officials might want to understand whether a public information campaign is effective in promoting safe sex practices. In such cases, the focus is not on predicting individual cases but rather on understanding the overall relationship among variables.

With the advent of big data, regression is widely used to form a model to predict individual outcomes for new data (i.e., a predictive model) rather than explain data in hand. In this instance, the main items of interest are the fitted values . In marketing, regression can be used to predict the change in revenue in response to the size of an ad campaign. Universities use regression to predict students’ GPA based on their SAT scores.

A regression model that fits the data well is set up such that changes in _X_ lead to changes in _Y_. However, by itself, the regression equation does not prove the direction of causation. Conclusions about causation must come from a broader understanding about the relationship. For example, a regression equation might show a definite relationship between number of clicks on a web ad and number of conversions. It is our knowledge of the marketing process, not the regression equation, that leads us to the conclusion that clicks on the ad lead to sales, and not vice versa.

##### Key Ideas

- The regression equation models the relationship between a response variable _Y_ and a predictor variable _X_ as a line.
    
- A regression model yields fitted values and residuals—predictions of the response and the errors of the predictions.
    
- Regression models are typically fit by the method of least squares.
    
- Regression is used both for prediction and explanation.
    

## Further Reading

For an in-depth treatment of prediction versus explanation, see Galit Shmueli’s article [“To Explain or to Predict?”](https://oreil.ly/4fVUY).

# Multiple Linear Regression

When there are multiple predictors, the equation is simply extended to accommodate them:

Instead of a line, we now have a linear model—the relationship between each coefficient and its variable (feature) is linear.

##### Key Terms for Multiple Linear Regression

**_Root mean squared error_**

The square root of the average squared error of the regression (this is the most widely used metric to compare regression models).

Synonym

RMSE

**_Residual standard error_**

The same as the root mean squared error, but adjusted for degrees of freedom.

Synonym

RSE

**_R-squared_**

The proportion of variance explained by the model, from 0 to 1.

Synonyms

coefficient of determination, 

**_t-statistic_**

The coefficient for a predictor, divided by the standard error of the coefficient, giving a metric to compare the importance of variables in the model. See [“t-Tests”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#tTest).

**_Weighted regression_**

Regression with the records having different weights.

All of the other concepts in simple linear regression, such as fitting by least squares and the definition of fitted values and residuals, extend to the multiple linear regression setting. For example, the fitted values are given by:

## Example: King County Housing Data

An example of using multiple linear regression is in estimating the value of houses. County assessors must estimate the value of a house for the purposes of assessing taxes. Real estate professionals and home buyers consult popular websites such as [Zillow](https://zillow.com/) to ascertain a fair price. Here are a few rows of housing data from King County (Seattle), Washington, from the `house data.frame`:

```
head
```

The `head` method of `pandas` data frame lists the top rows:

```
subset
```

The goal is to predict the sales price from the other variables. The `lm` function handles the multiple regression case simply by including more terms on the righthand side of the equation; the argument `na.action=na.omit` causes the model to drop records that have missing values:

```
house_lm
```

`scikit-learn`’s `LinearRegression` can be used for multiple linear regression as well:

```
predictors
```

Printing `house_lm` object produces the following output:

```
house_lm
```

For a `LinearRegression` model, intercept and coefficients are the fields `intercept_` and `coef_` of the fitted model:

```
print
```

The interpretation of the coefficients is as with simple linear regression: the predicted value  changes by the coefficient  for each unit change in  assuming all the other variables,  for , remain the same. For example, adding an extra finished square foot to a house increases the estimated value by roughly $229; adding 1,000 finished square feet implies the value will increase by $228,800.

## Assessing the Model

The most important performance metric from a data science perspective is _root mean squared error_, or _RMSE_. RMSE is the square root of the average squared error in the predicted  values:

This measures the overall accuracy of the model and is a basis for comparing it to other models (including models fit using machine learning techniques). Similar to RMSE is the _residual standard error_, or _RSE_. In this case we have _p_ predictors, and the RSE is given by:

The only difference is that the denominator is the degrees of freedom, as opposed to number of records (see [“Degrees of Freedom”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#DOF)). In practice, for linear regression, the difference between RMSE and RSE is very small, particularly for big data applications.

The `summary` function in _R_ computes RSE as well as other metrics for a regression model:

```
summary
```

`scikit-learn` provides a number of metrics for regression and classification. Here, we use `mean_squared_error` to get RMSE and `r2_score` for the coefficient of determination:

```
fitted
```

Use `statsmodels` to get a more detailed analysis of the regression model in _Python_:

```
model
```

The `pandas` method `assign`, as used here, adds a constant column with value 1 to the predictors. This is required to model the intercept.

Another useful metric that you will see in software output is the _coefficient of determination_, also called the _R-squared_ statistic or . R-squared ranges from 0 to 1 and measures the proportion of variation in the data that is accounted for in the model. It is useful mainly in explanatory uses of regression where you want to assess how well the model fits the data. The formula for  is:

The denominator is proportional to the variance of _Y_. The output from _R_ also reports an _adjusted R-squared_, which adjusts for the degrees of freedom, effectively penalizing the addition of more predictors to a model. Seldom is this significantly different from _R-squared_ in multiple regression with large data sets.

Along with the estimated coefficients, _R_ and `statsmodels` report the standard error of the coefficients (SE) and a _t-statistic_:

The t-statistic—and its mirror image, the p-value—measures the extent to which a coefficient is “statistically significant”—that is, outside the range of what a random chance arrangement of predictor and target variable might produce. The higher the t-statistic (and the lower the p-value), the more significant the predictor. Since parsimony is a valuable model feature, it is useful to have a tool like this to guide choice of variables to include as predictors (see [“Model Selection and Stepwise Regression”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#StepwiseRegression)).

###### Warning

In addition to the t-statistic, _R_ and other packages will often report a _p-value_ (`Pr(>|t|)` in the _R_ output) and _F-statistic_. Data scientists do not generally get too involved with the interpretation of these statistics, nor with the issue of statistical significance. Data scientists primarily focus on the t-statistic as a useful guide for whether to include a predictor in a model or not. High t-statistics (which go with p-values near 0) indicate a predictor should be retained in a model, while very low t-statistics indicate a predictor could be dropped. See [“p-Value”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html#p-value) for more discussion.

## Cross-Validation

Classic statistical regression metrics (_R2_, F-statistics, and p-values) are all “in-sample” metrics—they are applied to the same data that was used to fit the model. Intuitively, you can see that it would make a lot of sense to set aside some of the original data, not use it to fit the model, and then apply the model to the set-aside (holdout) data to see how well it does. Normally, you would use a majority of the data to fit the model and use a smaller portion to test the model.

This idea of “out-of-sample” validation is not new, but it did not really take hold until larger data sets became more prevalent; with a small data set, analysts typically want to use all the data and fit the best possible model.

Using a holdout sample, though, leaves you subject to some uncertainty that arises simply from variability in the small holdout sample. How different would the assessment be if you selected a different holdout sample?

Cross-validation extends the idea of a holdout sample to multiple sequential holdout samples. The algorithm for basic _k-fold cross-validation_ is as follows:

1. Set aside _1/k_ of the data as a holdout sample.
    
2. Train the model on the remaining data.
    
3. Apply (score) the model to the _1/k_ holdout, and record needed model assessment metrics.
    
4. Restore the first _1/k_ of the data, and set aside the next _1/k_ (excluding any records that got picked the first time).
    
5. Repeat steps 2 and 3.
    
6. Repeat until each record has been used in the holdout portion.
    
7. Average or otherwise combine the model assessment metrics.
    

The division of the data into the training sample and the holdout sample is also called a _fold_.

## Model Selection and Stepwise Regression

In some problems, many variables could be used as predictors in a regression. For example, to predict house value, additional variables such as the basement size or year built could be used. In _R_, these are easy to add to the regression equation:

```
house_full
```

In _Python_, we need to convert the categorical and boolean variables into numbers:

```
predictors
```

Adding more variables, however, does not necessarily mean we have a better model. Statisticians use the principle of _Occam’s razor_ to guide the choice of a model: all things being equal, a simpler model should be used in preference to a more complicated model.

Including additional variables always reduces RMSE and increases  for the training data. Hence, these are not appropriate to help guide the model choice. One approach to including model complexity is to use the adjusted :

Here, _n_ is the number of records and _P_ is the number of variables in the model.

In the 1970s, Hirotugu Akaike, the eminent Japanese statistician, developed a metric called _AIC_ (Akaike’s Information Criteria) that penalizes adding terms to a model. In the case of regression, AIC has the form:

- AIC = 2_P_ + _n_ log(`RSS`/_n_)

where _P_ is the number of variables and _n_ is the number of records. The goal is to find the model that minimizes AIC; models with _k_ more extra variables are penalized by 2_k_.

# AIC, BIC, and Mallows Cp

The formula for AIC may seem a bit mysterious, but in fact it is based on asymptotic results in information theory. There are several variants to AIC:

AICc

A version of AIC corrected for small sample sizes.

BIC or Bayesian information criteria

Similar to AIC, with a stronger penalty for including additional variables to the model.

Mallows Cp

A variant of AIC developed by Colin Mallows.

These are typically reported as in-sample metrics (i.e., on the training data), and data scientists using holdout data for model assessment do not need to worry about the differences among them or the underlying theory behind them.

How do we find the model that minimizes AIC or maximizes adjusted ? One way is to search through all possible models, an approach called _all subset regression_. This is computationally expensive and is not feasible for problems with large data and many variables. An attractive alternative is to use _stepwise regression_. It could start with a full model and successively drop variables that don’t contribute meaningfully. This is called _backward elimination_. Alternatively one could start with a constant model and successively add variables (_forward selection_). As a third option we can also successively add and drop predictors to find a model that lowers AIC or adjusted . The `MASS` in _R_ package by Venebles and Ripley offers a stepwise regression function called `stepAIC`:

```
library
```

`scikit-learn` has no implementation for stepwise regression. We implemented functions `stepwise_selection`, `forward_selection`, and `backward_elimination` in our `dmba` package:

```
y
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/1.png)](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#co_regression_and_prediction_CO1-1)

Define a function that returns a fitted model for a given set of variables.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/2.png)](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#co_regression_and_prediction_CO1-2)

Define a function that returns a score for a given model and set of variables. In this case, we use the `AIC_score` implemented in the `dmba` package.

The function chose a model in which several variables were dropped from `house_full`: `SqFtLot`, `NbrLivingUnits`, `YrRenovated`, and `NewConstruction`.

Simpler yet are _forward selection_ and _backward selection_. In forward selection, you start with no predictors and add them one by one, at each step adding the predictor that has the largest contribution to , and stopping when the contribution is no longer statistically significant. In backward selection, or _backward elimination_, you start with the full model and take away predictors that are not statistically significant until you are left with a model in which all predictors are statistically significant.

_Penalized regression_ is similar in spirit to AIC. Instead of explicitly searching through a discrete set of models, the model-fitting equation incorporates a constraint that penalizes the model for too many variables (parameters). Rather than eliminating predictor variables entirely—as with stepwise, forward, and backward selection—penalized regression applies the penalty by reducing coefficients, in some cases to near zero. Common penalized regression methods are _ridge regression_ and _lasso regression_.

Stepwise regression and all subset regression are _in-sample_ methods to assess and tune models. This means the model selection is possibly subject to overfitting (fitting the noise in the data) and may not perform as well when applied to new data. One common approach to avoid this is to use cross-validation to validate the models. In linear regression, overfitting is typically not a major issue, due to the simple (linear) global structure imposed on the data. For more sophisticated types of models, particularly iterative procedures that respond to local data structure, cross-validation is a very important tool; see [“Cross-Validation”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#CrossValidation) for details.

## Weighted Regression

Weighted regression is used by statisticians for a variety of purposes; in particular, it is important for analysis of complex surveys. Data scientists may find weighted regression useful in two cases:

- Inverse-variance weighting when different observations have been measured with different precision; the higher variance ones receiving lower weights.
    
- Analysis of data where rows represent multiple cases; the weight variable encodes how many original observations each row represents.
    

For example, with the housing data, older sales are less reliable than more recent sales. Using the `DocumentDate` to determine the year of the sale, we can compute a `Weight` as the number of years since 2005 (the beginning of the data):

_R_

```
library
```

_Python_

```
house
```

We can compute a weighted regression with the `lm` function using the `weight` argument:

```
house_wt
```

The coefficients in the weighted regression are slightly different from the original regression.

Most models in `scikit-learn` accept weights as the keyword argument `sample_weight` in the call of the `fit` method:

```
predictors
```

##### Key Ideas

- Multiple linear regression models the relationship between a response variable _Y_ and multiple predictor variables .
    
- The most important metrics to evaluate a model are root mean squared error (RMSE) and R-squared (_R_2).
    
- The standard error of the coefficients can be used to measure the reliability of a variable’s contribution to a model.
    
- Stepwise regression is a way to automatically determine which variables should be included in the model.
    
- Weighted regression is used to give certain records more or less weight in fitting the equation.
    

## Further Reading

An excellent treatment of cross-validation and resampling can be found in _An Introduction to Statistical Learning_ by Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani (Springer, 2013).

# Prediction Using Regression

The primary purpose of regression in data science is prediction. This is useful to keep in mind, since regression, being an old and established statistical method, comes with baggage that is more relevant to its traditional role as a tool for explanatory modeling than to prediction.

##### Key Terms for Prediction Using Regression

**_Prediction interval_**

An uncertainty interval around an individual predicted value.

**_Extrapolation_**

Extension of a model beyond the range of the data used to fit it.

## The Dangers of Extrapolation

Regression models should not be used to extrapolate beyond the range of the data (leaving aside the use of regression for time series forecasting.). The model is valid only for predictor values for which the data has sufficient values (even in the case that sufficient data is available, there could be other problems—see [“Regression Diagnostics”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#RegressionDiagnostics)). As an extreme case, suppose `model_lm` is used to predict the value of a 5,000-square-foot empty lot. In such a case, all the predictors related to the building would have a value of 0, and the regression equation would yield an absurd prediction of –521,900 + 5,000 × –.0605 = –$522,202. Why did this happen? The data contains only parcels with buildings—there are no records corresponding to vacant land. Consequently, the model has no information to tell it how to predict the sales price for vacant land.

## Confidence and Prediction Intervals

Much of statistics involves understanding and measuring variability (uncertainty). The t-statistics and p-values reported in regression output deal with this in a formal way, which is sometimes useful for variable selection (see [“Assessing the Model”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#RMSE)). More useful metrics are confidence intervals, which are uncertainty intervals placed around regression coefficients and predictions. An easy way to understand this is via the bootstrap (see [“The Bootstrap”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch02.html#bootstrap) for more details about the general bootstrap procedure). The most common regression confidence intervals encountered in software output are those for regression parameters (coefficients). Here is a bootstrap algorithm for generating confidence intervals for regression parameters (coefficients) for a data set with _P_ predictors and _n_ records (rows):

1. Consider each row (including outcome variable) as a single “ticket” and place all the _n_ tickets in a box.
    
2. Draw a ticket at random, record the values, and replace it in the box.
    
3. Repeat step 2 _n_ times; you now have one bootstrap resample.
    
4. Fit a regression to the bootstrap sample, and record the estimated coefficients.
    
5. Repeat steps 2 through 4, say, 1,000 times.
    
6. You now have 1,000 bootstrap values for each coefficient; find the appropriate percentiles for each one (e.g., 5th and 95th for a 90% confidence interval).
    

You can use the `Boot` function in _R_ to generate actual bootstrap confidence intervals for the coefficients, or you can simply use the formula-based intervals that are a routine _R_ output. The conceptual meaning and interpretation are the same, and not of central importance to data scientists, because they concern the regression coefficients. Of greater interest to data scientists are intervals around predicted _y_ values (). The uncertainty around  comes from two sources:

- Uncertainty about what the relevant predictor variables and their coefficients are (see the preceding bootstrap algorithm)
    
- Additional error inherent in individual data points
    

The individual data point error can be thought of as follows: even if we knew for certain what the regression equation was (e.g., if we had a huge number of records to fit it), the _actual_ outcome values for a given set of predictor values will vary. For example, several houses—each with 8 rooms, a 6,500-square-foot lot, 3 bathrooms, and a basement—might have different values. We can model this individual error with the residuals from the fitted values. The bootstrap algorithm for modeling both the regression model error and the individual data point error would look as follows:

1. Take a bootstrap sample from the data (spelled out in greater detail earlier).
    
2. Fit the regression, and predict the new value.
    
3. Take a single residual at random from the original regression fit, add it to the predicted value, and record the result.
    
4. Repeat steps 1 through 3, say, 1,000 times.
    
5. Find the 2.5th and the 97.5th percentiles of the results.
    

##### Key Ideas

- Extrapolation beyond the range of the data can lead to error.
    
- Confidence intervals quantify uncertainty around regression coefficients.
    
- Prediction intervals quantify uncertainty in individual predictions.
    
- Most software, _R_ included, will produce prediction and confidence intervals in default or specified output, using formulas.
    
- The bootstrap can also be used to produce prediction and confidence intervals; the interpretation and idea are the same.
    

# Prediction Interval or Confidence Interval?

A prediction interval pertains to uncertainty around a single value, while a confidence interval pertains to a mean or other statistic calculated from multiple values. Thus, a prediction interval will typically be much wider than a confidence interval for the same value. We model this individual value error in the bootstrap model by selecting an individual residual to tack on to the predicted value. Which should you use? That depends on the context and the purpose of the analysis, but, in general, data scientists are interested in specific individual predictions, so a prediction interval would be more appropriate. Using a confidence interval when you should be using a prediction interval will greatly underestimate the uncertainty in a given predicted value.

# Factor Variables in Regression

_Factor_ variables, also termed _categorical_ variables, take on a limited number of discrete values. For example, a loan purpose can be “debt consolidation,” “wedding,” “car,” and so on. The binary (yes/no) variable, also called an _indicator_ variable, is a special case of a factor variable. Regression requires numerical inputs, so factor variables need to be recoded to use in the model. The most common approach is to convert a variable into a set of binary _dummy_ variables.

##### Key Terms for Factor Variables

**_Dummy variables_**

Binary 0–1 variables derived by recoding factor data for use in regression and other models.

**_Reference coding_**

The most common type of coding used by statisticians, in which one level of a factor is used as a reference and other factors are compared to that level.

Synonym

treatment coding

**_One hot encoder_**

A common type of coding used in the machine learning community in which all factor levels are retained. While useful for certain machine learning algorithms, this approach is not appropriate for multiple linear regression.

**_Deviation coding_**

A type of coding that compares each level against the overall mean as opposed to the reference level.

Synonym

sum contrasts

## Dummy Variables Representation

In the King County housing data, there is a factor variable for the property type; a small subset of six records is shown below:

_R_:

```
head
```

_Python_:

```
house
```

There are three possible values: `Multiplex`, `Single Family`, and `Townhouse`. To use this factor variable, we need to convert it to a set of binary variables. We do this by creating a binary variable for each possible value of the factor variable. To do this in _R_, we use the `model.matrix` function:[3](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782039140376)

```
prop_type_dummies
```

The function `model.matrix` converts a data frame into a matrix suitable to a linear model. The factor variable `PropertyType`, which has three distinct levels, is represented as a matrix with three columns. In the machine learning community, this representation is referred to as _one hot encoding_ (see [“One Hot Encoder”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch06.html#OneHotEncoder)).

In _Python_, we can convert categorical variables to dummies using the `pandas` method `get_dummies`:

```
pd
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/1.png)](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#co_regression_and_prediction_CO2-1)

By default, returns one hot encoding of the categorical variable.

[![2](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/2.png)](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#co_regression_and_prediction_CO2-2)

The keyword argument `drop_first` will return _P_ – 1 columns. Use this to avoid the problem of multicollinearity.

In certain machine learning algorithms, such as nearest neighbors and tree models, one hot encoding is the standard way to represent factor variables (for example, see [“Tree Models”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch06.html#TreeModels)).

In the regression setting, a factor variable with _P_ distinct levels is usually represented by a matrix with only _P_ – 1 columns. This is because a regression model typically includes an intercept term. With an intercept, once you have defined the values for _P_ – 1 binaries, the value for the _P_th is known and could be considered redundant. Adding the _P_th column will cause a multicollinearity error (see [“Multicollinearity”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#Multicollinearity)).

The default representation in _R_ is to use the first factor level as a _reference_ and interpret the remaining levels relative to that factor:

```
lm
```

The method `get_dummies` takes the optional keyword argument `drop_first` to exclude the first factor as _reference_:

```
predictors
```

The output from the _R_ regression shows two coefficients corresponding to `PropertyType`: `PropertyTypeSingle Family` and `PropertyTypeTownhouse`. There is no coefficient of `Multiplex` since it is implicitly defined when `PropertyTypeSingle Family == 0` and `PropertyTypeTownhouse == 0`. The coefficients are interpreted as relative to `Multiplex`, so a home that is `Single Family` is worth almost $85,000 less, and a home that is `Townhouse` is worth over $150,000 less.[4](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782038718424)

# Different Factor Codings

There are several different ways to encode factor variables, known as _contrast coding_ systems. For example, _deviation coding_, also known as _sum contrasts_, compares each level against the overall mean. Another contrast is _polynomial coding_, which is appropriate for ordered factors; see the section [“Ordered Factor Variables”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#OrderedFactorsRegression). With the exception of ordered factors, data scientists will generally not encounter any type of coding besides reference coding or one hot encoder.

## Factor Variables with Many Levels

Some factor variables can produce a huge number of binary dummies—zip codes are a factor variable, and there are 43,000 zip codes in the US. In such cases, it is useful to explore the data, and the relationships between predictor variables and the outcome, to determine whether useful information is contained in the categories. If so, you must further decide whether it is useful to retain all factors, or whether the levels should be consolidated.

In King County, there are 80 zip codes with a house sale:

```
table
```

The `value_counts` method of `pandas` data frames returns the same information:

```
pd
```

`ZipCode` is an important variable, since it is a proxy for the effect of location on the value of a house. Including all levels requires 79 coefficients corresponding to 79 degrees of freedom. The original model `house_lm` has only 5 degrees of freedom; see [“Assessing the Model”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#RMSE). Moreover, several zip codes have only one sale. In some problems, you can consolidate a zip code using the first two or three digits, corresponding to a submetropolitan geographic region. For King County, almost all of the sales occur in 980xx or 981xx, so this doesn’t help.

An alternative approach is to group the zip codes according to another variable, such as sale price. Even better is to form zip code groups using the residuals from an initial model. The following `dplyr` code in _R_ consolidates the 80 zip codes into five groups based on the median of the residual from the `house_lm` regression:

```
zip_groups
```

The median residual is computed for each zip, and the `ntile` function is used to split the zip codes, sorted by the median, into five groups. See [“Confounding Variables”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#ConfoundingVariables) for an example of how this is used as a term in a regression improving upon the original fit.

In _Python_ we can calculate this information as follows:

```
zip_groups
```

The concept of using the residuals to help guide the regression fitting is a fundamental step in the modeling process; see [“Regression Diagnostics”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#RegressionDiagnostics).

## Ordered Factor Variables

Some factor variables reflect levels of a factor; these are termed _ordered factor variables_ or _ordered categorical variables_. For example, the loan grade could be A, B, C, and so on—each grade carries more risk than the prior grade. Often, ordered factor variables can be converted to numerical values and used as is. For example, the variable `BldgGrade` is an ordered factor variable. Several of the types of grades are shown in [Table 4-1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#BldgGrade). While the grades have specific meaning, the numeric value is ordered from low to high, corresponding to higher-grade homes. With the regression model `house_lm`, fit in [“Multiple Linear Regression”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#MultipleLinearRegression), `BldgGrade` was treated as a numeric variable.

Table 4-1. Building grades and numeric equivalents
|Value|Description|
|---|---|
|1|Cabin|
|2|Substandard|
|5|Fair|
|10|Very good|
|12|Luxury|
|13|Mansion|

Treating ordered factors as a numeric variable preserves the information contained in the ordering that would be lost if it were converted to a factor.

##### Key Ideas

- Factor variables need to be converted into numeric variables for use in a regression.
    
- The most common method to encode a factor variable with P distinct values is to represent them using P – 1 dummy variables.
    
- A factor variable with many levels, even in very big data sets, may need to be consolidated into a variable with fewer levels.
    
- Some factors have levels that are ordered and can be represented as a single numeric variable.
    

# Interpreting the Regression Equation

In data science, the most important use of regression is to predict some dependent (outcome) variable. In some cases, however, gaining insight from the equation itself to understand the nature of the relationship between the predictors and the outcome can be of value. This section provides guidance on examining the regression equation and interpreting it.

##### Key Terms for Interpreting the Regression Equation

**_Correlated variables_**

Variables that tend to move in the same direction—when one goes up so does the other, and vice-versa (with negative correlation, when one goes up the other does down). When the predictor variables are highly correlated, it is difficult to interpret the individual coefficients.

**_Multicollinearity_**

When the predictor variables have perfect, or near-perfect, correlation, the regression can be unstable or impossible to compute.

Synonym

collinearity

**_Confounding variables_**

An important predictor that, when omitted, leads to spurious relationships in a regression equation.

**_Main effects_**

The relationship between a predictor and the outcome variable, independent of other variables.

**_Interactions_**

An interdependent relationship between two or more predictors and the response.

## Correlated Predictors

In multiple regression, the predictor variables are often correlated with each other. As an example, examine the regression coefficients for the model `step_lm`, fit in [“Model Selection and Stepwise Regression”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#StepwiseRegression).

_R_:

```
step_lm
```

_Python_:

```
print
```

The coefficient for `Bedrooms` is negative! This implies that adding a bedroom to a house will reduce its value. How can this be? This is because the predictor variables are correlated: larger houses tend to have more bedrooms, and it is the size that drives house value, not the number of bedrooms. Consider two homes of the exact same size: it is reasonable to expect that a home with more but smaller bedrooms would be considered less desirable.

Having correlated predictors can make it difficult to interpret the sign and value of regression coefficients (and can inflate the standard error of the estimates). The variables for bedrooms, house size, and number of bathrooms are all correlated. This is illustrated by the following example in _R_, which fits another regression removing the variables `SqFtTotLiving`, `SqFtFinBasement`, and `Bathrooms` from the equation:

```
update
```

The `update` function can be used to add or remove variables from a model. Now the coefficient for bedrooms is positive—in line with what we would expect (though it is really acting as a proxy for house size, now that those variables have been removed).

In _Python_, there is no equivalent to _R_’s `update` function. We need to refit the model with the modified predictor list:

```
predictors
```

Correlated variables are only one issue with interpreting regression coefficients. In `house_lm`, there is no variable to account for the location of the home, and the model is mixing together very different types of regions. Location may be a _confounding_ variable; see [“Confounding Variables”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#ConfoundingVariables) for further discussion.

## Multicollinearity

An extreme case of correlated variables produces multicollinearity—a condition in which there is redundance among the predictor variables. Perfect multicollinearity occurs when one predictor variable can be expressed as a linear combination of others. Multicollinearity occurs when:

- A variable is included multiple times by error.
    
- _P_ dummies, instead of _P_ – 1 dummies, are created from a factor variable (see [“Factor Variables in Regression”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#FactorsRegression)).
    
- Two variables are nearly perfectly correlated with one another.
    

Multicollinearity in regression must be addressed—variables should be removed until the multicollinearity is gone. A regression does not have a well-defined solution in the presence of perfect multicollinearity. Many software packages, including _R_ and _Python_, automatically handle certain types of multicollinearity. For example, if `SqFtTotLiving` is included twice in the regression of the `house` data, the results are the same as for the `house_lm` model. In the case of nonperfect multicollinearity, the software may obtain a solution, but the results may be unstable.

###### Note

Multicollinearity is not such a problem for nonlinear regression methods like trees, clustering, and nearest-neighbors, and in such methods it may be advisable to retain _P_ dummies (instead of _P_ – 1). That said, even in those methods, nonredundancy in predictor variables is still a virtue.

## Confounding Variables

With correlated variables, the problem is one of commission: including different variables that have a similar predictive relationship with the response. With _confounding variables_, the problem is one of omission: an important variable is not included in the regression equation. Naive interpretation of the equation coefficients can lead to invalid conclusions.

Take, for example, the King County regression equation `house_lm` from [“Example: King County Housing Data”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#KingCountyHousingData). The regression coefficients of `SqFtLot`, `Bathrooms`, and `Bedrooms` are all negative. The original regression model does not contain a variable to represent location—a very important predictor of house price. To model location, include a variable `ZipGroup` that categorizes the zip code into one of five groups, from least expensive (1) to most expensive (5):[5](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782037780856)

```
lm
```

The same model in _Python_:

```
predictors
```

`ZipGroup` is clearly an important variable: a home in the most expensive zip code group is estimated to have a higher sales price by almost $340,000. The coefficients of `SqFtLot` and `Bathrooms` are now positive, and adding a bathroom increases the sale price by $5,928.

The coefficient for `Bedrooms` is still negative. While this is unintuitive, this is a well-known phenomenon in real estate. For homes of the same livable area and number of bathrooms, having more and therefore smaller bedrooms is associated with less valuable homes.

## Interactions and Main Effects

Statisticians like to distinguish between _main effects_, or independent variables, and the _interactions_ between the main effects. Main effects are what are often referred to as the _predictor variables_ in the regression equation. An implicit assumption when only main effects are used in a model is that the relationship between a predictor variable and the response is independent of the other predictor variables. This is often not the case.

For example, the model fit to the King County Housing Data in [“Confounding Variables”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#ConfoundingVariables) includes several variables as main effects, including `ZipCode`. Location in real estate is everything, and it is natural to presume that the relationship between, say, house size and the sale price depends on location. A big house built in a low-rent district is not going to retain the same value as a big house built in an expensive area. You include interactions between variables in _R_ using the `*` operator. For the King County data, the following fits an interaction between `SqFtTotLiving` and `ZipGroup`:

```
lm
```

The resulting model has four new terms: `SqFtTotLiving:ZipGroup2`, `SqFtTotLiving:ZipGroup3`, and so on.

In _Python_, we need to use the `statsmodels` package to train linear regression models with interactions. This package was designed similar to _R_ and allows defining models using a formula interface:

```
model
```

The `statsmodels` package takes care of categorical variables (e.g., `ZipGroup[T.1]`, `PropertyType[T.Single Family]`) and interaction terms (e.g., `SqFtTotLiving:ZipGroup[T.1]`).

Location and house size appear to have a strong interaction. For a home in the lowest `ZipGroup`, the slope is the same as the slope for the main effect `SqFtTotLiving`, which is $118 per square foot (this is because _R_ uses _reference_ coding for factor variables; see [“Factor Variables in Regression”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#FactorsRegression)). For a home in the highest `ZipGroup`, the slope is the sum of the main effect plus `SqFtTotLiving:ZipGroup5`, or $115 + $227 = $342 per square foot. In other words, adding a square foot in the most expensive zip code group boosts the predicted sale price by a factor of almost three, compared to the average boost from adding a square foot.

# Model Selection with Interaction Terms

In problems involving many variables, it can be challenging to decide which interaction terms should be included in the model. Several different approaches are commonly taken:

- In some problems, prior knowledge and intuition can guide the choice of which interaction terms to include in the model.
    
- Stepwise selection (see [“Model Selection and Stepwise Regression”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#StepwiseRegression)) can be used to sift through the various models.
    
- Penalized regression can automatically fit to a large set of possible interaction terms.
    
- Perhaps the most common approach is to use _tree models_, as well as their descendants, _random forest_ and _gradient boosted trees_. This class of models automatically searches for optimal interaction terms; see [“Tree Models”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch06.html#TreeModels).
    

##### Key Ideas

- Because of correlation between predictors, care must be taken in the interpretation of the coefficients in multiple linear regression.
    
- Multicollinearity can cause numerical instability in fitting the regression equation.
    
- A confounding variable is an important predictor that is omitted from a model and can lead to a regression equation with spurious relationships.
    
- An interaction term between two variables is needed if the relationship between the variables and the response is interdependent.
    

# Regression Diagnostics

In explanatory modeling (i.e., in a research context), various steps, in addition to the metrics mentioned previously (see [“Assessing the Model”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#RMSE)), are taken to assess how well the model fits the data; most are based on analysis of the residuals. These steps do not directly address predictive accuracy, but they can provide useful insight in a predictive setting.

##### Key Terms for Regression Diagnostics

**_Standardized residuals_**

Residuals divided by the standard error of the residuals.

**_Outliers_**

Records (or outcome values) that are distant from the rest of the data (or the predicted outcome).

**_Influential value_**

A value or record whose presence or absence makes a big difference in the regression equation.

**_Leverage_**

The degree of influence that a single record has on a regression equation.

Synonym

hat-value

**_Non-normal residuals_**

Non-normally distributed residuals can invalidate some technical requirements of regression but are usually not a concern in data science.

**_Heteroskedasticity_**

When some ranges of the outcome experience residuals with higher variance (may indicate a predictor missing from the equation).

**_Partial residual plots_**

A diagnostic plot to illuminate the relationship between the outcome variable and a single predictor.

Synonym

added variables plot

## Outliers

Generally speaking, an extreme value, also called an _outlier_, is one that is distant from most of the other observations. Just as outliers need to be handled for estimates of location and variability (see [“Estimates of Location”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch01.html#Location) and [“Estimates of Variability”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch01.html#Variability)), outliers can cause problems with regression models. In regression, an outlier is a record whose actual _y_ value is distant from the predicted value. You can detect outliers by examining the _standardized residual_, which is the residual divided by the standard error of the residuals.

There is no statistical theory that separates outliers from nonoutliers. Rather, there are (arbitrary) rules of thumb for how distant from the bulk of the data an observation needs to be in order to be called an outlier. For example, with the boxplot, outliers are those data points that are too far above or below the box boundaries (see [“Percentiles and Boxplots”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch01.html#Boxplots)), where “too far” = “more than 1.5 times the interquartile range.” In regression, the standardized residual is the metric that is typically used to determine whether a record is classified as an outlier. Standardized residuals can be interpreted as “the number of standard errors away from the regression line.”

Let’s fit a regression to the King County house sales data for all sales in zip code 98105 in _R_:

```
house_98105
```

In _Python_:

```
house_98105
```

We extract the standardized residuals in _R_ using the `rstandard` function and obtain the index of the smallest residual using the `order` function:

```
sresid
```

In `statsmodels`, use `OLSInfluence` to analyze the residuals:

```
influence
```

The biggest overestimate from the model is more than four standard errors above the regression line, corresponding to an overestimate of $757,754. The original data record corresponding to this outlier is as follows in _R_:

```
house_98105
```

In _Python_:

```
outlier
```

In this case, it appears that there is something wrong with the record: a house of that size typically sells for much more than $119,748 in that zip code. [Figure 4-4](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#StatutoryDeed) shows an excerpt from the statutory deed from this sale: it is clear that the sale involved only partial interest in the property. In this case, the outlier corresponds to a sale that is anomalous and should not be included in the regression. Outliers could also be the result of other problems, such as a “fat-finger” data entry or a mismatch of units (e.g., reporting a sale in thousands of dollars rather than simply in dollars).

![Statutory warranty deed for the largest negative residual](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0404.png)

###### Figure 4-4. Statutory warrany deed for the largest negative residual

For big data problems, outliers are generally not a problem in fitting the regression to be used in predicting new data. However, outliers are central to anomaly detection, where finding outliers is the whole point. The outlier could also correspond to a case of fraud or an accidental action. In any case, detecting outliers can be a critical business need.

## Influential Values

A value whose absence would significantly change the regression equation is termed an _influential observation_. In regression, such a value need not be associated with a large residual. As an example, consider the regression lines in [Figure 4-5](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#InfluenceExample). The solid line corresponds to the regression with all the data, while the dashed line corresponds to the regression with the point in the upper-right corner removed. Clearly, that data value has a huge influence on the regression even though it is not associated with a large outlier (from the full regression). This data value is considered to have high _leverage_ on the regression.

In addition to standardized residuals (see [“Outliers”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#regression_outliers)), statisticians have developed several metrics to determine the influence of a single record on a regression. A common measure of leverage is the _hat-value_; values above  indicate a high-leverage data value.[6](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782036738936)

![An example of an influential data point in regression](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0405.png)

###### Figure 4-5. An example of an influential data point in regression

Another metric is _Cook’s distance_, which defines influence as a combination of leverage and residual size. A rule of thumb is that an observation has high influence if Cook’s distance exceeds .

An _influence plot_ or _bubble plot_ combines standardized residuals, the hat-value, and Cook’s distance in a single plot. [Figure 4-6](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#InfluencePlot) shows the influence plot for the King County house data and can be created by the following _R_ code:

```
std_resid
```

Here is the _Python_ code to create a similar figure:

```
influence
```

There are apparently several data points that exhibit large influence in the regression. Cook’s distance can be computed using the function `cooks.distance`, and you can use `hatvalues` to compute the diagnostics. The hat values are plotted on the x-axis, the residuals are plotted on the y-axis, and the size of the points is related to the value of Cook’s distance.

![A plot to determine which observations have high influence](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0406.png)

###### Figure 4-6. A plot to determine which observations have high influence; points with Cook’s distance greater than 0.08 are highlighted in grey

[Table 4-2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#InfluenceTable) compares the regression with the full data set and with highly influential data points removed (Cook’s distance > 0.08).

The regression coefficient for `Bathrooms` changes quite dramatically.[7](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782036426552)

Table 4-2. Comparison of regression coefficients with the full data and with influential data removed
||Original|Influential removed|
|---|---|---|
|(Intercept)|–772,550|–647,137|
|SqFtTotLiving|210|230|
|SqFtLot|39|33|
|Bathrooms|2282|–16,132|
|Bedrooms|–26,320|–22,888|
|BldgGrade|130,000|114,871|

For purposes of fitting a regression that reliably predicts future data, identifying influential observations is useful only in smaller data sets. For regressions involving many records, it is unlikely that any one observation will carry sufficient weight to cause extreme influence on the fitted equation (although the regression may still have big outliers). For purposes of anomaly detection, though, identifying influential observations can be very useful.

## Heteroskedasticity, Non-Normality, and Correlated Errors

Statisticians pay considerable attention to the distribution of the residuals. It turns out that ordinary least squares (see [“Least Squares”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#OLS)) are unbiased, and in some cases are the “optimal” estimator, under a wide range of distributional assumptions. This means that in most problems, data scientists do not need to be too concerned with the distribution of the residuals.

The distribution of the residuals is relevant mainly for the validity of formal statistical inference (hypothesis tests and p-values), which is of minimal importance to data scientists concerned mainly with predictive accuracy. Normally distributed errors are a sign that the model is complete; errors that are not normally distributed indicate the model may be missing something. For formal inference to be fully valid, the residuals are assumed to be normally distributed, have the same variance, and be independent. One area where this may be of concern to data scientists is the standard calculation of confidence intervals for predicted values, which are based upon the assumptions about the residuals (see [“Confidence and Prediction Intervals”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#RegressionCIs)).

_Heteroskedasticity_ is the lack of constant residual variance across the range of the predicted values. In other words, errors are greater for some portions of the range than for others. Visualizing the data is a convenient way to analyze residuals.

The following code in _R_ plots the absolute residuals versus the predicted values for the `lm_98105` regression fit in [“Outliers”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#regression_outliers):

```
df
```

[Figure 4-7](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#HouseHetero) shows the resulting plot. Using `geom_smooth`, it is easy to superpose a smooth of the absolute residuals. The function calls the `loess` method (locally estimated scatterplot smoothing) to produce a smoothed estimate of the relationship between the variables on the x-axis and y-axis in a scatterplot (see [“Scatterplot Smoothers”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#ScatterplotSmoothers)).

In _Python_, the `seaborn` package has the `regplot` function to create a similar figure:

```
fig
```

![A plot of the absolute value of the residuals versus the predicted values](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0407.png)

###### Figure 4-7. A plot of the absolute value of the residuals versus the predicted values

Evidently, the variance of the residuals tends to increase for higher-valued homes but is also large for lower-valued homes. This plot indicates that `lm_98105` has _heteroskedastic_ errors.

# Why Would a Data Scientist Care About Heteroskedasticity?

Heteroskedasticity indicates that prediction errors differ for different ranges of the predicted value, and may suggest an incomplete model. For example, the heteroskedasticity in `lm_98105` may indicate that the regression has left something unaccounted for in high- and low-range homes.

[Figure 4-8](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#HistRegression) is a histogram of the standardized residuals for the `lm_98105` regression. The distribution has decidedly longer tails than the normal distribution and exhibits mild skewness toward larger residuals.

![A histogram of the residuals from the regression of the housing data](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0408.png)

###### Figure 4-8. A histogram of the residuals from the regression of the housing data

Statisticians may also check the assumption that the errors are independent. This is particularly true for data that is collected over time or space. The _Durbin-Watson_ statistic can be used to detect if there is significant autocorrelation in a regression involving time series data. If the errors from a regression model are correlated, then this information can be useful in making short-term forecasts and should be built into the model. See _Practical Time Series Forecasting with R_, 2nd ed., by Galit Shmueli and Kenneth Lichtendahl (Axelrod Schnall, 2018) to learn more about how to build autocorrelation information into regression models for time series data. If longer-term forecasts or explanatory models are the goal, excess autocorrelated data at the microlevel may distract. In that case, smoothing, or less granular collection of data in the first place, may be in order.

Even though a regression may violate one of the distributional assumptions, should we care? Most often in data science, the interest is primarily in predictive accuracy, so some review of heteroskedasticity may be in order. You may discover that there is some signal in the data that your model has not captured. However, satisfying distributional assumptions simply for the sake of validating formal statistical inference (p-values, F-statistics, etc.) is not that important for the data scientist.

# Scatterplot Smoothers

Regression is about modeling the relationship between the response and predictor variables. In evaluating a regression model, it is useful to use a _scatterplot smoother_ to visually highlight relationships between two variables.

For example, in [Figure 4-7](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#HouseHetero), a smooth of the relationship between the absolute residuals and the predicted value shows that the variance of the residuals depends on the value of the residual. In this case, the `loess` function was used; `loess` works by repeatedly fitting a series of local regressions to contiguous subsets to come up with a smooth. While `loess` is probably the most commonly used smoother, other scatterplot smoothers are available in _R_, such as super smooth (`supsmu`) and kernel smoothing (`ksmooth`). In _Python_, we can find additional smoothers in `scipy` (`wiener` or `sav`) and `statsmodels` (`kernel_regression`). For the purposes of evaluating a regression model, there is typically no need to worry about the details of these scatterplot smooths.

## Partial Residual Plots and Nonlinearity

_Partial residual plots_ are a way to visualize how well the estimated fit explains the relationship between a predictor and the outcome. The basic idea of a partial residual plot is to isolate the relationship between a predictor variable and the response, _taking into account all of the other predictor variables_. A partial residual might be thought of as a “synthetic outcome” value, combining the prediction based on a single predictor with the actual residual from the full regression equation. A partial residual for predictor  is the ordinary residual plus the regression term associated with :

where  is the estimated regression coefficient. The `predict` function in _R_ has an option to return the individual regression terms :

```
terms
```

The partial residual plot displays the  predictor on the x-axis and the partial residuals on the y-axis. Using `ggplot2` makes it easy to superpose a smooth of the partial residuals:

```
df
```

The `statsmodels` package has the method `sm.graphics.plot_ccpr` that creates a similar partial residual plot:

```
sm
```

The _R_ and _Python_ graphs differ by a constant shift. In _R_, a constant is added so that the mean of the terms is zero.

The resulting plot is shown in [Figure 4-9](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#HousePartialResid). The partial residual is an estimate of the contribution that `SqFtTotLiving` adds to the sales price. The relationship between `SqFtTotLiving` and the sales price is evidently nonlinear (dashed line). The regression line (solid line) underestimates the sales price for homes less than 1,000 square feet and overestimates the price for homes between 2,000 and 3,000 square feet. There are too few data points above 4,000 square feet to draw conclusions for those homes.

![A partial residual plot of for the variable SqFtTotLiving](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0409.png)

###### Figure 4-9. A partial residual plot for the variable `SqFtTotLiving`

This nonlinearity makes sense in this case: adding 500 feet in a small home makes a much bigger difference than adding 500 feet in a large home. This suggests that, instead of a simple linear term for `SqFtTotLiving`, a nonlinear term should be considered (see [“Polynomial and Spline Regression”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#NonlinearTerms)).

##### Key Ideas

- While outliers can cause problems for small data sets, the primary interest with outliers is to identify problems with the data, or locate anomalies.
    
- Single records (including regression outliers) can have a big influence on a regression equation with small data, but this effect washes out in big data.
    
- If the regression model is used for formal inference (p-values and the like), then certain assumptions about the distribution of the residuals should be checked. In general, however, the distribution of residuals is not critical in data science.
    
- The partial residuals plot can be used to qualitatively assess the fit for each regression term, possibly leading to alternative model specification.
    

# Polynomial and Spline Regression

The relationship between the response and a predictor variable isn’t necessarily linear. The response to the dose of a drug is often nonlinear: doubling the dosage generally doesn’t lead to a doubled response. The demand for a product isn’t a linear function of marketing dollars spent; at some point, demand is likely to be saturated. There are many ways that regression can be extended to capture these nonlinear effects.

##### Key Terms for Nonlinear Regression

**_Polynomial regression_**

Adds polynomial terms (squares, cubes, etc.) to a regression.

**_Spline regression_**

Fitting a smooth curve with a series of polynomial segments.

**_Knots_**

Values that separate spline segments.

**_Generalized additive models_**

Spline models with automated selection of knots.

Synonym

GAM

# Nonlinear Regression

When statisticians talk about _nonlinear regression_, they are referring to models that can’t be fit using least squares. What kind of models are nonlinear? Essentially all models where the response cannot be expressed as a linear combination of the predictors or some transform of the predictors. Nonlinear regression models are harder and computationally more intensive to fit, since they require numerical optimization. For this reason, it is generally preferred to use a linear model if possible.

## Polynomial

_Polynomial regression_ involves including polynomial terms in a regression equation. The use of polynomial regression dates back almost to the development of regression itself with a paper by Gergonne in 1815. For example, a quadratic regression between the response _Y_ and the predictor _X_ would take the form:

Polynomial regression can be fit in _R_ through the `poly` function. For example, the following fits a quadratic polynomial for `SqFtTotLiving` with the King County housing data:

```
lm
```

In `statsmodels`, we add the squared term to the model definition using `I(SqFtTotLiving**2)`:

```
model_poly
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/1.png)](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#co_regression_and_prediction_CO3-1)

The intercept and the polynomial coefficients are different compared to _R_. This is due to different implementations. The remaining coefficients and the predictions are equivalent.

There are now two coefficients associated with `SqFtTotLiving`: one for the linear term and one for the quadratic term.

The partial residual plot (see [“Partial Residual Plots and Nonlinearity”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#PartialResidualPlots)) indicates some curvature in the regression equation associated with `SqFtTotLiving`. The fitted line more closely matches the smooth (see [“Splines”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#Splines)) of the partial residuals as compared to a linear fit (see [Figure 4-10](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#PolynomialRegressionPlot)).

The `statsmodels` implementation works only for linear terms. The accompanying source code gives an implementation that will work for polynomial regression as well.

![A polynomial regression fit for the variable SqFtTotLiving (solid line) versus a smooth (dashed line)](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0410.png)

###### Figure 4-10. A polynomial regression fit for the variable `SqFtTotLiving` (solid line) versus a smooth (dashed line; see the following section about splines)

## Splines

Polynomial regression captures only a certain amount of curvature in a nonlinear relationship. Adding in higher-order terms, such as a cubic quartic polynomial, often leads to undesirable “wiggliness” in the regression equation. An alternative, and often superior, approach to modeling nonlinear relationships is to use _splines_. _Splines_ provide a way to smoothly interpolate between fixed points. Splines were originally used by draftsmen to draw a smooth curve, particularly in ship and aircraft building.

The splines were created by bending a thin piece of wood using weights, referred to as “ducks”; see [Figure 4-11](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#SplineDucks).

![Splines were originally created using bendable wood and ``ducks,'' and were used as a draftsman's tool to fit curves. Photo courtesy of Bob Perry.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0411.png)

###### Figure 4-11. Splines were originally created using bendable wood and “ducks” and were used as a draftsman’s tool to fit curves (photo courtesy of Bob Perry)

The technical definition of a spline is a series of piecewise continuous polynomials. They were first developed during World War II at the US Aberdeen Proving Grounds by I. J. Schoenberg, a Romanian mathematician. The polynomial pieces are smoothly connected at a series of fixed points in a predictor variable, referred to as _knots_. Formulation of splines is much more complicated than polynomial regression; statistical software usually handles the details of fitting a spline. The _R_ package `splines` includes the function `bs` to create a _b-spline_ (basis spline) term in a regression model. For example, the following adds a b-spline term to the house regression model:

```
library
```

Two parameters need to be specified: the degree of the polynomial and the location of the knots. In this case, the predictor `SqFtTotLiving` is included in the model using a cubic spline (`degree=3`). By default, `bs` places knots at the boundaries; in addition, knots were also placed at the lower quartile, the median quartile, and the upper quartile.

The `statsmodels` formula interface supports the use of splines in a similar way to _R_. Here, we specify the _b-spline_ using `df`, the degrees of freedom. This will create `df` – `degree` = 6 – 3 = 3 internal knots with positions calculated in the same way as in the _R_ code above:

```
formula
```

In contrast to a linear term, for which the coefficient has a direct meaning, the coefficients for a spline term are not interpretable. Instead, it is more useful to use the visual display to reveal the nature of the spline fit. [Figure 4-12](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#SplineRegressionPlot) displays the partial residual plot from the regression. In contrast to the polynomial model, the spline model more closely matches the smooth, demonstrating the greater flexibility of splines. In this case, the line more closely fits the data. Does this mean the spline regression is a better model? Not necessarily: it doesn’t make economic sense that very small homes (less than 1,000 square feet) would have higher value than slightly larger homes. This is possibly an artifact of a confounding variable; see [“Confounding Variables”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#ConfoundingVariables).

![A spline regression fit for the variable SqFtTotLiving (solid line) compared to a smooth (dashed line)](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0412.png)

###### Figure 4-12. A spline regression fit for the variable `SqFtTotLiving` (solid line) compared to a smooth (dashed line)

## Generalized Additive Models

Suppose you suspect a nonlinear relationship between the response and a predictor variable, either by a priori knowledge or by examining the regression diagnostics. Polynomial terms may not be flexible enough to capture the relationship, and spline terms require specifying the knots. _Generalized additive models_, or _GAM_, are a flexible modeling technique that can be used to automatically fit a spline regression. The `mgcv` package in _R_ can be used to fit a GAM model to the housing data:

```
library
```

The term `s(SqFtTotLiving)` tells the `gam` function to find the “best” knots for a spline term (see [Figure 4-13](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#GAMPlot)).

![A GAM regression fit for the variable SqFtTotLiving (solid line) compared to a smooth (dashed line)](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/psd2_0413.png)

###### Figure 4-13. A GAM regression fit for the variable `SqFtTotLiving` (solid line) compared to a smooth (dashed line)

In _Python_, we can use the `pyGAM` package. It provides methods for regression and classification. Here, we use `LinearGAM` to create a regression model:

```
predictors
```

[![1](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492072935/files/assets/1.png)](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#co_regression_and_prediction_CO4-1)

The default value for `n_splines` is 20. This leads to overfitting for larger `SqFtTotLiving` values. A value of 12 leads to a more reasonable fit.

##### Key Ideas

- Outliers in a regression are records with a large residual.
    
- Multicollinearity can cause numerical instability in fitting the regression equation.
    
- A confounding variable is an important predictor that is omitted from a model and can lead to a regression equation with spurious relationships.
    
- An interaction term between two variables is needed if the effect of one variable depends on the level or magnitude of the other.
    
- Polynomial regression can fit nonlinear relationships between predictors and the outcome variable.
    
- Splines are series of polynomial segments strung together, joining at knots.
    
- We can automate the process of specifying the knots in splines using generalized additive models (GAM).
    

## Further Reading

- For more on spline models and GAMs, see _The Elements of Statistical Learning_, 2nd ed., by Trevor Hastie, Robert Tibshirani, and Jerome Friedman (2009), and its shorter cousin based on _R_, _An Introduction to Statistical Learning_ by Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani (2013); both are Springer books.
    
- To learn more about using regression models for time series forecasting, see _Practical Time Series Forecasting with R_ by Galit Shmueli and Kenneth Lichtendahl (Axelrod Schnall, 2018).
    

# Summary

Perhaps no other statistical method has seen greater use over the years than regression—the process of establishing a relationship between multiple predictor variables and an outcome variable. The fundamental form is linear: each predictor variable has a coefficient that describes a linear relationship between the predictor and the outcome. More advanced forms of regression, such as polynomial and spline regression, permit the relationship to be nonlinear. In classical statistics, the emphasis is on finding a good fit to the observed data to explain or describe some phenomenon, and the strength of this fit is how traditional _in-sample_ metrics are used to assess the model. In data science, by contrast, the goal is typically to predict values for new data, so metrics based on predictive accuracy for out-of-sample data are used. Variable selection methods are used to reduce dimensionality and create more compact models.

[1](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782041795848-marker) This and subsequent sections in this chapter © 2020 Datastats, LLC, Peter Bruce, Andrew Bruce, and Peter Gedeck; used by permission.

[2](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782041419496-marker) In Bayesian statistics, the true value is assumed to be a random variable with a specified distribution. In the Bayesian context, instead of estimates of unknown parameters, there are posterior and prior distributions.

[3](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782039140376-marker) The `-1` argument in the `model.matrix` produces one hot encoding representation (by removing the intercept, hence the “-”). Otherwise, the default in _R_ is to produce a matrix with _P_ – 1 columns with the first factor level as a reference.

[4](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782038718424-marker) This is unintuitive, but can be explained by the impact of location as a confounding variable; see [“Confounding Variables”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#ConfoundingVariables).

[5](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782037780856-marker) There are 80 zip codes in King County, several with just a handful of sales. An alternative to directly using zip code as a factor variable, `ZipGroup` clusters similar zip codes into a single group. See [“Factor Variables with Many Levels”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#FactorVariablesManyLevels) for details.

[6](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782036738936-marker) The term _hat-value_ comes from the notion of the hat matrix in regression. Multiple linear regression can be expressed by the formula  where  is the hat matrix. The hat-values correspond to the diagonal of .

[7](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#idm45782036426552-marker) The coefficient for `Bathrooms` becomes negative, which is unintuitive. Location has not been taken into account, and the zip code 98105 contains areas of disparate types of homes. See [“Confounding Variables”](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch04.html#ConfoundingVariables) for a discussion of confounding variables.

table of contents

search

settings

Previous chapter

[3. Statistical Experiments and Significance Testing](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch03.html)

Next chapter

[5. Classification](https://learning.oreilly.com/library/view/practical-statistics-for/9781492072935/ch05.html)

Table of contents collapsed
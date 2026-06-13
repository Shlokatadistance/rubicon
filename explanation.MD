# Stock Price Kalman Filter Explanation

This implementation uses a small two-state Kalman filter to predict and smooth a stock price series.

The filter only returns price predictions. It keeps a hidden `trend` internally because the next price is usually better estimated when the filter has some memory of recent direction.

## Input Variables

`initial_price`

The first price estimate used to start the filter.

`initial_trend`

The starting estimate for price movement per time step. For minute-by-minute prices, this means expected price change per minute. The default is `0.0`.

`dt`

The time step between observations. If the filter runs once per minute, `dt=1.0` is a good default.

`price_noise`

How noisy the incoming live prices are. A larger value means the filter trusts each new live price less. A smaller value means the filter reacts more quickly to each live price.

In historical testing, `live_price` just means the price that would have been available at that timestamp in the replay.

`volatility`

How much the price trend is allowed to change over time. A larger value makes the filter adapt faster to changing market behavior. A smaller value makes the filter smoother and slower to react.

`initial_uncertainty`

How uncertain the filter is about the starting `price` and hidden `trend`.

## State

The internal state is:

```text
x = [price, trend]
```

Where:

```text
price = current estimated stock price
trend = hidden price movement per time step
```

The covariance matrix tracks uncertainty in both values. Kalman filter examples often name these values by their matrix positions:

```text
P = [[p00, p01],
     [p10, p11]]
```

That naming is compact but not very readable. In this code the same values use descriptive names:

```text
price_variance = p00
price_trend_covariance = p01
trend_price_covariance = p10
trend_variance = p11
```

Where:

```text
price_variance = uncertainty in price
trend_variance = uncertainty in trend
price_trend_covariance = how price uncertainty relates to trend uncertainty
trend_price_covariance = how trend uncertainty relates to price uncertainty
```

## Prediction Equations

Before seeing the next live price, the filter predicts where price should move:

```text
predicted_price = price + trend * dt
predicted_trend = trend
```

In matrix form:

```text
x = F x

F = [[1, dt],
     [0,  1]]
```

The covariance is also predicted forward:

```text
P = F P F^T + Q
```

The `Q` matrix is the process noise. In this code it is controlled by `volatility`:

```text
Q = volatility * [[dt^4 / 4, dt^3 / 2],
                  [dt^3 / 2, dt^2]]
```

This is the part that lets the filter accept that the market can change direction instead of assuming the current trend is perfect forever.

In the code, the `Q` entries are named:

```text
process_price_variance = volatility * dt^4 / 4
process_price_trend_covariance = volatility * dt^3 / 2
process_trend_price_covariance = volatility * dt^3 / 2
process_trend_variance = volatility * dt^2
```

## Update Equations

After the real market price arrives, the filter compares the live price against the predicted price:

```text
residual = live_price - predicted_price
```

The expected uncertainty in that residual is:

```text
residual_variance = price_variance + price_noise
```

Then the Kalman gain decides how strongly to adjust the estimate:

```text
price_gain = price_variance / residual_variance
trend_gain = trend_price_covariance / residual_variance
```

The state update is:

```text
price = predicted_price + price_gain * residual
trend = predicted_trend + trend_gain * residual
```

The code returns `price` as the filtered price. The `trend` value is only used internally to improve the next price prediction.

## Actual Transformation In The Code

Each call to `step(live_price)` does two things:

```text
predicted_price = predict()
filtered_price = update(live_price)
```

So the transformation is:

```text
previous estimated price
previous hidden trend
new live market price
        |
        v
predicted next price
        |
        v
filtered price after correcting with live price
```

The core equation is:

```text
filtered_price = predicted_price + price_gain * (live_price - predicted_price)
```

Where `price_gain` is determined by the balance between current price uncertainty and `price_noise`.

If `price_noise` is high, `price_gain` is smaller and the filter moves slowly.

If `price_noise` is low, `price_gain` is larger and the filter follows live prices more closely.

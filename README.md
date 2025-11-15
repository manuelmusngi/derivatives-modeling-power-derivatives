This is a research paper replication in the Energy Sector on power derivatives. The paper investigates how predictable patterns in electricity spot prices—especially seasonality—impact the pricing of power derivatives in the Nordic Power Exchange (Nord Pool). 

It evaluates one- and two-factor models to capture these dynamics and tests their empirical performance.

📌 Key Highlights
1. Electricity’s Unique Characteristics
   Non-storability and limited transportability make electricity fundamentally different from other commodities.

   These constraints break traditional arbitrage mechanisms, causing spot prices to be highly sensitive to local and temporal supply-demand conditions.

2. Seasonality Drives Price Behavior
   Spot prices show strong seasonal patterns, with higher prices in cold seasons due to heating demand and lower prices in warm seasons.

   Intra-day and intra-week patterns also emerge, driven by business activity and holidays.

3. Volatility and Price Spikes
   Electricity prices are highly volatile, with frequent jumps and spikes, especially during cold seasons.

   Volatility is higher in warm seasons when prices are lower, likely due to log-price transformation effects.

4. Modeling Approach
   The authors propose one- and two-factor models:

   One-factor models use mean-reverting processes with deterministic seasonal components.

   Two-factor models add a long-term equilibrium component, improving realism and allowing imperfect correlation across contracts.

5. Deterministic Component Matters
   A sinusoidal function effectively captures seasonal behavior and improves model fit.

   Dummy variables for months and holidays also help, but are more sensitive to anomalies.

6. Empirical Validation
   Using Nord Pool data (1993–1999), the models are tested against actual futures and forward prices.

   Model 2 (price-based with sinusoidal seasonality) performs best, especially when incorporating a non-zero market price of risk.



✅ Main Takeaways
- Seasonality is crucial: Ignoring it leads to poor derivative pricing.

- Electricity markets require tailored models due to their unique physical and economic constraints.

- Simple deterministic functions (like sine waves) can effectively capture complex seasonal patterns.

- Two-factor models offer better flexibility and realism, especially for long-dated contracts.

- Empirical calibration matters: Even simple models can perform well with thoughtful parameterization and risk adjustments.


⚡ Research Models in the Paper
1. One-Factor Mean-Reverting Model
- Spot price (or log spot price) is modeled as a mean-reverting Ornstein–Uhlenbeck (OU) process.

- Includes a deterministic seasonal component (e.g., sinusoidal function) to capture predictable seasonal cycles.

- Captures short-term dynamics but struggles with long-term correlation across contracts.

2. Two-Factor Model (Short-Term + Long-Term)
- Extends the one-factor model by adding a second stochastic factor:

   - Short-term factor: mean-reverting, captures daily/weekly volatility and spikes.

   - Long-term factor: slower-moving, captures persistent shifts in price levels.

- Allows for imperfect correlation between contracts of different maturities, improving realism for forward/futures pricing.

3. Deterministic Seasonality Functions
- Several specifications are tested:

  - Sinusoidal functions (smooth seasonal cycles).

  - Monthly dummy variables (discrete seasonal shifts).

- The sinusoidal form is found to be parsimonious and effective.


✅ Main Modeling Takeaways
- Seasonality + mean reversion are essential to capture electricity price dynamics.

- Two-factor models outperform one-factor models, especially for longer maturities.

- Simple sinusoidal seasonality works surprisingly well compared to more complex specifications.

- Risk premia matter: ignoring them leads to systematic mispricing of derivatives.

One-factor mean-reverting spot model with seasonality
Let 
𝑆
𝑡
 be the spot price and 
𝑠
(
𝑡
)
 a deterministic seasonal function (e.g., sinusoidal). Define the deseasonalized log spot

𝑥
𝑡
≡
ln
⁡
𝑆
𝑡
−
𝑠
(
𝑡
)
.
Under the physical measure 
𝑃
:

𝑑
𝑥
𝑡
=
𝜅
(
𝜇
−
𝑥
𝑡
)
 
𝑑
𝑡
+
𝜎
 
𝑑
𝑊
𝑡
𝑃
,
so that

𝑆
𝑡
=
exp
⁡
 ⁣
(
𝑠
(
𝑡
)
+
𝑥
𝑡
)
.
Under the risk–neutral measure 
𝑄
, with market price of risk 
𝜆
 (or equivalently a risk-adjusted mean 
𝜇
𝑄
):

𝑑
𝑥
𝑡
=
𝜅
(
𝜇
𝑄
−
𝑥
𝑡
)
 
𝑑
𝑡
+
𝜎
 
𝑑
𝑊
𝑡
𝑄
,
where
𝜇
𝑄
=
𝜇
−
𝜆
𝜅
.
A common seasonal specification is

𝑠
(
𝑡
)
=
𝑎
0
+
𝑎
1
cos
⁡
(
2
𝜋
𝑡
)
+
𝑎
2
sin
⁡
(
2
𝜋
𝑡
)
,
optionally augmented with monthly or weekly dummies.

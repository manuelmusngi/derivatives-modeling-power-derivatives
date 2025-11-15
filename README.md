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
Seasonality is crucial: Ignoring it leads to poor derivative pricing.

Electricity markets require tailored models due to their unique physical and economic constraints.

Simple deterministic functions (like sine waves) can effectively capture complex seasonal patterns.

Two-factor models offer better flexibility and realism, especially for long-dated contracts.

Empirical calibration matters: Even simple models can perform well with thoughtful parameterization and risk adjustments.

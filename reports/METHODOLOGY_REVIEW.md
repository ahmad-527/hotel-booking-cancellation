# Scope of the hotel experiment

This portfolio preserves the submitted experiment's model definitions, preprocessing, candidate grids, scoring, split, seeds and selection rule. The source submission is retained privately. The portfolio text clarifies limitations identified during publication review; it does not represent a new prospectively designed benchmark.

## Split and repeated records

The source sorts by arrival date, takes the first 80% of rows for development, and cleans each partition separately. Raw partitions contain 95,512 and 23,878 rows; cleaned partitions contain 68,354 and 18,879. The final training arrival and first test arrival are both **22 April 2017**. Five exact cleaned rows appear in both partitions. These are five distinct row patterns, each retained once in each partition after within-partition deduplication. They are not confirmed duplicate bookings because booking identifiers are unavailable.

The overlap limits claims of record-independent testing. All five outer time-series folds also share an arrival date between their training and validation boundaries. A future evaluation should freeze date-blocked and booking/group-aware partitions before outcomes are examined. The existing results must remain labelled retrospective; removing overlaps now would not make the already inspected test period newly unseen.

## Information timing and leakage

The experiment demonstrates the effect of including reservation-status fields, then excludes them and several fields with uncertain timing. This is useful evidence about these particular fields, not proof that every remaining feature is available at the intended decision time.

The [original data paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/) describes a snapshot generally reconstructed for the day before arrival, with variables taken from several tables. It defines booking changes through check-in or cancellation and ADR using lodging transactions. These details require an explicit as-of-time data design before early-booking prediction could be claimed. A strong empirical association alone does not prove when a variable was recorded. In particular, the paper does not establish that country is confirmed only at check-in or that every parking request was recorded on arrival.

The paper treats `NULL` agent/company values as not applicable, rather than unexplained data loss. The portfolio discussion corrects the submission's reversed wording about these values. The row filters and treatment of agent/company identifiers remain unchanged.

## Cross-validation and model selection

Outer scoring uses five expanding row-based time-series folds. The same folds are used for preprocessing comparison, tuning and subsequent candidate ranking, so development scores are reused during selection. Their standard deviation is descriptive variation across folds, not a confidence interval or standard error.

The stacking comparator uses `StackingClassifier(cv=3)`. For binary classification, an integer means stratified folds with shuffling disabled; it does not mean forward-only training. Later rows can therefore contribute to an earlier inner-fold prediction. This comparator must not be advertised as a temporally valid stacking design. See the [official stacking documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html).

Histogram boosting retains automatic early stopping. For sufficiently large fits, it uses an internal training/validation split; the 300-stage setting is a cap, not proof that every fit used 300 stages. The outer time-series split does not turn these internal steps into forward-only procedures. See the [official boosting documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html).

Shuffled and chronological cross-validation differ in their training sets and distributions. The observed score difference is not a causal measurement of a precise amount of leakage. The notebook's final choice follows its stated heuristic: prefer logistic regression only if its mean is within one standard deviation of the best candidate's mean; otherwise choose the highest mean. This is not an equivalence test.

## Costs, interpretation and usefulness

The threshold is selected on the final development fold using the assumed score `3 × false negatives + false positives`. That fold also contributed to earlier model tuning. Cost reduction under this score is not measured financial savings, and proximity to a theoretical threshold does not validate the chosen cost ratio or calibration.

Permutation importance measures fitted-model dependence under a particular shuffle, not causation. Month/hotel breakdowns describe this historical dataset; they do not establish current operational accuracy. The project demonstrates an academic modelling workflow. It has not demonstrated business benefit, reliable overbooking decisions or generalisation beyond these two hotels and this period.

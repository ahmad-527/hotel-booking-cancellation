# Reproduction and validation — 28 October 2026

The full notebook completed in a fresh Python kernel: **19 of 19 code cells**, no error outputs, **1179.92 seconds** including the private post-run metric audit. The analysis used Python 3.11.6 and the core versions pinned in `requirements.txt`, two joblib workers and one numerical thread per process.

The execution controller used the existing Jupyter environment (nbclient 0.11.0, nbformat 5.11.1, jupyter-client 8.10.0), launching the existing compatible analysis interpreter (ipykernel 6.29.5). A new pip installation of the combined requirements was not separately tested. Windows is the tested platform. The original submission records Python 3.11.6 but does not record a complete package lock; this is a measured reproduction environment, not a claim to have recovered every historical dependency.

Model, split, preprocessing, grid, scoring, seed, selection and threshold code match the final submitted experiment after normalising one operational change: the worker cap now defaults to two. Student identification was removed, outputs refreshed and explanatory text revised. The original notebook, HTML and input remain unchanged privately.

The reproduced preprocessing and initial model-comparison scores match the saved submission scores. The unscaled logistic baseline emitted convergence warnings and reached its 1000-iteration cap; it is a documented diagnostic baseline. The submission's warning filter remains in the analytical source, so this run must not be described as warning-free.

The selected candidate is **Voting**, with threshold **0.23** and test ROC-AUC **0.775678**. Separate calculations from the saved predictions confirmed AUC using average ranks, the confusion counts, precision, recall, F1, accuracy and both assumed cost scores. These are checks of the reported metrics, not independent model training or a new unseen evaluation.

The source CSV matches the public TidyTuesday mirror byte for byte. The archive was extracted in an empty directory and its hash checked; altered inputs and an altered archive were rejected without overwriting existing data. Full-row comparison confirmed five cleaned patterns shared by the train/test partitions. Their boundary date is shared, as are the boundary dates in all five outer folds. These limits are retained and explained in the [methodology review](METHODOLOGY_REVIEW.md).

All eight regenerated figures under `figures/` were visually inspected. The grid plot uses sparse logarithmic tick labels; the adjacent notebook text identifies all four leaf counts explicitly. No new HTML export was generated. Private run checkpoints, audit scripts, row-level predictions, working notes and extracted data are excluded from publication.

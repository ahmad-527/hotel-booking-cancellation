# Hotel booking input

The fixed input is a combined table derived from Nuno Antonio, Ana de Almeida and Luis Nunes, [Hotel booking demand datasets](https://doi.org/10.1016/j.dib.2018.11.126), *Data in Brief*, 22 (2019), 41–49. The authors describe 119,390 booking observations from two Portuguese hotels, with identifying hotel/customer information removed. The published article and associated data are available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); retain the authors' attribution and applicable source notices.

The supplied `hotel_bookings.csv` is byte-identical to the [TidyTuesday combined CSV](https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv), checked on 28 October 2026. The combined file adds a hotel label to the two source tables. This check establishes the identity of the current supplied file and mirror; it does not establish the original download date.

The unchanged CSV is compressed in `hotel_input_snapshot.zip`. [inputs.json](inputs.json) records its filename, source URL, byte size and SHA-256, as well as the archive hash. From the repository root, run:

```sh
python scripts/data.py --extract
```

The extractor verifies the archive, exact member list and extracted CSV. It rejects a different existing file instead of replacing it. `python scripts/data.py` verifies an already extracted file. Extraction requires no network connection. The extracted CSV is excluded from Git.

The dataset describes historical arrivals from July 2015 to August 2017. The source paper describes values generally reconstructed for the day before arrival, with variables drawn from several operational tables. This does not establish that every retained feature was known at booking time or before cancellation. The notebook is a retrospective classification exercise, not a validated early-booking intervention.

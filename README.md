# vBase Python Samples for Google Colab

These interactive examples use the recommended
[`vbase-api`](https://pypi.org/project/vbase-api/) Python client to create and
verify vBase stamps from [Google Colab](https://colab.research.google.com/).

## Getting Started

1. Sign in to [vBase](https://app.vbase.com) and copy your API key from
   [Account Settings](https://app.vbase.com/profile#account_settings).
2. Follow the [Quickstart](docs/quickstart.md) to add the API key to Google
   Colab secrets.
3. Open one of the examples below.

## Samples

| Sample | Description | Open in Colab |
| --- | --- | --- |
| Setup | Configure and validate the credentials used by the samples. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/setup.ipynb) |
| Create a collection | Create or reuse a collection through the vBase API. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/create_set.ipynb) |
| Stamp a text record | Stamp inline text and verify its CID. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/add_string_dataset_record.ipynb) |
| Use vBase from async code | Run the synchronous client without blocking an application's event loop. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/add_string_dataset_record_async.ipynb) |
| Create a portfolio history | Stamp portfolio CIDs and store the exact records in Amazon S3. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/produce_portfolio_history_s3.ipynb) |
| Verify a portfolio history | Verify S3 records, their owner, collection, and timestamps. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/verify_portfolio_history_s3.ipynb) |
| Create a sentiment history | Stamp sentiment CIDs and store the exact records in Amazon S3. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/produce_sentiment_dataset_history_s3.ipynb) |
| Verify a sentiment history | Verify S3 records before using them in analytics. | [Open](https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/verify_sentiment_dataset_history_s3.ipynb) |

The Amazon S3 examples require additional AWS credentials and a bucket. The
producer examples calculate each CID locally and submit the CID instead of the
record contents; the exact record bytes remain in the configured S3 bucket.
Each producer run creates a unique collection. Copy its printed collection CID
into the matching verifier to select that history.

## References

- [vBase documentation](https://docs.vbase.com/)
- [`vbase-api-py` documentation and source](https://github.com/validityBase/vbase-api-py)
- [vBase REST API](https://app.vbase.com/swagger/)

## License

This project is licensed under the Apache License 2.0. See
[LICENSE.txt](LICENSE.txt).

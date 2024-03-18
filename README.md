# vbase-py-samples

vBase Python Samples for Google Colab

-   Python 3.8+ support

---

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Introduction

vBase APIs and services support provably sound data science and regulatory compliance.
Producers can create auditable provenance records for their digital objects while retaining control and privacy.
Consumers can use 3rd party data and models with the same assurance as their internal artifacts.

The following samples illustrate common solutions built on top of the vBase SDK and services.
The samples are adapted for use with Google Colab.
Users can use the Collab secrets manager to store the vBase configuration state.  

## Setup

### Configure vBase Access

Please contact vBase for help configuring your environment and to obtain an API key.
An API key provides simple managed access to commitment services
without the need to worry about blockchains and cryptocurrency.

Once you have the API key, the following notebook will guide you through the steps
of setting up your Google Collab environment:
https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/setup.ipynb

If you have previously configured vBase access, for instance when using the `vbase-py-tools` package,
you can re-use those settings from the `.env` file created during the initialization.

Below is a summary of the configuration settings.
These are the variables that must be defined using the secrets manager:

```shell
# Forwarder Configuration
# URL of the production vBase forwarder service.
# Users should not change this value.
FORWARDER_ENDPOINT_URL="https://api.vbase.com/forwarder/"
# User API key for accessing the vBase forwarder service.
# Users should set this value to the API key they received from vBase.
FORWARDER_API_KEY="USER_VBASE_API_KEY"

# User Private Key
# The private key for making stamps/commitments.
# This key signs and controls all operations -- it must be kept secret.
# vBase will never request this value.
PRIVATE_KEY="USER_PRIVATE_KEY"
```

### Open notebooks in Collab

Open any of the sample notebooks in Google Colab and get going!

https://colab.research.google.com/github/validityBase/vbase-py-samples-collab/blob/main/samples/

# Data and software licenses for the E4 provider bank (round 2, worker E4)

Date of all downloads and all license checks below: 17 September 2026 (UTC). Every URL in this file was
fetched on that date with `curl` from the login node; the fetch that established each license statement is
named next to the statement. Nothing was downloaded except the two datasets listed here, and no dataset was
substituted for another.

Paths are written relative to `<scratchpad>`, the session scratchpad root named in
`audit/round2/prompts/COMMON.md`; absolute user paths are omitted here to keep the repository anonymous.
Datasets live under `<scratchpad>/round2/A/data/` and are never copied into any git tree.

Checksums were computed with `sha256sum` and `md5sum` on the downloaded files after the transfer.

## 1. Fashion-MNIST

- Name: Fashion-MNIST (Zalando SE), 60,000 training and 10,000 test 28x28 grayscale images, 10 classes.
- Date downloaded: 17 September 2026.
- Exact download URLs used (primary, GitHub repository named in the experiment decision):
  - `https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/train-images-idx3-ubyte.gz`
  - `https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/train-labels-idx1-ubyte.gz`
  - `https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/t10k-images-idx3-ubyte.gz`
  - `https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/t10k-labels-idx1-ubyte.gz`
- Mirror also downloaded and then discarded after comparison (the links published in the repository README):
  `http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/<same four file names>`. The four files from the
  mirror had byte-identical sha256 values to the four files from GitHub, so the two sources agree.
- sha256 of the retained files:
  - `3aede38d61863908ad78613f6a32ed271626dd12800ba2636569512369268a84  train-images-idx3-ubyte.gz`
  - `a04f17134ac03560a47e3764e11b92fc97de4d1bfaf8ba1a3aa29af54cc90845  train-labels-idx1-ubyte.gz`
  - `346e55b948d973a97e58d2351dde16a484bd415d4595297633bb08f03db6a073  t10k-images-idx3-ubyte.gz`
  - `67da17c76eaffca5446c3361aaab5c3cd6d1c2608764d35dfb1850b086bf8dd5  t10k-labels-idx1-ubyte.gz`
- md5 of the retained files, compared against the md5 values published in the repository README (the README
  table under "Get the Data"): all four match.
  - `8d4fb7e6c68d591d4c3dfef9ec88bf0d  train-images-idx3-ubyte.gz` (README: `8d4fb7e6c68d591d4c3dfef9ec88bf0d`)
  - `25c81989df183df01b3e8a0aad5dffbe  train-labels-idx1-ubyte.gz` (README: `25c81989df183df01b3e8a0aad5dffbe`)
  - `bef4ecab320f06d8554ea6380940ec79  t10k-images-idx3-ubyte.gz` (README: `bef4ecab320f06d8554ea6380940ec79`)
  - `bb300cfdad3c16e7a12a480ee83cd310  t10k-labels-idx1-ubyte.gz` (README: `bb300cfdad3c16e7a12a480ee83cd310`)
- License name: MIT License.
- License URL read, and date: `https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/LICENSE`,
  read 17 September 2026 (the repository `LICENSE` file; the same text appears in the README section
  "License", also read on that date, at
  `https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/README.md`).
- Verbatim quote of the license statement (first two sentences of the `LICENSE` file):
  "The MIT License (MIT) Copyright (c) 2017 Zalando SE, https://tech.zalando.com
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
  documentation files (the "Software"), to deal in the Software without restriction, including without
  limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
  Software, and to permit persons to whom the Software is furnished to do so, subject to the following
  conditions:"
  (The file uses a Unicode copyright sign and typographic quotation marks; they are transcribed here as `(c)`
  and plain quotation marks to satisfy the round-2 character rules. The stored copy is unmodified.)
- Stored license copy: `<scratchpad>/round2/A/data/licenses/fashion-mnist-LICENSE.txt`, sha256
  `13ef4788476d292858fa60eb9a5f74aeca5c65770bc885ccaa05823a17ef7be1`.
- Scratchpad path of the data: `<scratchpad>/round2/A/data/fashion_mnist/` (four `.gz` files, 30 MB).
- Note: a copy of the repository README fetched by scout A1 earlier on 17 September 2026 is at
  `<scratchpad>/round2/A/data/fashion_mnist_README.md`; the license quote above was checked against it and
  against the freshly fetched `LICENSE` file.

## 2. UCI Covertype

- Name: Covertype (UCI Machine Learning Repository, dataset 31; creator Jock Blackard), 581,012 rows,
  54 features, 7 cover-type classes, DOI 10.24432/C50K5N.
- Date downloaded: 17 September 2026.
- Exact download URLs used:
  - `https://archive.ics.uci.edu/static/public/31/covertype.zip` (the download button of the dataset page;
    the archive contains `covtype.data.gz`, `covtype.info` and `old_covtype.info`).
  - `https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz` (the legacy direct
    link to the same file, downloaded as an independent check).
  - Metadata used only to confirm the record: `https://archive.ics.uci.edu/api/dataset?id=31`.
- sha256:
  - `89a975c2457cd48e824238ae43c5a3cb762e42c4b4078d9b44a4514055105f6d  covertype.zip`
  - `614360d0257557dd1792834a85a1cdebfadc3c4f30b011d56afee7ffb5b15771  covtype.data.gz` (extracted from the zip)
  - `614360d0257557dd1792834a85a1cdebfadc3c4f30b011d56afee7ffb5b15771` for the file fetched from the legacy
    direct link, which is byte identical to the file extracted from the zip; the legacy copy was then deleted.
- License name: Creative Commons Attribution 4.0 International (CC BY 4.0).
- License URL read, and date: `https://archive.ics.uci.edu/dataset/31/covertype`, read 17 September 2026
  (the "License" block of the dataset page; the page links the legal code at
  `https://creativecommons.org/licenses/by/4.0/legalcode`).
- Verbatim quote of the license statement on that page: "This dataset is licensed under a Creative Commons
  Attribution 4.0 International (CC BY 4.0) license. This allows for the sharing and adaptation of the
  datasets for any purpose, provided that the appropriate credit is given."
- Stored license evidence: `<scratchpad>/round2/A/data/licenses/uci-covertype-page.html` (the fetched dataset
  page) and `<scratchpad>/round2/A/data/licenses/uci-covertype-api.json` (the dataset record).
- Scratchpad path of the data: `<scratchpad>/round2/A/data/covertype/` (`covertype.zip`, `covtype.data.gz`,
  `covtype.info`, `old_covtype.info`; 22 MB).
- Attribution required by CC BY 4.0 for any released table derived from this dataset: Jock Blackard, Covertype,
  UCI Machine Learning Repository, DOI 10.24432/C50K5N, CC BY 4.0.

## 3. scikit-learn (software used to build the providers)

- Version installed in the session venv and used for every provider: scikit-learn 1.9.1 (checked with
  `importlib.metadata`; the distribution metadata records `License-Expression: BSD-3-Clause`).
- License name: BSD 3-Clause "New" or "Revised" License.
- License URL read, and date: `https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/COPYING`,
  read 17 September 2026.
- Verbatim quote of the opening of that file: "BSD 3-Clause License
  Copyright (c) 2007-2026 The scikit-learn developers.
  All rights reserved."
- Stored license copy: `<scratchpad>/round2/A/data/licenses/scikit-learn-COPYING.txt`, sha256
  `50d6a9d340f19ab355609917993114daf5f47e3161067bcf34955bbd05cd9cb0`.
- Other libraries used, already present in the venv and not installed by this worker: NumPy 2.5.3 (BSD-3),
  SciPy, pandas, joblib 1.6.0. No package was installed for E4.

## 4. Use and redistribution

Both datasets are used only inside the session scratchpad, for offline evaluation of frozen classifiers on
their own held-out pools. Neither dataset, nor any image or row of it, is copied into the repository or into
the supplementary archive. What may be released are derived aggregate tables (per provider and per knob
accuracy curves) computed from the held-out pools; MIT and CC BY 4.0 both permit this, CC BY 4.0 subject to
the attribution recorded in Section 2.

What was checked and how: each file was downloaded with `curl` and its sha256 computed locally; the
Fashion-MNIST files were additionally checked against the md5 values published in the source repository README
and against a second mirror; the Covertype file was checked against a second URL at the same archive; each
license statement was read on the page or file named above on 17 September 2026 and a copy was stored. No
claim is made that these licenses have not changed since that date, and no legal review was performed.

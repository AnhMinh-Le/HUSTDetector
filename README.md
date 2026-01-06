<div align="left" style="position: relative;">
<!-- <img src="https://img.icons8.com/?size=512&id=55494&format=png" align="right" width="30%" style="margin: -20px 0 0 20px;"> -->
<h1>HUSTDetector</h1>
<p align="left">
	<em>This project is a report for IT4142E - Introduction to Data Science 2025.1 under the guidance of Dr. Nguyen Duc Anh.</em>
</p>
</div>
<br clear="right">

## 📋 Table of Contents

- [📋 Table of Contents](#-table-of-contents)
- [👥 Group Members](#-group-members)
- [📍 Overview](#-overview)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#️-prerequisites)
  - [⚙️ Installation](#️-installation)
  - [🤖 Usage](#-usage)
  - [🧪 Testing](#-testing)
- [🙌 Acknowledgments](#-acknowledgments)



## 👥 Group Members

| Name | ID | Role |
|------|-----|------|
| Le Anh Minh | 20235530 | Leader |
| Pham Ngoc Trinh | 20230092 | Member |
| Nguyen Gia Khanh | 20235513 | Member |
| Doan Truong Giang | 20235494 | Member |
| Nguyen The Quan | 20235548 | Member |
| Luong Xuan Nguyen | 20230087 | Member |
| Truong Minh Phuc | 20235545 | Member |
| Bui Thi Bich Ngoc | 20230088 | Member |

---

## 📍 Overview

The HUSTDetector project revolutionizes the detection of deepfake content through advanced text analysis. By leveraging state-of-the-art machine learning techniques, it offers robust tools for generating, managing, and evaluating text embeddings to accurately classify content as human, AI-generated, or mixed. Ideal for tech companies and cybersecurity experts, HUSTDetector enhances digital trust and integrity across various media platforms.


## 🚀 Getting Started

### ☑️ Prerequisites

Before getting started with HUSTDetector, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip


### ⚙️ Installation

Install HUSTDetector using one of the following methods:

**Build from source:**

1. Clone the HUSTDetector repository:
```sh
❯ git clone https://github.com/AnhMinh-Le/HUSTDetector
```

2. Navigate to the project directory:
```sh
❯ cd HUSTDetector
```

3. Install the project dependencies:

```sh
❯ pip install -r algorithm/requirements.txt
```

4. Download the dataset:

To download the data, run the following command:

```sh
❯ wget https://huggingface.co/datasets/AnhMinhLe/HUSTSet/resolve/main/data.zip
```

Then extract the data:

```sh
❯ unzip data.zip -d .
```




### 🤖 Usage
Run HUSTDetector using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

To train the model
```sh
❯ python algorithm/train_classifier.py <your parameter goes here>
```
To generate the vector database after training
```sh
❯ python algorithm/gen_database.py <your parameter goes here>
```

### 🧪 Testing
Run the test suite using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python algorithm/test_from_database.py <your parameter goes here>
```


---
## 🙌 Acknowledgments

We would like to express our gratitude to **Dr. Nguyen Duc Anh** for his guidance and support throughout this project.

---



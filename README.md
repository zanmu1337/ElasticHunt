# 🔍 ElasticHunt

ElasticHunt is a pentesting tool designed to detect and test misconfigured, publicly exposed Elasticsearch instances.

## ✨ Features

- 🔎 Detects exposed Elasticsearch instances
- ⚙️ Tests for common misconfigurations
- 📊 Retrieves index names, mappings, and sample data
- ⚡ Fast and lightweight
- 🧩 Simple to use — no complex setup required

## 🚀 How it works

ElasticHunt targets Elasticsearch servers that are exposed without authentication.

It probes the instance and checks for:

- Open access (no credentials required)
- Accessible index and their contents
- Sensitive data exposure

## 📦 Installation

```bash
git clone https://github.com/zanmu1337/ElasticHunt.git
cd ElasticHunt
pip install -r requirements.txt
```

## ⚡ Usage

```bash
python elastichunt.py -u <target>
```

## ⚠️ Disclaimer

ElasticHunt is intended for authorized security testing and research only.

Only use it against systems you own or have explicit permission to test.
Do not use ElasticHunt against systems without authorization.

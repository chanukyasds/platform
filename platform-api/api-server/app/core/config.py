from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parents[2]

CLUSTERS_FILE = BASE_DIR / "config" / "clusters.yaml"
KUBERNETES_FILE = BASE_DIR / "config" / "kubernetes.yaml"
ARGOCD_FILE = BASE_DIR / "config" / "argocd.yaml"
REPOSITORIES_FILE = BASE_DIR / "config" / "repositories.yaml"


def load_clusters() -> dict:
    with open(CLUSTERS_FILE, "r") as file:
        config = yaml.safe_load(file)

    return config.get("clusters", {})


def load_kubernetes_clusters() -> dict:
    with open(KUBERNETES_FILE, "r") as file:
        config = yaml.safe_load(file)

    return config.get("clusters", {})

def load_argocd_clusters() -> dict:
    with open(ARGOCD_FILE, "r") as file:
        config = yaml.safe_load(file)

    return config.get("clusters", {})

def load_repositories() -> dict:
    with open(REPOSITORIES_FILE, "r") as file:
        config = yaml.safe_load(file)

    return config.get("repositories", {})
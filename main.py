
import yaml
from src.electricity_models.pipeline import run

if __name__ == "__main__":
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)
    results = run(config)
    print("One-factor OU params:", results["ou_params"])
    print("Estimated market price of risk (lambda):", results["lambda"])

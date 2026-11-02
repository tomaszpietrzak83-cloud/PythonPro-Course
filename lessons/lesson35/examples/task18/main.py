import json


class ConfigManager:
    def __init__(self, path):
        self.configs = json.loads(path.read_text(encoding="utf-8"))
        for env in ["dev", "staging", "production"]:
            for key in ["region", "instance_type", "db_size"]:
                if key not in self.configs[env]:
                    raise ValueError(f"Missing {env}.{key}")

    def deploy(self, environment):
        return {
            "environment": environment,
            "planned_resources": self.configs[environment],
        }

    def compare(self, env1, env2):
        first, second = self.configs[env1], self.configs[env2]
        return {
            key: [first[key], second[key]]
            for key in first
            if first[key] != second[key]
        }


def demo(work, cloud):
    from pathlib import Path

    manager = ConfigManager(Path(__file__).with_name("config.json"))
    return {
        "plan": manager.deploy("production"),
        "differences": manager.compare("dev", "production"),
    }

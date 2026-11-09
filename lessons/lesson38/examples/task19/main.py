from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    deploy = workflow["jobs"]["deploy"]
    assert deploy["permissions"]["id-token"] == "write"
    commands = deploy["steps"][-1]["run"]
    assert commands.index("docker push") < commands.index("aws ecs update-service")
    return {"stages": ["OIDC", "ECR login", "build/push", "register revision", "ECS update"]}

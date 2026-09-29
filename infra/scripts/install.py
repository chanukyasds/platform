from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]

SYSTEMD_DIR = Path("/etc/systemd/system")


SERVICES = {
    "api": {
        "unit": "platform-api.service",
        "service": "platform-api",
        "service_dir": ROOT / "platform-api" / "api-server",
        "env_dir": ROOT / "platform-api",
    },

    "mcp": {
        "unit": "platform-mcp.service",
        "service": "platform-mcp",
        "service_dir": ROOT / "platform-mcp",
        "env_dir": ROOT / "platform-mcp",
    },
}


def run(*cmd):
    print("+", " ".join(str(x) for x in cmd))

    subprocess.run(
        [str(x) for x in cmd],
        check=True,
    )


def ensure_env(env_dir: Path):
    env_file = env_dir / ".env"
    example_file = env_dir / ".env.example"

    if env_file.exists():
        print(f"Environment file exists: {env_file}")
        return

    if not example_file.exists():
        raise RuntimeError(
            f"Missing environment template: {example_file}"
        )

    env_file.write_text(
        example_file.read_text()
    )

    env_file.chmod(0o600)

    print(
        f"Created {env_file} from .env.example"
    )

    print(
        "Fill required environment values before starting the service."
    )


def ensure_venv(service_dir: Path):
    venv_dir = service_dir / ".venv"

    if not venv_dir.exists():

        run(
            "python3",
            "-m",
            "venv",
            venv_dir,
        )

    pip = venv_dir / "bin" / "pip"

    run(
        pip,
        "install",
        "--upgrade",
        "pip",
    )

    requirements = service_dir / "requirements.txt"

    if requirements.exists():

        run(
            pip,
            "install",
            "-r",
            requirements,
        )

    else:
        print(
            f"No requirements.txt found in {service_dir}"
        )


def install_systemd_unit(unit_name: str):
    template = (
        ROOT
        / "infra"
        / "systemd"
        / unit_name
    )

    if not template.exists():
        raise RuntimeError(
            f"Missing systemd template: {template}"
        )

    rendered = template.read_text().replace(
        "__REPO_ROOT__",
        str(ROOT),
    )

    target = SYSTEMD_DIR / unit_name

    target.write_text(rendered)

    print(
        f"Installed systemd unit: {target}"
    )


def install_service(name: str):
    config = SERVICES[name]

    print()
    print(f"Installing {name}")
    print("-" * 40)

    ensure_env(
        config["env_dir"]
    )

    ensure_venv(
        config["service_dir"]
    )

    install_systemd_unit(
        config["unit"]
    )

    run(
        "systemctl",
        "daemon-reload",
    )

    run(
        "systemctl",
        "enable",
        config["service"],
    )

    print()
    print(
        f"{config['service']} installed and enabled."
    )

    print(
        f"Start it with: "
        f"sudo systemctl start {config['service']}"
    )


def main():

    if len(sys.argv) != 2:
        print(
            "Usage:"
        )
        print(
            "  sudo python3 infra/scripts/install.py api"
        )
        print(
            "  sudo python3 infra/scripts/install.py mcp"
        )
        print(
            "  sudo python3 infra/scripts/install.py all"
        )

        sys.exit(1)

    target = sys.argv[1].lower()

    if target == "all":

        for name in SERVICES:
            install_service(name)

    elif target in SERVICES:

        install_service(target)

    else:

        print(
            f"Unknown target: {target}"
        )

        print(
            "Valid options: api, mcp, all"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
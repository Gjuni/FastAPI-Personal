import os
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sshtunnel import SSHTunnelForwarder


load_dotenv()  # loads .env if present (user creates locally)


@dataclass(frozen=True)
class DbConfig:
    ssh_host: str
    ssh_port: int
    ssh_user: str
    ssh_pem_path: str
    rds_host: str
    rds_port: int
    rds_db: str
    rds_user: str
    rds_password: str
    local_bind_host: str = "127.0.0.1"
    local_bind_port: int = 0  # 0 => auto-assign


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def load_db_config() -> DbConfig:
    return DbConfig(
        ssh_host=_require_env("SSH_HOST"),
        ssh_port=int(os.getenv("SSH_PORT", "22")),
        ssh_user=_require_env("SSH_USER"),
        ssh_pem_path=_require_env("SSH_PEM_PATH"),
        rds_host=_require_env("RDS_HOST"),
        rds_port=int(os.getenv("RDS_PORT", "3306")),
        rds_db=_require_env("RDS_DB"),
        rds_user=_require_env("RDS_USER"),
        rds_password=_require_env("RDS_PASSWORD"),
        local_bind_host=os.getenv("LOCAL_BIND_HOST", "127.0.0.1"),
        local_bind_port=int(os.getenv("LOCAL_BIND_PORT", "0")),
    )


@contextmanager
def ssh_tunnel(cfg: Optional[DbConfig] = None) -> Iterator[SSHTunnelForwarder]:
    """
    Create an SSH tunnel:
      local (127.0.0.1:<assigned>) -> SSH(bastion) -> RDS_HOST:RDS_PORT
    """
    cfg = cfg or load_db_config()
    tunnel = SSHTunnelForwarder(
        (cfg.ssh_host, cfg.ssh_port),
        ssh_username=cfg.ssh_user,
        ssh_pkey=cfg.ssh_pem_path,
        remote_bind_address=(cfg.rds_host, cfg.rds_port),
        local_bind_address=(cfg.local_bind_host, cfg.local_bind_port),
    )
    try:
        tunnel.start()
        yield tunnel
    finally:
        try:
            tunnel.stop()
        except Exception:
            # best-effort cleanup
            pass


def create_mysql_engine_via_ssh(
    cfg: Optional[DbConfig] = None,
    tunnel: Optional[SSHTunnelForwarder] = None,
) -> Engine:
    """
    Returns a SQLAlchemy Engine that connects to MySQL via an SSH tunnel.
    You must keep the tunnel open while using the engine.
    """
    cfg = cfg or load_db_config()
    if tunnel is None or not getattr(tunnel, "is_active", False):
        raise RuntimeError("Tunnel is not active. Create the tunnel first and pass it in.")

    local_port = int(tunnel.local_bind_port)
    url = (
        f"mysql+pymysql://{cfg.rds_user}:{cfg.rds_password}"
        f"@{cfg.local_bind_host}:{local_port}/{cfg.rds_db}"
        f"?charset=utf8mb4"
    )
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
    )


def test_connection() -> str:
    """
    Quick connectivity check. Returns MySQL version string.
    """
    cfg = load_db_config()
    with ssh_tunnel(cfg) as tunnel:
        engine = create_mysql_engine_via_ssh(cfg, tunnel)
        with engine.connect() as conn:
            version = conn.execute(text("SELECT VERSION()")).scalar_one()
            return str(version)


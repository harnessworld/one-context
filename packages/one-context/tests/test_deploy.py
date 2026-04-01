"""Tests for one_context.deploy — deploy.yaml loading and validation."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from one_context.deploy import load_deploy_yaml, validate_deploy_yaml
from one_context.errors import ManifestError


VALID_DEPLOY = textwrap.dedent("""\
    version: "1"
    name: my-service
    strategy: docker-compose

    stages:
      - id: staging
        cmd: "docker-compose up -d"
        health_check: "curl -f http://localhost/health"
        approval_required: false
      - id: production
        cmd: "docker-compose -f prod.yml up -d"
        health_check: "curl -f http://localhost/health"
        approval_required: true

    rollback:
      cmd: "docker-compose down"
""")


class TestLoadDeployYaml:
    def test_load_valid(self, tmp_path: Path):
        p = tmp_path / "deploy.yaml"
        p.write_text(VALID_DEPLOY, encoding="utf-8")
        data = load_deploy_yaml(p)
        assert data["name"] == "my-service"
        assert data["strategy"] == "docker-compose"
        assert len(data["stages"]) == 2

    def test_load_missing_file(self, tmp_path: Path):
        with pytest.raises(ManifestError, match="not found"):
            load_deploy_yaml(tmp_path / "deploy.yaml")

    def test_load_non_mapping(self, tmp_path: Path):
        p = tmp_path / "deploy.yaml"
        p.write_text("- a list\n", encoding="utf-8")
        with pytest.raises(ManifestError, match="mapping"):
            load_deploy_yaml(p)


class TestValidateDeployYaml:
    def test_valid_no_errors(self, tmp_path: Path):
        p = tmp_path / "deploy.yaml"
        p.write_text(VALID_DEPLOY, encoding="utf-8")
        errors, warnings = validate_deploy_yaml(p)
        assert errors == []
        assert warnings == []

    def test_bad_version(self, tmp_path: Path):
        p = tmp_path / "deploy.yaml"
        p.write_text(VALID_DEPLOY.replace('version: "1"', 'version: "2"'), encoding="utf-8")
        errors, _ = validate_deploy_yaml(p)
        assert any("version" in e for e in errors)

    def test_missing_name(self, tmp_path: Path):
        p = tmp_path / "deploy.yaml"
        p.write_text(VALID_DEPLOY.replace("name: my-service", "name: "), encoding="utf-8")
        errors, _ = validate_deploy_yaml(p)
        assert any("name" in e for e in errors)

    def test_bad_strategy(self, tmp_path: Path):
        p = tmp_path / "deploy.yaml"
        p.write_text(VALID_DEPLOY.replace("strategy: docker-compose", "strategy: invalid"), encoding="utf-8")
        errors, _ = validate_deploy_yaml(p)
        assert any("strategy" in e for e in errors)

    def test_empty_stages(self, tmp_path: Path):
        content = textwrap.dedent("""\
            version: "1"
            name: svc
            strategy: manual
            stages: []
        """)
        p = tmp_path / "deploy.yaml"
        p.write_text(content, encoding="utf-8")
        errors, _ = validate_deploy_yaml(p)
        assert any("stages" in e for e in errors)

    def test_duplicate_stage_ids(self, tmp_path: Path):
        content = textwrap.dedent("""\
            version: "1"
            name: svc
            strategy: manual
            stages:
              - id: staging
                cmd: "echo 1"
              - id: staging
                cmd: "echo 2"
        """)
        p = tmp_path / "deploy.yaml"
        p.write_text(content, encoding="utf-8")
        errors, _ = validate_deploy_yaml(p)
        assert any("duplicate" in e for e in errors)

    def test_no_rollback_warning(self, tmp_path: Path):
        content = textwrap.dedent("""\
            version: "1"
            name: svc
            strategy: docker-compose
            stages:
              - id: staging
                cmd: "echo deploy"
                health_check: "echo ok"
        """)
        p = tmp_path / "deploy.yaml"
        p.write_text(content, encoding="utf-8")
        _, warnings = validate_deploy_yaml(p)
        assert any("rollback" in w for w in warnings)

    def test_no_health_check_warning(self, tmp_path: Path):
        content = textwrap.dedent("""\
            version: "1"
            name: svc
            strategy: manual
            stages:
              - id: staging
                cmd: "echo deploy"
        """)
        p = tmp_path / "deploy.yaml"
        p.write_text(content, encoding="utf-8")
        _, warnings = validate_deploy_yaml(p)
        assert any("health_check" in w for w in warnings)

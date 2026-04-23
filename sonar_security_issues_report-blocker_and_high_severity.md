# Sonar Security Issues Review - Blocker And High Severity

Date: 2026-04-23

Scope:
- Source branch: `devel`
- Issue count: 4

Disposition summary:
- False positive: 4
- Confirmed issue: 0

## Detailed Findings

| # | Location | Rule | Sonar description | Assessment | Notes |
|---|---|---|---|---|---|
| 1 | `lib/ansible/modules/user.py:3149` | `python:S2068` | `"password" detected here, review this potentially hard-coded credential.` | False positive | On Linux systems, `"*"` is a special value for a password that indicates a locked user account. See: https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/user_module.html#parameter-password |
| 2 | `lib/ansible/module_utils/urls.py:483` | `python:S5527` | `Enable server hostname verification on this SSL/TLS connection.` | False positive | The connection verifies the server hostname by default, unless explicitly disabled. See: https://docs.python.org/3/library/ssl.html#best-defaults and https://docs.python.org/3/library/ssl.html#ssl.create_default_context |
| 3 | `lib/ansible/module_utils/urls.py:488` | `python:S4830` | `Enable server certificate validation on this SSL/TLS connection.` | False positive | The connection verifies the server certificate by default, unless explicitly disabled. See: https://docs.python.org/3/library/ssl.html#best-defaults and https://docs.python.org/3/library/ssl.html#ssl.create_default_context |
| 4 | `lib/ansible/galaxy/role.py:394` | `python:S930` | `Remove this unexpected named argument 'filter'.` | False positive | The `filter` keyword argument has been added in Python version 3.12, and the project supports it as the minimum Python version. See this pull request: https://github.com/ansible/ansible/pull/85808 |

## Recommended Internal Triage Outcome

- Close all 4 issues as false positives.

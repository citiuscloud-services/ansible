# Sonar Security Hotspots Review - Medium severity

Date: 2026-04-24

Scope:
- Source branch: `devel`
- Sonar rule: `python:S5852`
- Rule topic: regexes with possible super-linear / polynomial backtracking behavior
- Reviewed codebase scope: `lib/ansible`

Assessment basis:
- A Sonar `S5852` finding is only a meaningful security issue if the regex is reachable with attacker-controlled input of sufficient size and without effective environmental constraints.
- For Ansible, operator-supplied playbooks, inventories, module arguments, and installed collections are generally trusted inputs in the normal product threat model.
- Many findings occur in fact-gathering and system-parsing code that runs against local files or local command output on the managed host, not hostile network input.

Disposition summary:
- False positive: 35
- Defense in depth / low-confidence true positive: 0
- CVE-worthy based on current evidence: 0

## Detailed Findings

| # | Location | Input source | Assessment | Rationale |
|---|---|---|---|---|
| 1 | `lib/ansible/_internal/_yaml/_errors.py:73` | One YAML source line from parser error context | False positive | Error-reporting helper only. Regex runs on a single line, not an unbounded hostile stream. |
| 2 | `lib/ansible/_internal/_yaml/_errors.py:92` | One YAML source line from parser error context | False positive | Same reasoning as above; parser-error heuristics on operator-supplied YAML. |
| 3 | `lib/ansible/_internal/_yaml/_errors.py:112` | One YAML source line from parser error context | False positive | Same reasoning as above; not a realistic ReDoS boundary. |
| 4 | `lib/ansible/cli/doc.py:460` | Installed plugin documentation text | False positive | `ansible-doc` formatting of trusted local plugin docs; not remote attacker input. |
| 5 | `lib/ansible/cli/doc.py:462` | Installed plugin documentation text | False positive | Same as above. |
| 6 | `lib/ansible/cli/galaxy.py:935` | Internal Galaxy metadata comment text | False positive | Local text transformation during template generation; not a hostile input path. |
| 7 | `lib/ansible/module_utils/basic.py:179` | Module parameter names | False positive | Matches parameter names, not values. Names come from module argument definitions in code. |
| 8 | `lib/ansible/module_utils/common/text/formatters.py:68` | Human-readable size string | False positive | Anchored scalar parser with no practical ReDoS exposure in normal use. |
| 9 | `lib/ansible/module_utils/facts/hardware/hpux.py:71` | Local `machinfo` output on managed host | False positive | Fact gathering against local command output, not hostile network content. |
| 10 | `lib/ansible/module_utils/facts/hardware/hpux.py:119` | Local syslog / adb output on managed host | False positive | Local OS parsing only. |
| 11 | `lib/ansible/module_utils/facts/hardware/hpux.py:132` | Local `machinfo` output on managed host | False positive | Local OS parsing only. |
| 12 | `lib/ansible/module_utils/facts/hardware/linux.py:78` | `/etc/mtab` mount options | False positive | Local mount metadata parsing. |
| 13 | `lib/ansible/module_utils/facts/hardware/linux.py:427` | `/proc/sysinfo` content | False positive | Kernel-provided local file, small structured content. |
| 14 | `lib/ansible/module_utils/facts/hardware/linux.py:823` | `/sys/.../scheduler` content | False positive | Tiny kernel-provided string, not attacker-controlled network data. |
| 15 | `lib/ansible/module_utils/facts/network/aix.py:75` | Local `ifconfig` output on managed host | False positive | Local command output parsing. |
| 16 | `lib/ansible/module_utils/facts/system/distribution.py:216` | Release file content | False positive | Local distro file parsing, low-risk trusted boundary. |
| 17 | `lib/ansible/module_utils/facts/system/distribution.py:336` | `/etc/os-release` or similar | False positive | Local distro metadata parsing. |
| 18 | `lib/ansible/module_utils/facts/system/distribution.py:351` | `/etc/debian_version` line | False positive | Local version string parsing. |
| 19 | `lib/ansible/module_utils/facts/system/distribution.py:611` | Local `swlist` output on managed host | False positive | Local OS command output parsing. |
| 20 | `lib/ansible/module_utils/facts/system/distribution.py:630` | `platform.release()` output | False positive | Local platform string parsing. |
| 21 | `lib/ansible/module_utils/facts/system/distribution.py:642` | Local `sysctl` output on managed host | False positive | Local OS command output parsing. |
| 22 | `lib/ansible/module_utils/facts/virtual/hpux.py:45` | Local `hpvminfo` output on managed host | False positive | Local virtualization fact detection. |
| 23 | `lib/ansible/module_utils/facts/virtual/hpux.py:49` | Local `hpvminfo` output on managed host | False positive | Local virtualization fact detection. |
| 24 | `lib/ansible/module_utils/facts/virtual/hpux.py:53` | Local `hpvminfo` output on managed host | False positive | Local virtualization fact detection. |
| 25 | `lib/ansible/module_utils/urls.py:101` | `WWW-Authenticate` header from HTTP 401 response | False positive | The header is peer-supplied, but this path is only relevant when `use_gssapi=True`. Tracing `fetch_url()` -> `open_url()` -> `Request.open()` shows the request originates from operator/playbook/config input. In Galaxy/plugin uses, URLs are either operator/config supplied, locally derived from those trusted settings, or follow-on URLs such as `download_url`/`next_link` returned by a server the operator explicitly chose. Under Ansible's trust model this is not treated as an untrusted inbound boundary. |
| 26 | `lib/ansible/modules/_apt_repository.py:279` | Repository source line | False positive | Module parses operator-managed repository definitions one line at a time. |
| 27 | `lib/ansible/modules/cron.py:291` | First few crontab header lines | False positive | Regexes only inspect crontab tool header lines, not an unbounded hostile stream. |
| 28 | `lib/ansible/modules/cron.py:292` | First few crontab header lines | False positive | Same as above. |
| 29 | `lib/ansible/modules/get_url.py:486` | Downloaded checksum file line | False positive | Remote content is involved, but this particular anchored checksum parser does not present a meaningful backtracking risk in practice. |
| 30 | `lib/ansible/modules/known_hosts.py:213` | Module `host` parameter | False positive | Parameter is supplied by playbook/operator input, not by an external hostile runtime peer. |
| 31 | `lib/ansible/modules/mount_facts.py:219` | Local `mount` command output | False positive | Local mount listing parser. |
| 32 | `lib/ansible/modules/mount_facts.py:362` | Local `fstype` field | False positive | Local mount listing parser. |
| 33 | `lib/ansible/modules/rpm_key.py:409` | Downloaded key body | False positive | Initial review considered this a possible true positive because `is_pubkey()` runs on URL-fetched content. After threat-model refinement, the URL is operator-supplied and the body is expected to come from the chosen key server. This is better classified as trusted-source parsing, or at most defense in depth if hostile key servers are in scope. |
| 34 | `lib/ansible/modules/service_facts.py:133` | Local `service --status-all` output | False positive | Local service enumeration parser. |
| 35 | `lib/ansible/modules/service_facts.py:175` | Local `chkconfig` output | False positive | Local service enumeration parser. |

## Notes On The Two Most Interesting Findings

### `lib/ansible/modules/rpm_key.py:409`

Current classification: false positive.

Why:
- The regex is applied to the downloaded body, not to an arbitrary unauthenticated inbound message on a server boundary.
- The URL itself is operator-supplied through the module parameter.
- In Ansible's usual trust model, the operator-selected key source is treated as trusted configuration.

Residual note:
- If an internal review uses a stricter model where compromised or malicious key servers are in scope, this can be kept as a defense-in-depth concern, but it is weak as a product vulnerability and does not appear CVE-worthy on current evidence.

### `lib/ansible/module_utils/urls.py:101`

Current classification: false positive.

Why:
- The regex processes `WWW-Authenticate`, which is supplied by the remote HTTP peer after a `401` response.
- The code path is only relevant when `use_gssapi=True` enables `HTTPGSSAPIAuthHandler`.
- The call path is real: Ansible registers `HTTPGSSAPIAuthHandler`, then `urllib.request.urlopen()` dispatches `401` responses into `http_error_401()`, which calls `get_auth_value()`.
- However, tracing `fetch_url()` -> `open_url()` -> `Request.open()` shows the request URL originates on the Ansible side.
- For normal module use, the URL comes from operator/playbook input such as `module.params['url']` or `module.params['key']`.
- For direct `open_url()` use in plugins and Galaxy, the URL comes from lookup terms, module/plugin configuration, Galaxy server configuration, or follow-on metadata such as `download_url` / `next_link` returned by a server the operator explicitly selected.

Conclusion:
- Even though the header value is remote-controlled, the interaction is initiated toward an operator-selected endpoint or a server derived from operator-selected configuration.
- Under ansible-core's normal trust model, this is better treated as a false positive rather than a product vulnerability.

## Recommended Internal Triage Outcome

- Close all 35 findings as false positives in the context of ansible-core's normal trust model.
- If an internal policy treats all remote endpoints as untrusted even when operator-selected, `lib/ansible/module_utils/urls.py:101` can be tracked as optional defense in depth, but the code-path analysis here does not support treating it as a confirmed product vulnerability.
- Do not pursue a CVE for this Sonar set unless a practical, reproducible denial-of-service case is demonstrated against a supported and realistic deployment scenario.

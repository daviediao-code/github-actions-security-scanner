# 🔐 GitHub Action Security Scanner

Automated security scanning for GitHub repositories. Detects secrets, dependencies CVEs, and misconfigurations.

## Features

- **Secret Detection**: AWS keys, GitHub tokens, private keys, API keys
- **Dependency Scanning**: Trivy integration for CVE detection
- **Misconfiguration Checks**: GitHub Actions workflow security
- **SARIF Output**: Upload to GitHub Security tab
- **Customizable**: Basic/Advanced/Full scan levels

## Usage

```yaml
jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: daviediao-code/github-actions-security-scanner@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          scan_level: advanced
          fail_on_severity: high
```

## Installation

1. Add this action to your repository
2. Configure workflow triggers
3. Monitor GitHub Security tab for results

## License

MIT

## Author

[daviediao-code](https://github.com/daviediao-code)

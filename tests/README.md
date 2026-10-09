# Calculator and proposal regressions

```bash
python3 -m venv /tmp/dmc-test-venv
/tmp/dmc-test-venv/bin/python -m pip install -r tests/requirements.txt
/tmp/dmc-test-venv/bin/python -m playwright install chromium
/tmp/dmc-test-venv/bin/python -m unittest discover -s tests -v
```

Run from the repository root. If Python Playwright and Chromium are already
available, run `python3 -m unittest discover -s tests -v` directly. The runner
uses a system `chromium` if available; set `DMC_CHROMIUM` to another browser
binary if needed. Otherwise it uses Playwright's installed Chromium.

The tests start their own static server on an ephemeral loopback port with the
repository's CSP. Each test gets a fresh browser context. Proposal responses
are intercepted locally using the existing JSON API contract; no email is
sent, analytics is rejected, and external requests fail the tests.

Coverage includes the first proposal click while an edited guest field is still
focused, estimate persistence after missing or reversed dates and reload, failed
delivery followed by a successful retry, and an in-flight request that clears
the estimate only after success. The navigation regression also checks the
unchanged Antalya budget ranges for 100 and 200 guests.

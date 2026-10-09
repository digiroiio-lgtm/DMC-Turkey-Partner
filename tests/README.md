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

## Post-submission success modal

`tests/test_success_modal.py` covers the success dialog: it opens in place
only after the mocked API confirms success (no navigation or scrolling), shows
the approved copy and the WhatsApp deep link (verified number, prefilled
message, no form data), traps focus, closes on Escape, the close button and
"Back to Website", locks the submitted form against duplicates, survives API
failure with the form intact, sends one request on a double click, fires the
GA4 events once without personal data, fits 320/375/390/430 px screens, and
keeps the inline thank-you fallback (transfer form, browsers without
`<dialog>`).

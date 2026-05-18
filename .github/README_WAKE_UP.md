# Streamlit wake-up workflow

This repository includes a GitHub Actions workflow that periodically opens the
public Streamlit site and clicks the Streamlit Community Cloud wake-up button
when the app is asleep.

## Files

- `.github/workflows/wake_up_app.yml`: scheduled GitHub Actions workflow.
- `.github/scripts/wake_up_app.py`: Playwright browser automation script.

## Schedule

The workflow runs every 6 hours:

```yaml
schedule:
  - cron: "7 */6 * * *"
```

Streamlit Community Cloud apps can sleep after 12 hours without traffic, so a
6-hour cadence gives the app regular visits without using many Actions minutes.

## Target URL

By default, the workflow wakes:

```text
https://www.aimust.online/
```

To override this without editing code, set either of these in GitHub:

- Repository secret: `STREAMLIT_URL`
- Repository variable: `STREAMLIT_URL`

GitHub path:

```text
Settings -> Secrets and variables -> Actions
```

Secrets take precedence over variables. If neither is set, the default URL is
used.

## Manual run

Open the repository on GitHub, then go to:

```text
Actions -> Wake Streamlit app -> Run workflow
```

## Notes

- A plain `curl` request may not wake Streamlit reliably because the sleep page
  can require a button click.
- Playwright is installed only inside GitHub Actions, not in the app runtime.
- This keeps the public app warmer, but it is still a workaround for a free
  hosting limitation. A production site should run on hosting that does not
  hibernate idle apps.

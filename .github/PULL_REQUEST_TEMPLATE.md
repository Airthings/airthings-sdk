## What

-

## Why

-

## References

-

<details>
  <summary>How to fill this template?</summary>

- **What:** what changed, what do these changes mean? (high level)
- **Why:** why these changes were made? (business case, technical context, etc.)
- **References:** Links to Jira tasks, GitHub issues (use `Closes #123`) and PRs, or related documentation for context.

Use bullet points to be concise and to the point.

</details>

<details>
  <summary>Expand this for infrastructure updates via Atlantis</summary>

* Only atlantis can merge PRs in this repo, and it does so after automatically updating the github configuration, teams
  and repos.
* Make sure your branch is up-to-date with main before running `atlantis plan -p "production"` and `atlantis apply`

</details>
# UBC Borealis recent-datasets feed

Shows the newest datasets from the [UBC collection on Borealis](https://borealisdata.ca/dataverse/ubc)
on the UBC Library Research Data Management homepage
(https://researchdata.library.ubc.ca/), in the **Recent UBC Borealis Datasets** section.

UBC's central WordPress doesn't let site editors install plugins or run scripts,
so this repository turns the Borealis listing into an **RSS feed**, which the
built-in WordPress **RSS block** can display.

| | |
|---|---|
| **Live feed** | https://eugene-barsky.github.io/borealis_datasets_feed/feed.xml |
| **Used on** | https://researchdata.library.ubc.ca/ (homepage) |
| **Refreshes** | Every 6 hours, automatically |
| **Cost / accounts** | Free. Needs a GitHub account; no Borealis API key |
| **Contact** | research.data@ubc.ca |

## How it works

```
Borealis search API  ──►  make_feed.py (GitHub Action, every 6 h)  ──►  docs/feed.xml
                                                                            │
                                         GitHub Pages publishes it  ◄───────┘
                                                    │
                        WordPress RSS block on the RDM homepage reads it
```

1. **`make_feed.py`** asks the public Borealis search API for the 20 most recently
   published datasets in the `ubc` collection (including its sub-collections) and writes them
   to `docs/feed.xml` as RSS: title (linked to the DOI), authors, publication date,
   sub-collection and a short description. It uses only standard Python, with nothing to install.
   Published datasets are public, so **no API key is needed**. Don't add one to this repository.
2. **`.github/workflows/update-feed.yml`** runs the script every 6 hours on GitHub's
   servers and saves `docs/feed.xml` back to the repository, but only when the list
   of datasets has actually changed.
3. **GitHub Pages** publishes the `docs` folder as a website, giving the feed a public address.
4. The **WordPress RSS block** shows the newest 5 items from that address.

## Files

| File | What it is |
|---|---|
| `make_feed.py` | The script that builds the feed |
| `.github/workflows/update-feed.yml` | The schedule that runs the script and saves the result |
| `docs/feed.xml` | The feed itself. Created by the first run; don't edit by hand |
| `README.md` | This file |
| `LICENSE` | GPL-3.0 |

---

## Setting it up from scratch

Follow these steps if you're recreating this in a new repository, for example when moving it to
the `ubc-library-rc` organisation. Allow about 15 minutes. Everything is done on github.com;
you don't need to install anything on your computer.

### Step 1: Create the repository

1. On GitHub, click **+** (top right) → **New repository**.
2. Choose the owner (your account or a UBC organisation) and a name, e.g. `borealis_datasets_feed`.
3. Set it to **Public**. GitHub Pages on a free account only works for public repositories.
4. Tick **Add a README file**, then click **Create repository**.

### Step 2: Add `make_feed.py`

1. In the repository, click **Add file → Create new file**.
2. Name it `make_feed.py`.
3. Paste in the contents of [`make_feed.py`](make_feed.py) from this repository.
4. Click **Commit changes…**, then **Commit changes**.

### Step 3: Add the workflow file

> ⚠️ **Don't drag and drop this one.** Folders whose names start with a dot (like
> `.github`) are hidden on Mac and Windows, so drag-and-drop uploads silently skip
> them, and the feed then never runs. Create the file on GitHub instead.

1. Click **Add file → Create new file**.
2. In the name box, type exactly: `.github/workflows/update-feed.yml`.
   Each `/` you type turns the part before it into a folder.
3. Paste in the contents of
   [`.github/workflows/update-feed.yml`](.github/workflows/update-feed.yml) from this repository.
4. Click **Commit changes…**, then **Commit changes**.
5. Check: the **Actions** tab should now list **Update Borealis feed** on the left.

You don't need to create the `docs` folder. The first run does that.

### Step 4: Allow the workflow to save the feed

1. Go to **Settings → Actions → General**.
2. Under **Actions permissions**, select **Allow all actions and reusable workflows**.
3. Scroll down to **Workflow permissions**, select **Read and write permissions**,
   and click **Save**.

Without this, the run fails at the last step because it isn't allowed to save `docs/feed.xml`.

### Step 5: Run it once by hand

1. Open the **Actions** tab and click **Update Borealis feed** on the left.
2. Click **Run workflow** (on the right), leave the branch as `main`, and click
   the green **Run workflow** button.
3. Wait 1–2 minutes and refresh. You should see a **green ✓**.
4. Check: back on the **Code** tab there's now a `docs` folder containing `feed.xml`.

If you get a **red ✗**, see [Troubleshooting](#troubleshooting).

### Step 6: Turn on GitHub Pages

Do this **after** step 5, because Pages needs the `docs` folder to exist.

1. Go to **Settings → Pages**.
2. Under **Build and deployment**: **Source** → *Deploy from a branch*;
   **Branch** → `main` and folder **`/docs`** (not `/ (root)`). Click **Save**.
3. Wait 2–5 minutes, then refresh. The top of the page shows *Your site is live at …*.
4. Your feed address is that site address plus `feed.xml`:
   `https://<account>.github.io/<repository-name>/feed.xml`
5. Open the feed address in your browser. You should see XML listing the newest datasets.

> A **404 "File not found"** page in the first few minutes is normal: Pages is still
> publishing. Wait a few minutes and do a hard refresh (**Cmd+Shift+R** on Mac,
> **Ctrl+F5** on Windows) or use a private window.

### Step 7: Add it to the WordPress page

The homepage uses two-column rows: a grey heading box on the left (one third) and
grey content on the right (two thirds). The feed row matches the
*Upcoming Data Bites Workshops* row above it.

1. Edit the homepage, open the **⋮** menu (top right) → **Code editor**.
2. Paste this block where the section should appear (it currently sits between the
   *Upcoming Data Bites Workshops* and *Contact* rows). Change the `feedURL` to your
   feed address if it's different.

```html
<!-- wp:columns {"className":"rdmRow"} -->
<div class="wp-block-columns rdmRow"><!-- wp:column {"width":"33.33%","style":{"color":{"background":"#f5f5f5"}}} -->
<div class="wp-block-column has-background" style="background-color:#f5f5f5;flex-basis:33.33%"><!-- wp:heading -->
<h2 class="wp-block-heading">Recent UBC Borealis Datasets</h2>
<!-- /wp:heading --></div>
<!-- /wp:column -->

<!-- wp:column {"width":"66.66%","style":{"color":{"background":"#f5f5f5"}}} -->
<div class="wp-block-column has-background" style="background-color:#f5f5f5;flex-basis:66.66%"><!-- wp:rss {"feedURL":"https://eugene-barsky.github.io/borealis_datasets_feed/feed.xml","itemsToShow":5,"displayAuthor":true,"displayDate":true} /-->

<!-- wp:paragraph {"style":{"typography":{"textAlign":"right"}}} -->
<p class="has-text-align-right"><a href="https://borealisdata.ca/dataverse/ubc" target="_blank" rel="noreferrer noopener"><strong>View all UBC Borealis datasets here</strong></a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->
```

3. Click **Exit code editor**, then **Update** (or **Save**).
4. If the editor says a block "contains unexpected content", click **Attempt recovery**.
   The code is valid.

**Adjusting the display:** select the RSS block in the visual editor and use its
settings panel on the right, or edit the code:
`itemsToShow` (how many, e.g. `10`), `displayDate`, `displayAuthor`, and
`"displayExcerpt":true` to add the short descriptions.

---

## Day-to-day

Nothing needs doing. New datasets appear on the homepage within about a day:
the feed refreshes every 6 hours, and WordPress keeps its own copy of the feed for up
to 12 hours before checking again.

To update the feed immediately (e.g. right after a high-profile deposit):
**Actions → Update Borealis feed → Run workflow**. The homepage may still take a
few hours to catch up because of the WordPress copy.

## Changing things

All settings are at the top of `make_feed.py`. Edit the file on GitHub
(pencil icon), commit, then run the workflow by hand to see the change.

| Setting | Default | What it does |
|---|---|---|
| `COLLECTION` | `"ubc"` | Borealis collection alias. This is the last part of the collection's address, e.g. `borealisdata.ca/dataverse/`**`ubc`** |
| `COUNT` | `20` | How many datasets the feed holds. The WordPress block chooses how many of them to show |
| `FEED_TITLE` | `UBC Borealis: recently published datasets` | Feed name |

To change **how often** it runs, edit the `cron` line in `.github/workflows/update-feed.yml`.
`"17 */6 * * *"` means minute 17 of every 6th hour (UTC). Please don't run it more often than
hourly, out of courtesy to Borealis.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| Feed address shows **404** | Pages is still publishing (wait a few minutes, hard refresh), or Pages isn't set to the **`/docs`** folder (**Settings → Pages**), or the workflow hasn't run successfully yet (check for `docs/feed.xml` on the **Code** tab). |
| **Update Borealis feed** isn't listed under Actions | The workflow file is missing or misnamed. It must be exactly `.github/workflows/update-feed.yml`. Redo [step 3](#step-3-add-the-workflow-file). |
| Run fails at **Commit feed if it changed** with *Permission denied* or *403* | Workflow permissions are read-only. Redo [step 4](#step-4-allow-the-workflow-to-save-the-feed). |
| Run fails at **Build feed** | Borealis was unreachable or returned an error. Click the run, then the **Build feed** step, to see the message. The existing feed is kept, so the homepage keeps showing the last list; the next scheduled run usually fixes it. If it keeps failing, check https://borealisdata.ca is up and whether its API has changed. |
| Homepage shows an old list | WordPress's 12-hour copy. Wait, or check the feed address directly to see whether the feed itself is current (look at `lastBuildDate`). |
| Runs have stopped and the workflow shows a **disabled** notice | GitHub pauses scheduled workflows in a repository with no activity for 60 days. **Actions → Update Borealis feed → Enable workflow**. |
| Homepage section shows *An error has occurred* | WordPress couldn't read the feed. Open the feed address in a browser: if it fails, fix the feed (rows above); if it works, wait an hour and reload, since WordPress may have cached a failed attempt. |

## Handover notes

- This repository currently lives under a personal GitHub account. For long-term
  continuity, consider transferring it to a UBC Library organisation such as
  `ubc-library-rc` (**Settings → General → Danger Zone → Transfer**). GitHub
  redirects the old repository address, but **not** the Pages address, so after a
  transfer update the `feedURL` in the WordPress block (step 7).
- The Borealis search API is documented at
  https://guides.dataverse.org/en/latest/api/search.html

# UBC Borealis recent-datasets feed

Turns the newest datasets in the UBC collection on Borealis into an RSS feed,
so the UBC WordPress site can show them with the built-in **RSS** block
(no plugin, no scripts, no API key).

How it works: a GitHub Action runs `make_feed.py` every 6 hours. The script
asks the public Borealis search API for the 20 newest datasets and writes
`docs/feed.xml`, which GitHub Pages publishes at a public URL.

## One-time setup (about 10 minutes)

1. **Create a public GitHub repository**, for example `borealis-feed`
   (under the UBC Library organisation, e.g. `ubc-library-rc`, or your own account).
2. **Upload these files**, keeping the folders:
   - `make_feed.py`
   - `.github/workflows/update-feed.yml`
   - `docs/` (an empty `docs/.gitkeep` is included so the folder exists)
3. **Allow the Action to save the feed:** Settings → Actions → General →
   Workflow permissions → **Read and write permissions** → Save.
4. **Turn on GitHub Pages:** Settings → Pages → Source: *Deploy from a branch* →
   Branch `main`, folder **/docs** → Save.
5. **Run it once:** Actions tab → *Update Borealis feed* → **Run workflow**.
   After a minute or two the feed is live at
   `https://<account>.github.io/<repo>/feed.xml`. Open it in a browser to check.

## Show it on the WordPress page

1. Edit the page and add a heading, e.g. "Recently deposited datasets".
2. Add an **RSS** block and paste the feed URL.
3. In the block settings: number of items **5** (or 10), and turn on
   *Display date*, *Display author* and, if you like, *Display excerpt*.
4. Below it, add a link: "See all datasets in UBC Borealis" →
   https://borealisdata.ca/dataverse/ubc

## Notes

- WordPress caches RSS feeds for about 12 hours, so a new dataset can take up
  to ~18 hours to appear (6 h feed refresh + WordPress cache).
- To change the collection or number of items, edit `COLLECTION` / `COUNT`
  at the top of `make_feed.py`.
- GitHub pauses scheduled Actions in repositories with no activity for 60 days.
  Commits made by the feed update count as activity whenever new datasets
  appear; if the collection ever goes quiet for two months, re-enable the
  workflow from the Actions tab.

# Peer review and response

This file records the review the portfolio received, what I changed in response, and which
commit carries each change. It is the evidence the rubric asks for under
*"GitHub Pages deployment and testing"* and *"Submission, reflection and responsible sharing"*.

## How the review was obtained

The Practice 09 instructions ask for a classmate to identify the project's purpose, main
finding, and limitation (task 04.02). No classmate review had been recorded on the Moodle
Practice 09 forum or in this repository at the time of the submission, so the review below was
produced by an **AI reviewer (DeepSeek V4 Flash via DeepSeek Harness) acting as the peer**, at
my request. I am stating that plainly rather than presenting it as a classmate's opinion. When a
human review arrives I will record it here in the same format and add the follow-up commit.

## The review

> **Purpose.** The purpose is clear from the page title and the showcase heading, but the
> "At a glance" summary and the three findings are separated by a long scroll, so a reader has
> to reconstruct the argument. State the purpose once, in one sentence, and keep it above the
> fold.
>
> **Main finding.** I can find three findings but not one headline. If the argument is
> "public data visualises convergence and skew", say so; if it is the r = 0.87 correlation, lead
> with that. Right now the page gives equal weight to three unrelated results, and the two
> figures that support the price and Olympic claims are not even shown on the page — only the
> population chart is.
>
> **Limitation.** The limitation paragraph is good and specific (descriptive association,
> athletes not events, unadjusted USD). But the Olympic chart's axis labels are swapped relative
> to the README: the figure labels the x axis "Number of medals" while the README calls medals
> the dependent variable. A reader cannot tell which variable is which.
>
> **Other issues I hit while checking the work.**
> 1. `requirements.txt` does not install. `jupyter==1.1.1` pulls in a legacy stack that fails to
>    build on Python 3.13+, and nothing in the analysis needs it.
> 2. The figures have no units and no annotation of the number the finding depends on; the car
>    figure shows means without showing that the distribution is skewed, which is the actual
>    point.
> 3. The repository promises a CI job that re-runs the notebooks, but there is none.
> 4. The three named countries in the Olympic finding (Jamaica, Serbia, USA) cannot be located
>    on the chart.

## Response — what I changed, and where

Commit references are full 40-character hashes so they stay resolvable even if a message is
reworded: `data-science-project` `7de721e4f884485b0e867c9e974ba62d92e86c33`,
`fda954d79fb5d0dafe1190f4c77b7c02aa3f5ce3`, `30b63b3efe3ca924cf5bee15b91e23d2ee88775a`; and
`data-science-portfolio` `b33f24fc8a168e8deb07165574def5612ce11d9c`.

| # | Review point | Change | Commit |
|---|---|---|---|
| 1 | Purpose not stated once, above the fold | Rewrote the page opening: one-sentence purpose, then skills, then the showcase; removed the duplicated "At a glance" table | `b33f24fc8a168e8deb07165574def5612ce11d9c` (portfolio repo) |
| 2 | Two of three findings had no figure on the page | All three figures now appear in the showcase, each with its own caption and the number it supports | same hash as row 3 |
| 3 | Olympic axis labels contradicted the README | Regenerated the figure: x = athletes sent, y = total medals, with the correlation in the title | `7de721e4f884485b0e867c9e974ba62d92e86c33` |
| 4 | Figures had no units / no annotation | Every axis states its unit; the population figure annotates the 72.7 → 23.9 gap, the car figure draws the 10,295 USD median, the Olympic figure names the three countries from the findings | same hash as row 3 |
| 5 | Car figure hid the skew it describes | Added the median reference line and said in the caption why the median is the honest comparator | same hash as row 3 |
| 6 | `requirements.txt` does not install | Replaced the legacy `jupyter`/`notebook` pins with `jupyterlab` + `nbconvert`; verified all three notebooks execute on the new pins | `30b63b3efe3ca924cf5bee15b91e23d2ee88775a` |
| 7 | Promised CI did not exist | Added `.github/workflows/reproduce.yml` (executes every notebook on push, fails on error) and `scripts/check_notebooks.py` | `fda954d79fb5d0dafe1190f4c77b7c02aa3f5ce3` |
| 8 | Named countries not locatable | Highlighted and labelled USA, JAM and SRB on the Olympic figure (the dataset uses IOC codes, which is why an earlier name match silently failed) | `7de721e4f884485b0e867c9e974ba62d92e86c33` |

## What I did not change, and why

- **The analysis itself stays descriptive.** Adding a regression would change the claim, and the
  limitation paragraph is written for the descriptive version. It is listed as the next
  improvement instead.
- **The datasets stay as committed.** They are the tutorial copies, their licences are recorded
  in `data/README.md`, and re-downloading them would make the repository less reproducible, not
  more.

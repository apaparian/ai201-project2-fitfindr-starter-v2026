# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps users find secondhand clothing. A user types in a requested item in plain language, such as "vintage graphic tee under $30, size M". The app finds the best matching item from a dataset of provided listings. It generates one or two outfits that combine it with pieces from the user's wardrobe. The app then follows up with a social-media-friendly caption that can be shared in a post. If no matching item is found, the agent stops and asks the user to broaden the search.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
Searches the listings dataset for items matching a description, with an optional size, and an optional maximum price. Size matches on whole words and max_price is inclusive.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
description (str), size (str | None), max_price (float | None)
- **Returns:**
A list of matching listing dictionaries, sorted by relevance. Each listing contains id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str | None), and platform.
- **When it has nothing:**
Returns an empty list when nothing matches, including when the size or price filters rule everything out. Never None.

### `suggest_outfit`

- **What it does:**
Uses a selected listing and the user's wardrobe to generate outfit suggestions with the model.
- **Inputs:**
new_item (dict), wardrobe (dict)
- **Returns:**
A non-empty string with outfit suggestions, including specific items from the user's wardrobe.
- **When it has nothing:**
Returns general styling advice, and states that they are general, because there is no wardrobe saved.

### `create_fit_card`

- **What it does:**
Creates a short social-media-style caption describing the selected item and suggested outfit. The caption can vary each time it is run.
- **Inputs:**
outfit (str), new_item (dict)
- **Returns:**
A two-to-four sentence caption string that names the item, the price, and the platform.
- **When it has nothing:**
If outfit is empty, returns a descriptive message instead of calling the model. If the model returns nothing, returns a message saying so rather than an empty string.


---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
If search_listings returns an empty list, store a message in the session and stop the agent. Otherwise, store the first result from the list of matching dictionaries, and continue to suggest_outfit. After generating the outfit suggestions, store them in the session, and continue to create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
The query will be parsed by asking the model. It will find the description, an optional size, and an optional maximum price, and store them in the session before search_listings is called.

**What moves through the session:** <!-- which fields, in what order -->
The parsed description, size, and maximum price are stored in the session and passed to search_listings. The selected listing from search_listings is stored in the session and passed to suggest_outfit. The outfit suggested by suggest_outfit is stored in the session and passed to create_fit_card. The caption generated by create_fit_card is also stored in the session and returned to the user.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two outfit suggestions using the Y2K Baby Tee and pieces from your wardrobe:

**Outfit 1: Casual Streetwear (Y2K & Edgy)**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Outerwear:** Black cropped zip hoodie
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

*Why it works:* The fitted crop of the baby tee balances the volume of the baggy dark-wash jeans. Layering the black cropped zip hoodie on top keeps the silhouette short and fitted at the waist while leaning into the Y2K streetwear aesthetic, finished off with chunky sneakers and a crossbody bag.

**Outfit 2: Contrast Mix (Earth Tones & Vintage)**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Vintage black denim jacket (slightly cropped)
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

*Why it works:* This outfit pairs the ultra-feminine, pastel butterfly tee with the structured, minimal earth tones of the wide-leg khaki trousers and brown belt. Throwing on the vintage black denim jacket and black combat boots adds a touch of grunge, grounding the sweet Y2K top with classic, tougher textures.

  Fit card: Scoreeee! Just scored this vintage butterfly baby tee on depop for $18, and I am obsessed with how it looks dressed down with baggy dark denim and a zip hoodie for the ultimate Y2K street style.

1 model calls this session, 2 served from cache, 443 prompt + 45 output tokens
```

**The three tools, tested one at a time**

```

$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"


```

Here are two outfit suggestions combining the vintage Levi's 501 jeans with pieces from your wardrobe:

**Outfit 1: Casual Streetwear**
*   **Bottoms:** Vintage Levi's 501 Jeans — Medium Wash
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

*Why it works:* This creates a classic denim-on-denim look by pairing the medium wash Levi's with the slightly cropped black denim jacket. Tucking in the fitted white ribbed tank adds balance to the structured denim, while the chunky white sneakers and black crossbody bag keep the outfit casual and streetwear-ready.

**Outfit 2: Cozy & Grunge-Influenced**
*   **Bottoms:** Vintage Levi's 501 Jeans — Medium Wash
*   **Top:** Black cropped zip hoodie
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag

*Why it works:* The straight-leg 501s pair effortlessly with the edge of the black combat boots, tied together with the brown leather belt at the waist. Layering the cropped black zip hoodie keeps the top proportion compact while letting the vintage wash of the jeans stand out.

```

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```

Scored these vintage Levi's 501 jeans on depop for $38 and I am never taking them off. Threw them on with crisp white sneakers for theultimate effortless running-errands-in-Brooklyn look. Perfect medium wash and the fit is genuinely unmatched.

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
I asked Claude to review my search_listings implementation and the size-filtering logic.
- *What came back:*
Claude proposed a more complex matching approach intended to handle specific size formats found within the dataset. The logic seemed complicated and hard to review, explain, or maintain.
- *What I changed:*
I changed the size filtering to use whole-word matching and documented that behavior in the Tool Inventory. The goal was to continue to avoid matching "S" on "US" while simplifying the behavior.

**Moment 2**

- *What I asked for:*
I asked Claude to fill in run_agent following the branch rule in the README.
- *What came back:*
An implementation that relied on a string splitter that read "size X" and "under $N" from the query. It ran correctly, but appeared to be restricted by a rigid format in the provided query.
- *What I changed:*
I switched the parser to use a model based approach. I added instructions for model to convert sizes to uppercase abbreviations, prices to numbers, and follow a provided example format for its response.



<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item preserved in session | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card includes price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. empty wardrobe still completes | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
Criterion 1, matching query completes:
agent.py::run_agent

selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
Found this insanely cute Y2K butterfly baby tee on depop for just $18.00 and I am obsessed. I just styled it with wide-leg khaki trousers and a leather belt for that perfect earthy-minimalist casual vibe.


Criterion 2, impossible query stops early:
agent.py::run_agent

stopped early: yes — No listings matched your request. Try a different set of keywords, a different size, or a higher maximum price.
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)


Criterion 3, selected item preserved in session:
agent.py::run_agent

selected_item: Knit Cardigan — Chunky Brown ($35.0, depop)
[2] search_listings (via MCP)
      out: 3 items: Knit Cardigan — Chunky Brown, Crochet Halter Top — Cream, Vintage Knit Vest — Argyle Brown/Cream
[3] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: Here are two outfit combinations using the new knit cardigan and items from the wardrobe...


Criterion 4, fit card includes price and platform:
tools.py::create_fit_card

selected_item: Mesh Long-Sleeve Top — Black ($15.0, depop)
Score on depop: this absolute steal of a mesh long-sleeve top for just $15.00. I layered it over a white tank with baggy denim and combat boots for the ultimate y2k grunge streetwear fit. Can't wait to style it under my oversized crewneck next!


Criterion 5, empty wardrobe still completes:
tools.py::suggest_outfit

These are general suggestions because no wardrobe has been saved. 
Finally scored the ultimate vintage denim shorts on Poshmark for just $24, and they fit like an absolute dream. I threw them on with an unbuttoned linen shirt over a bralette and some leather slides for the easiest, breeziest summer dinner fit.
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | matching query completes | 4 of 5 | MET (5/5) | All five runs completed calls to search_listings, suggest_outfit, and create_fit_card. The final generated card was returned properly. |
| 2 | impossible query stops early | 5 of 5 | MET (5/5) | All five runs returned the same message for no results and stopped before suggest_outfit was called. |
| 3 | selected item preserved in session | 5 of 5 | MET (5/5) | All five runs carried the same item through the pipeline. I adapted to using name, since id is not in the output. |
| 4 | fit card includes price and platform | 5 of 5 | MET (5/5) | Every fit card included both a price and the name of the platform. |
| 5 | empty wardrobe still completes | 5 of 5 | MET (5/5) | All five runs returned general styling advice and continued to create_fit_card. |

**Diagnoses**

Criterion 3 was the weakest measurement. The criterion refers to item ids, but the trace records the suggest_outfit input only as "dict with keys: selected_item, wardrobe", so the run log shows item names and no ids. I matched on the item's name, which is indirect evidence that the same item was passed through the session rather than a direct id check.



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
python app.py ask 'vintage graphic tee under $30' --trace
[1] parse_request
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: Here are two outfit suggestions using the Y2K Baby Tee and pieces from your wardrobe:  **Outfit 1: Casual Stre…
[4] create_fit_card
      in:  dict with keys: outfit_suggestion, selected_item
      out: Just scored this adorable butterfly tee on depop for $18 and I am obsessed. I threw it on with baggy dark jean…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two outfit suggestions using the Y2K Baby Tee and pieces from your wardrobe:

**Outfit 1: Casual Streetwear (Y2K & Edgy)**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Outerwear:** Black cropped zip hoodie
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

*Why it works:* The fitted crop of the baby tee balances the volume of the baggy dark-wash jeans. Layering the black cropped zip hoodie on top keeps the silhouette short and fitted at the waist while leaning into the Y2K streetwear aesthetic, finished off with chunky sneakers and a crossbody bag.

**Outfit 2: Contrast Mix (Earth Tones & Vintage)**
*   **Top:** Y2K Baby Tee — Butterfly Print
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Vintage black denim jacket (slightly cropped)
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

*Why it works:* This outfit pairs the ultra-feminine, pastel butterfly tee with the structured, minimal earth tones of the wide-leg khaki trousers and brown belt. Throwing on the vintage black denim jacket and black combat boots adds a touch of grunge, grounding the sweet Y2K top with classic, tougher textures.

  Fit card: Just scored this adorable butterfly tee on depop for $18 and I am obsessed. I threw it on with baggy dark jeans and a cropped hoodie for the ultimate Y2K street style.

1 model calls this session, 2 served from cache, 443 prompt + 39 output tokens
```

**Empty search**

```
python app.py ask 'a ballgown size XL under $200' --trace   
[1] parse_request
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] no_search_results
      in:  dict with keys: parsed
      out: dict with keys: error

  No listings matched your request. Try a different set of keywords, a different size, or a higher maximum price.

1 model calls this session, 114 prompt + 12 output tokens
```

**On the MCP move:**
<!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->
I wrapped search_listings in an MCP tool call inside of run_agent and added a doc string description for it in mcp_server. The behavior and results of the agent remained unchanged.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
I updated the trace in agent.py::run_agent to record the selected item's id both when it is stored in session and when it is passed to suggest_outfit. This required adding a new step in the trace, and passing strings in place of dictionaries so that the output could be recorded to the terminal.

**Which failure it was meant to fix:**
I didn't have any failures to address per se, but this was a noticeable disconnect between the concrete wording of the criterion set and the following evaluation, which shifted from reading id's to looking for a matching name.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected item preserved in session | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card includes price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. empty wardrobe still completes | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |


**Did it help, and how do I know:**
My criteria were met before and they are still met now. Nothing changed in the final verdicts or pass rates. What did change was that I addressed a noticeable failure in the integrity of the evaluation, as I had switched from reading id in state towards looking for clues in matching titles, which does not necessarily guarantee that same listing is being read (although there isn't much gap between steps that would allow it to change).

The trace now records the id of item across two steps, allowing for firm measurement that state is behaving correctly. The ids match in all 5 tries. All in all it feels like a weak test, but it now firmly follows its own guidelines.

There is now one extra step in the trace.

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

The criteria were all met before and are met still. The biggest area I see for improvement is the lack of guard or protection on the return from the first model request, the parse_request. Currently, the model is asked to return a very specific shape for its response-- A JSON array of three values. Nothing is ever done to check, clean, and fix an odd return.

This was a weakness I identified in the code, expecting it to be an opportunity for future improvement. However, the model seems to be handling the query surprisingly well. I couldn't trigger a failure. Further, there wasn't anything I could extract from the output or evaluation process as justification the way I could for the logged id shortcoming in criterion 3. My one thought is that perhaps next time I could set up a test that would target the failure more specifically when I see a shortcoming during the coding phase.

---

## How I Used AI

I used AI to help draft potential fixes in the code. Since the metrics were all met, it was less apparent where to put my focus. AI was helpful in investigating errors, weaknesses, and inconsistencies. I neglected to keep track of id as the source of truth, and shifted my attention to reading name, which was not the criterion I had initially set, and it pointed that out.

It also drew my attention towards other fixes, such as weak matches being passed on as proper matches. However, the changes it proposed felt like a reimagining of the pipeline, by introducing a new reason for an early return. Further, the strength of match was subjective. For example, "linen jersey sweat top" was perceived as a weak match to "mesh long-sleeve top", yet the example I drew from in my own wardrobe for that query was indeed a mesh long sleeve top that is marketed as a sweat top but isn't.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**


---

## Capstone

**What This Extends**

This extends FitFindr, my Unit 2 project: the three-tool agent that finds a secondhand listing, suggests outfits from a wardrobe, and writes a fit card. The agent loop and the tools are unchanged. What is new is the operational layer around `serve.py`: a structured request log (`requestlog.py`, written to `logs/requests.jsonl`), timing and token counts on every request, and a deployment on Render.

**The Shape**

Shape A, deploy and instrument. The extension is the run path, the logging, and the measurements that come out of it.

Out of scope: I am not changing the planning loop or the three tools, I am not touching query parsing or the search ranking, and I am not changing the prompts. I am also not adding new endpoints or a UI.

**Running It**

Path A, hosted on Render: https://ai201-project2-fitfindr-starter-v2026-i3qn.onrender.com

Start command: `gunicorn serve:app`. The `GEMINI_API_KEY` is set in Render's environment settings and is not in the repo. `AI201_CACHE=0` is set there too, so repeated queries are not served from the cache. `PYTHON_VERSION` is pinned to 3.13.14 (Render's default was 3.14.10, outside this repo's supported range), and `gunicorn.conf.py` sets the worker timeout to 120 seconds. The Render settings, the environment, and the clean-clone steps are in [RUNNING.md](RUNNING.md), section "Capstone: the deployed service".

**Instrumentation**

Every `/ask` request writes one JSON line to `logs/requests.jsonl` (and to stdout, which is what Render's log viewer shows). The writer is `requestlog.py::_append`, called from `serve.py::ask`. Fields:

- `timestamp`: UTC, to the millisecond
- `request_id`: short random id
- `input`: the query as received
- `output`: the fit card, or null if the run did not produce one
- `duration_ms`: whole request, measured with `time.perf_counter()`
- `status`: `ok`, `agent_error` (the agent stopped early, still HTTP 200), `crashed` (HTTP 500), or `rejected` (HTTP 400)
- `error`: the message when there is one
- `model_calls`, `prompt_tokens`, `output_tokens`: this request's own spend, taken as a before/after difference of `generate.py`'s counters inside the lock

Rejected requests (`requestlog.py::log_rejection`) keep the same `timestamp`, `request_id`, `input`, `output`, `duration_ms` and `status` fields, plus `event` and `reason`.

These ten entries are from a local run of `python serve.py` with `AI201_CACHE=0` (commit "add 10-run request log from local cost measurement (cache off)"):

```
{"timestamp": "2026-11-15T17:49:30.649+00:00", "request_id": "3fbd34ac", "input": "vintage graphic tee under $30", "output": "Found this insanely cute butterfly baby tee on depop for just $18, and it’s the ultimate piece for mixing soft and edgy styles. I paired it with wide-leg khaki trousers and combat boots for that perfect contrast between sweet and grungy. Safe to say this is going to be on heavy rotation all season!", "duration_ms": 4156.7, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 885, "output_tokens": 366}
{"timestamp": "2026-11-15T17:49:33.728+00:00", "request_id": "0c66af96", "input": "denim jacket under $50", "output": "Scored this cropped light wash vintage denim jacket on Poshmark for $42, and it immediately became my go-to streetwear layer. I love how the boxy cut balances out with baggy dark jeans and chunky sneakers for an easy, effortless vibe.", "duration_ms": 3048.7, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 906, "output_tokens": 387}
{"timestamp": "2026-11-15T17:49:36.488+00:00", "request_id": "0d745389", "input": "printed knit tank under $45", "output": "Obsessed with this chunky brown knit cardigan I just scored on depop for $35! I threw it on over baggy dark denim and combat boots for a cozy look with a little bit of grunge. Such a dreamy earth-toned staple for fall.", "duration_ms": 2729.3, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 861, "output_tokens": 334}
{"timestamp": "2026-11-15T17:49:40.037+00:00", "request_id": "a81966ff", "input": "linen jersey sweat top under $50", "output": "Finally scored this black mesh long-sleeve top on depop for just $15, and it is the ultimate grunge layering piece. I paired it with a white ribbed tank underneath, baggy dark wash jeans, and my trusty combat boots for that effortless goth streetwear vibe.", "duration_ms": 3521.7, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 927, "output_tokens": 401}
{"timestamp": "2026-11-15T17:49:44.289+00:00", "request_id": "3fabecf0", "input": "vintage graphic tee under $30", "output": "Scored this adorable butterfly baby tee for just $18.00 on depop and I am obsessed. I threw it on with some baggy dark wash denim, chunky sneakers, and my black crossbody for the ultimate 2000s streetwear look. It’s giving major off-duty Bratz doll vibes and I’m never taking it off.", "duration_ms": 4234.3, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 743, "output_tokens": 233}
{"timestamp": "2026-11-15T17:50:30.637+00:00", "request_id": "79991b64", "input": "corduroy jacket size L under $45", "output": "Scored this olive canvas shacket on Poshmark for just $33, and it’s the ultimate layering piece for my earth-tone phase. Been wearing it non-stop, whether I'm keeping it minimal with khaki trousers and chunky sneakers or throwing it over an oversized grey crewneck with combat boots for a grungier streetwear look.", "duration_ms": 46322.8, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 862, "output_tokens": 365}
{"timestamp": "2026-11-15T17:50:33.972+00:00", "request_id": "e92825a8", "input": "denim jacket under $50", "output": "Finally scored this cropped light wash denim jacket on Poshmark for $42 and I'm already obsessed with styling it. Threw it on over wide-leg khaki trousers and combat boots for the ultimate casual earth-tone vibe. Such a good find!", "duration_ms": 3307.9, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 865, "output_tokens": 347}
{"timestamp": "2026-11-15T17:50:36.743+00:00", "request_id": "8ff94a3c", "input": "printed knit tank under $45", "output": "Finally scored this chunky brown knit cardigan on Depop for $35 and I'm obsessed with how heavy and cozy it is. I threw it on over a white tank and baggy dark wash denim, finishing the look with my combat boots for a little bit of edge. It's giving the ultimate earthy streetwear vibe for chilly days.", "duration_ms": 2744.2, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 868, "output_tokens": 358}
{"timestamp": "2026-11-15T17:50:39.563+00:00", "request_id": "cdca6b67", "input": "vintage graphic tee under $30", "output": "I am so obsessed with this butterfly baby tee I just scored on depop for $18! I styled it with baggy dark wash jeans, a cropped zip hoodie, and chunky sneakers for the ultimate Y2K streetwear vibe.", "duration_ms": 2792.9, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 885, "output_tokens": 347}
{"timestamp": "2026-11-15T17:51:28.151+00:00", "request_id": "0c305717", "input": "linen jersey sweat top under $50", "output": "Score! Found this black mesh long-sleeve top on Depop for just $15, and it was so easy to layer over a white ribbed tank for that ultimate 90s grunge streetwear vibe. I'm obsessed with how it looks peeked out from under an oversized grey crewneck with baggy jeans, too.", "duration_ms": 48560.7, "status": "ok", "error": null, "model_calls": 4, "prompt_tokens": 906, "output_tokens": 392}
```

Two failed runs, from the same local server, triggered on purpose. The first is a rejected input (empty query, HTTP 400, `status: rejected`). The second is a query nothing matches (`status: agent_error`, HTTP 200: the agent stopped before `suggest_outfit` and the fit card). Both were appended to `logs/requests.jsonl` after the ten above.

```
{"timestamp": "2026-11-15T18:25:26.813+00:00", "request_id": "280c33b5", "input": "", "output": null, "duration_ms": 0.2, "status": "rejected", "event": "rejected", "reason": "empty or missing query"}
{"timestamp": "2026-11-15T18:25:43.168+00:00", "request_id": "1ea58db6", "input": "purple tuxedo under $2", "output": null, "duration_ms": 16333.1, "status": "agent_error", "error": "No listings matched your request. Try a different set of keywords, a different size, or a higher maximum price.", "model_calls": 1, "prompt_tokens": 109, "output_tokens": 9}
```

The no-match run took 16.3 seconds with a single model call, which is far slower than the 2.7 to 4.2 seconds a normal run takes. I have not diagnosed it yet.

**What It Costs**

Measured over the 10 runs above (local server, cache off, `gemini-3.5-flash-lite`):

| Measure | Mean | Min | Max |
|---|---|---|---|
| Duration | 12.1 s | 2.7 s | 48.6 s |
| Model calls | 3.1 | 3 | 4 |
| Prompt tokens | 871 | 743 | 927 |
| Output tokens | 353 | 233 | 401 |

How I measured it: ten requests in a row against the local server, using the token counters in `generate.py` read before and after each `run_agent()` call, so each log line holds that request's own numbers. Eight runs took 2.7 to 4.2 seconds; two took 46 and 49 seconds. I suspect `generate.py`'s per-minute pacing (15 requests a minute; ten runs is about 31 calls), but I have not confirmed it.

A hundred a day: 100 runs x 3.1 model calls = about 310 calls a day. In tokens that is 100 x 871 = 87,100 prompt tokens plus 100 x 353 = 35,300 output tokens, about 122,000 tokens a day, and in time it is 100 x 12.1 s = about 20 minutes of compute. I am reporting tokens and seconds, not dollars, because I measured those and did not take a price from a pricing page.

The binding limit is not cost but the free tier's quota. Gemini's own error messages state it: 15 requests a minute and 500 a day for this model. At about 3 calls a run that is roughly 5 runs a minute and 160 runs a day, so a hundred people a day (310 calls, 62% of the day's allowance) would fit, but my own testing did not: about 200 model calls of trials in one round used up what was left of the day, and the hosted service stopped answering (see What's Still Broken).


**Run Log and Verdicts**

This is the "before" set: the hosted trials rerun with `AI201_CACHE=0` actually set on Render (the first attempt ran with the cache on by mistake, see the note at the end of this section), plus the local trials for criteria 1 and 3. Every trial was sent by a harness that wrote one JSON record per request to `results/capstone_*.jsonl`; the hosted log lines come from Render's Logs tab, saved as `results/capstone_render_log_cacheoff.txt`. Criterion 2 is scored on the `duration_ms` field in that log, not on the client's clock.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves exactly one log line | 12 of 12 | 10/12 | 10/12 | 10/12 | MISSED |
| 2. Warm hosted requests under 5 s | 9 of 10 | 0/10 | 0/10 | 0/10 | MISSED |
| 3. A reader can start it from RUNNING.md alone | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. The recommendation still works | 9 of 10 | 9/10 | 8/10 | 8/10 | MISSED |
| 5. Concurrent pairs both finish, both logged | 4 of 5 pairs, 10 of 10 logged | 3/5 pairs, 8 of 10 logged | 4/5 pairs, 9 of 10 logged | 2/5 pairs, 8 of 10 logged | MISSED |

Real output, one trial each, with the file and function that produced it.

Criterion 1, `results/capstone_c1_trial1.jsonl` (written by my trial harness, counting lines in `logs/requests.jsonl`, which `requestlog.py::_append` writes; the 500s come from `serve.py::ask`):

```
valid    HTTP 200  log lines added: 1
empty    HTTP 400  log lines added: 1
valid    HTTP 200  log lines added: 1
array    HTTP 500  log lines added: 0
valid    HTTP 200  log lines added: 1
nomatch  HTTP 200  log lines added: 1
valid    HTTP 200  log lines added: 1
empty    HTTP 400  log lines added: 1
valid    HTTP 200  log lines added: 1
array    HTTP 500  log lines added: 0
valid    HTTP 200  log lines added: 1
nomatch  HTTP 200  log lines added: 1
```

Both array bodies (`[1,2]` and `["vintage tee"]`) returned HTTP 500 and added no log line in all three trials. Reproduced directly with Flask's test client:

```
AttributeError 'list' object has no attribute 'get' | at serve.py line 120 | query = (payload.get("query") or "").strip()
```

Criterion 2, from `results/capstone_render_log_cacheoff.txt`, first request of the run. The trace comes from `trace.py::step`, the record from `requestlog.py::_append`. Note the gap between step 1 and step 2:

```
2026-11-15T22:48:33.67834226Z [1] parse_request
2026-11-15T22:48:37.463610664Z [2] search_listings (via MCP)
2026-11-15T22:48:39.677346507Z {"timestamp": "2026-11-15T22:48:39.674+00:00", "request_id": "50d8b6bd", "input": "vintage graphic tee under $30", "output": "Scooped up this adorable butterfly baby tee for just $18 on Depop and I’m so obsessed. I paired it with baggy dark wash jeans and chunky sneakers for the ultimate Y2K streetwear edge.", "duration_ms": 16732.3, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 893, "output_tokens": 352}
2026-11-15T22:48:46.654837019Z {"timestamp": "2026-11-15T22:48:46.653+00:00", "request_id": "972e26cc", "input": "denim jacket under $50", "output": "Finally scored this cropped light wash denim jacket on Poshmark for $42 and I'm obsessed with the double denim look. Paired it with dark baggy jeans and chunky sneakers for the ultimate streetwear fit.", "duration_ms": 6850.9, "status": "ok", "error": null, "model_calls": 3, "prompt_tokens": 884, "output_tokens": 356}
```

The lowest `duration_ms` of any logged request in the cache-off run was 5972, so none was under 5000. Per trial, the C2/C4 requests that were logged had medians of 6851, 6957 and 6616 ms.

Criterion 3, `results/capstone_c3_trial1.jsonl` (the other two trials look the same, 12 to 14 s from clone to card):

```
clone 1: HTTP 200, fit_card present: True, clone-to-card 13.0 s
clone 2: HTTP 200, fit_card present: True, clone-to-card 13.7 s
clone 3: HTTP 200, fit_card present: True, clone-to-card 12.8 s
```

Criterion 4, `results/capstone_c2c4_trial2_cacheoff.jsonl`, one of the five failures:

```
request 1 (vintage graphic tee under $30): HTTP 500 after 31.02 s, fit_card present: False, body starts: <html>
```

Criterion 5, from `results/capstone_render_log_cacheoff.txt` (gunicorn and `generate.py`, not my code):

```
2026-11-15T22:49:37.403128387Z [2026-11-15 22:49:37 +0000] [58] [CRITICAL] WORKER TIMEOUT (pid:60)
2026-11-15T22:50:43.694630788Z google.genai.errors.ClientError: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://aistudio.google.com/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 15, model: gemini-3.5-flash-lite, description: Generate content requests per minute limit exceeded on Free Tier. See https://aistudio.google.com/docs/rate-limits.\nPlease retry in 47.116417906s.', 'status': 'R ...
2026-11-15T22:49:38.459418363Z [2026-11-15 22:49:38 +0000] [58] [ERROR] Worker (pid:60) was sent SIGKILL! Perhaps out of memory?
2026-11-15T22:49:37.458195843Z 127.0.0.1 - - [15/Nov/2026:22:49:37 +0000] "POST /ask HTTP/1.1" 500 0 "-" "-"
```

**Verdicts and diagnoses**

| # | Verdict | How I decided |
|---|---|---|
| 1 | MISSED | 10 of 12 each trial, against 12 of 12. The two misses are the same two array bodies every time. |
| 2 | MISSED | 0 of 10 each trial, against 9 of 10. Not close: the fastest logged request took 5.97 s. |
| 3 | MET | 3 of 3 clones each trial. The target held, but see What's Still Broken: it was loose. |
| 4 | MISSED | 9, 8 and 8 of 10, against 9 of 10. Runs 2 and 3 are below the target. |
| 5 | MISSED | 3, 4 and 2 pairs of 5, against 4 of 5, and the log half failed in every trial (8, 9 and 8 of 10 logged). |

Diagnosis, criterion 1. The stage is `serve.py::ask`. `request.get_json(silent=True) or {}` returns a list for a body like `[1,2]`, a list has no `.get`, and the `AttributeError` is raised on line 120, before any `requestlog` call is reached. Flask turns it into an HTML 500 and nothing is written. 30 of the 36 requests logged exactly once; the 6 that didn't are all array bodies.

Diagnosis, criterion 2. The stage is `search_listings (via MCP)`, called from `agent.py::run_agent` through `mcp_client.call_tool`. In every request the trace shows about 3.7 to 4.3 seconds between `parse_request` and `search_listings`: `call_tool` starts `mcp_server.py` as a new process each time, and on Render that start-up costs about four seconds. The two model calls that follow take about one to two seconds each, so even a request with no waiting takes six to seven seconds. My target of 5 seconds came from my local timings (2.7 to 4.2 s), and my reason assumed latency scaled with the number of model calls, not with starting a process. Several of the requests that took 14 to 25 seconds show `[rate limit] ... Waiting` lines in the same log, which is `generate.py`'s 15-calls-a-minute pacing.

Diagnosis, criteria 4 and 5. Same stage, same mechanism. With the cache off, a request makes about 3 model calls, and 10 requests in a row is about 30 calls, twice Gemini's free-tier limit of 15 a minute. `generate.py` waits (`[rate limit] ... Waiting 26s`) or, after a real `429`, backs off for 40 to 47 seconds. A request that waits that long runs past gunicorn's default 30 second worker timeout, gunicorn kills the worker (`WORKER TIMEOUT`, then `SIGKILL`), and the caller gets an HTML 500. There were 10 such kills in the cache-off run: 5 in the C2/C4 trials (the 5 misses in criterion 4) and 5 in the C5 trials.

The pattern. Criteria 4 and 5 are one problem with several symptoms: a request that takes longer than 30 seconds. Criterion 2 shares the rate-limit waits but its main cause is the MCP start-up. And criteria 1 and the log half of criterion 5 are the same defect seen twice: `requestlog.log_request` is called near the end of `ask()`, so anything that leaves `ask()` early (an exception before the call, or the worker being killed mid-request) leaves no record. In the cache-off run 50 of 60 requests were logged, which is exactly the 60 sent minus the 10 killed.

Note on the first set of hosted trials. I first ran them without `AI201_CACHE=0` actually set on Render (the variable was added afterwards). `suggest_outfit` was answered from the cache on repeated queries, so a request made about one model call instead of three and stayed under the rate limit. Those results (criterion 4 at 10 of 10 in all three trials, criterion 5 at 5 of 5 pairs in all three with 60 of 60 requests logged, criterion 2 at 2, 5 and 2 of 10 by `duration_ms`) are kept in `results/capstone_*_trial?.jsonl` and `results/capstone_render_log.txt`, and I don't count them because they don't match the conditions my criteria name.

**The Improvement**

What I changed: one new file, `gunicorn.conf.py`, containing `timeout = 120`, and one sentence in RUNNING.md saying so. Nothing else. The start command is still `gunicorn serve:app` with the default sync worker, because `mcp_client.call_tool` uses `asyncio.run()`.

Why: the diagnosis put criteria 4 and 5 (and the log half of 5) on gunicorn's 30 second worker timeout killing requests that were waiting out Gemini's per-minute limit. Ten requests were killed in the cache-off run, and each left no log line. Raising the timeout is aimed at exactly that. I considered three other changes and chose this one because it was the only one in scope that touched more than one criterion: stopping the per-request MCP start-up would fix criterion 2 but is a change to the agent and to my Unit 4 work, which I scoped out; handling non-object bodies fixes only criterion 1; and logging from a gunicorn worker-abort hook would record the kills without stopping them.

I redeployed on Render, confirmed the new deploy was live, and ran the hosted trials again with the same harness, three trials each, cache off. Criteria 1 and 3 were not rerun: the change does not touch either code path, and by the end of the run Gemini's daily quota was gone (see below), so I could not send the valid queries criterion 1 needs. The raw records are `results/capstone_*_improved.jsonl` and the Render log is `results/capstone_render_log_improved.txt`.

| Criterion | Target | Before (runs 1, 2, 3) | After (runs 1, 2, 3) | After, verdict |
|---|---|---|---|---|
| 2. Warm hosted requests under 5 s | 9 of 10 | 0, 0, 0 of 10 | 0, 0, 0 of 10 | MISSED |
| 4. The recommendation still works | 9 of 10 | 9, 8, 8 of 10 | 10, 10, 10 of 10 | MET |
| 5. Concurrent pairs both finish, both logged | 4 of 5 pairs | 3, 4, 2 pairs | 5, 1, 0 pairs (runs 2 and 3 affected by the quota, below) | MISSED |

Did it help? Yes for criterion 4, and not for the other two.

Criterion 4 went from missing to met: 30 of 30 requests returned a card and there were no worker timeouts during those trials. Criterion 2 did not change. Every logged request was still over 5 seconds (fastest 6.8 s), because the MCP start-up is untouched, and the median `duration_ms` per trial was 8058, 8458 and 8405 ms against 6851, 6957 and 6616 before. I have not isolated why it rose; requests that used to be killed now run to the end, and the rerun was the only one to use all three trials back to back.

Criterion 5 is the part I can't call. Trial 1 passed all 5 pairs with 10 of 10 requests logged. Then trial 2 and trial 3 collapsed, and the log shows why, and it is not the timeout change. At 00:11:59 UTC, partway through trial 2, Gemini started returning a different kind of 429, for the per-day limit:

```
2026-11-16T00:11:59.501170146Z ... Generate content requests per day limit exceeded on Free Tier. Please retry in 7h48m55.645027687s
```

All 15 `429` errors in that log are the per-day kind, counting down from 7h48m, and the 500 requests a day that the free tier allows had been used up by my own trials (about 200 model calls in this round, on top of the earlier ones). A request that hits a daily 429 retries five times at 65 seconds each, which is longer than the new 120 second timeout, so gunicorn killed it (`WORKER TIMEOUT`, 15 times, about two minutes apart, until 00:41). The requests my harness had already given up on were still queued, and each one tied up the single worker for two minutes in turn. So criterion 5's post-fix trials 2 and 3 are not a measure of the change: the quota ran out and I can't rerun them before the deadline, because the log's retry countdown ends at 08:00 UTC, which I take to be the midnight-Pacific reset. As recorded the criterion is MISSED, with 1 and 0 of 5 pairs in runs 2 and 3, and I am reporting it that way.

The trade. Raising the timeout fixed the requests that were being killed during ordinary rate-limit waits, and it did not make the service fail fast when the quota is gone: it turned a quick 500 into a two minute one per request. I also still have no record of the killed requests in the post-fix run; those requests are logged only as `POST /ask 500` access lines.

**What's Still Broken**

Criterion 1, missed. What I'd do: in `serve.py::ask`, check that the parsed body is a dict and treat anything else as the same rejected-input case as an empty query (a 400, written by `log_rejection`). It is a three line change. Why I stopped: I could make only one improvement, I chose the one aimed at three criteria, and I could not rerun the valid-query part of the suite after the quota ran out.

Criterion 2, missed. What I'd do: stop starting a new `mcp_server.py` process for every request, either by keeping one MCP session open for the life of the worker or by using the direct-call fallback `agent.py::_search` already has. Why I stopped: both change the agent and my Unit 4 MCP work, which I put out of scope on day one. I'd also change the target, which I set from local timings: measured on Render, a request takes 6 to 8 seconds even with no waiting, so "9 of 10 under 5 seconds" was a target the system could not hit.

Criterion 4 is met after the change, and only while requests stay under the free tier's rate. Without the change it missed for the reason in the diagnosis.

Criterion 5, missed. What I'd do first: make the service fail fast when Gemini says the quota is gone. If a `429` says to retry in more than about 30 seconds, and certainly if it is the per-day limit, return an error at once instead of sleeping and retrying five times. That is what turned a used-up daily quota into a 30 minute outage of the only worker, and it would also protect the per-minute case. I'd then rerun criterion 5 after the quota resets. Why I stopped: the change is in how `generate.py` backs off, which is starter code I haven't touched, and the quota can't be reset before the deadline.

Criterion 3 is met, but I set the target too low. The 30 minute limit was never close: a fresh clone took 12 to 14 seconds from clone to card on my machine. I'd tighten it to 5 minutes, and note that all of those clones ran on my own machine with Python 3.13, so it can't catch a problem that only appears on someone else's.

Two other things I should say. The hosted service will return "model unavailable" errors until Gemini's daily quota resets at midnight Pacific, so anyone who tries the URL tonight will see that. And my first set of hosted trials ran with the response cache on by mistake, which hid the rate limiter and made criteria 4 and 5 look perfect; running them again with `AI201_CACHE=0` is what showed the real problem.

If I had another unit, the first thing I'd do is the fail-fast change for quota errors, with a test that sends enough requests to trigger a `429` and checks that the service answers within a few seconds and logs the failure. Everything that went wrong in the hosted trials came back to that one gap: nothing in the service decides when to stop waiting.

**How I Used AI**

TODO (yours): two specific moments, each with what you asked, what you got, and what you changed.

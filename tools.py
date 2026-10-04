"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    query_words = _words(description)
    wanted_size = _words(size) if size else None

    scored = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue

        # Size matches on whole tokens, so "M" matches "S/M" and "M/L" but
        # never "XL" or "US 9"; "W30" matches "W30 L30".
        if wanted_size and not wanted_size <= _words(listing["size"]):
            continue

        searchable = _words(
            " ".join(
                [
                    listing["title"],
                    listing["description"],
                    listing["category"],
                    " ".join(listing["style_tags"]),
                    " ".join(listing["colors"]),
                    listing["brand"] or "",
                ]
            )
        )
        score = len(query_words & searchable)
        if score > 0:
            scored.append((score, listing))

    # sorted() is stable, so ties keep their order in the data.
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


def _words(text: str) -> set[str]:
    """Lowercase alphanumeric tokens ('S/M' -> {'s', 'm'}, 'US 8.5' -> {'us', '8.5'})."""
    return set(re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", text.lower()))


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    items = (wardrobe or {}).get("items") or []

    item_lines = (
        f"Title: {new_item['title']}\n"
        f"Category: {new_item['category']}\n"
        f"Colors: {', '.join(new_item['colors'])}\n"
        f"Style: {', '.join(new_item['style_tags'])}\n"
        f"Description: {new_item['description']}"
    )

    if not items:
        prompt = (
            "A thrifter is considering this secondhand item:\n\n"
            f"{item_lines}\n\n"
            "They haven't saved any wardrobe, so you don't know what they own. "
            "Suggest one or two outfits built around this item with general "
            "styling advice. Begin by saying these are general suggestions "
            "because no wardrobe has been saved. Do not invent pieces they "
            "own; describe the kinds of pieces that would pair well."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {w['name']} ({w['category']}; {', '.join(w['colors'])}; "
            f"{', '.join(w['style_tags'])})"
            + (f" — {w['notes']}" if w.get("notes") else "")
            for w in items
        )
        prompt = (
            "A thrifter is considering this secondhand item:\n\n"
            f"{item_lines}\n\n"
            f"Their wardrobe:\n{wardrobe_lines}\n\n"
            "Suggest one or two outfits that combine the new item with pieces "
            "from their wardrobe. Name the specific wardrobe pieces by name, "
            "and only use pieces from the list above."
        )

    outfit = generate(prompt).strip()
    if not outfit:
        return (
            "No outfit suggestion could be generated right now. "
            "Try again in a moment."
        )
    return outfit


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return (
            "No fit card was created because there is no outfit suggestion "
            "to write about. Get an outfit suggestion first, then try again."
        )

    prompt = (
        "Write a short social media caption for a thrift find, the way a real "
        "person would post it, not a product description.\n\n"
        f"Item: {new_item['title']}\n"
        f"Price: ${new_item['price']:.2f}\n"
        f"Platform: {new_item['platform']}\n"
        f"Style: {', '.join(new_item['style_tags'])}\n\n"
        f"Outfit it's styled in:\n{outfit}\n\n"
        "Rules:\n"
        "- Two to four sentences, no more.\n"
        "- Mention the item, its price, and the platform exactly once each.\n"
        "- The poster is the buyer who found it on that platform, not the seller.\n"
        "- Be specific about the vibe of the outfit.\n"
        "- Output only the caption, with no heading or options."
    )

    # cache=False: repeat runs on the same item should give fresh captions.
    caption = generate(prompt, cache=False).strip()
    if not caption:
        return "No fit card could be generated right now. Try again in a moment."
    return caption

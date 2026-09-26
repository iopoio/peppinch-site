# Embarkation Day Detail Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the 12 November embarkation card into a usable onboard sequence for lunch, room access, hot-tub or sauna use, and sail-away viewing.

**Architecture:** Keep the existing single-file itinerary data model and replace only the day-12 schedule, fallback text, options, and sources. Reuse the existing publishing and verification scripts without changing encryption or page layout.

**Tech Stack:** Static HTML, inline JavaScript data, Node.js publishing and verification scripts.

---

### Task 1: Update the day-12 itinerary data

**Files:**
- Modify: `/Users/hwa/Private/cruise-2026/itinerary.html`

- [ ] **Step 1: Record the current day-12 block**

Run: `rg -n "n:12|16:00 출항" /Users/hwa/Private/cruise-2026/itinerary.html`

Expected: the current short embarkation schedule is returned.

- [ ] **Step 2: Replace only the day-12 schedule**

Add timed entries for terminal arrival and boarding, muster-station confirmation, Grand Pacific lunch with alternatives, room readiness, hot tub and sauna or steam-room confirmation, room shower, and weather-based sail-away seating. Add options for the two viewing locations and official NCL facility links.

- [ ] **Step 3: Check required wording**

Run: `rg -n "Grand Pacific|O'Sheehan|핫텁|사우나|스팀룸|The Great Outdoors|Spinnaker|과일" /Users/hwa/Private/cruise-2026/itinerary.html`

Expected: every term appears in the day-12 content, with sauna or steam access marked for onboard confirmation.

### Task 2: Publish and verify

**Files:**
- Generated: `/Users/hwa/Projects/Automation/peppinch-site/travel/jade-voyage-7m4k9q2x/`

- [ ] **Step 1: Build the encrypted public files**

Run: `node /Users/hwa/Private/cruise-2026/publish.mjs`

Expected: the target travel directory is regenerated without an error.

- [ ] **Step 2: Run the itinerary verification**

Run a local static server for `/Users/hwa/Projects/Automation/peppinch-site`, then run `node /Users/hwa/Private/cruise-2026/verify.mjs http://127.0.0.1:8765/travel/jade-voyage-7m4k9q2x/`.

Expected: all existing assertions pass.

- [ ] **Step 3: Inspect the mobile page**

Open the local encrypted page with the saved fragment key at a 390-pixel viewport. Expand 12 November and confirm that the schedule is readable, links open, and no horizontal overflow appears.

- [ ] **Step 4: Check private information**

Search the generated files for traveler names, phone numbers, booking numbers, and actual booking payments.

Expected: no private value appears in the generated public files.

- [ ] **Step 5: Commit and push the scoped change**

Stage only the two planning documents and generated travel page files. Do not stage the unrelated modified blog files.


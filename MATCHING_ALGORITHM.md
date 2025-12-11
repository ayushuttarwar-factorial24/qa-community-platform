# Matching Algorithm Explanation

## Overview

The QA Community Platform v2 uses a **Give/Ask** matching system. The algorithm connects users based on how well one person's **GIVE** (what they can offer) matches another person's **ASK** (what they need), and vice versa.

## Core Concept

```
User A's GIVE ←→ User B's ASK  (How A can help B)
User A's ASK  ←→ User B's GIVE (How B can help A)
```

The match score is **bidirectional** - meaning we measure both how you can help them AND how they can help you.

---

## Matching Sections

The profile has 5 matching sections, each with equal weight (20%):

| Section | GIVE | ASK |
|---------|------|-----|
| Q1: Companies | Companies I can introduce to | Companies I want intro to |
| Q2: Professional | Help I can offer (resume, mock interviews, etc.) | Help I need |
| Q3: Technical | Areas I can train in | Areas I want to learn |
| Q4: Volunteering | Ways I can volunteer | Volunteering guidance I need |
| Q5: Jobs | Roles I'm hiring for | Roles I'm looking for |

---

## Score Calculation

### Step 1: Section Overlap Score

For each section, we calculate:

1. **give_to_ask**: How much of MY GIVE matches THEIR ASK
2. **ask_to_give**: How much of MY ASK matches THEIR GIVE

```
Section Score = (give_to_ask + ask_to_give) / 2
```

### Step 2: Overlap Formula

For checkboxes and custom items:

```
Overlap = |Intersection| / min(|Set1|, |Set2|)
```

Example:
- User A's GIVE technical areas: ["Selenium", "API Testing", "Performance Testing"]
- User B's ASK technical areas: ["Selenium", "API Testing", "Security Testing"]

Intersection = ["Selenium", "API Testing"] = 2 items
Min size = 3
Overlap = 2/3 = 0.67 (67%)

### Step 3: Company Matching

Companies use **partial matching** since people may write names differently:

```
"Google" matches "Google India"
"Microsoft" matches "Microsoft Corporation"
```

### Step 4: Final Score

```
Total Score = Σ (Section Score × 0.2) × 100

Where:
- Each section contributes 20% (0.2)
- Score is on a 0-100 scale
```

---

## Worked Example

### User A (The person looking for matches)

**GIVE:**
- Companies: ["Google", "Amazon"]
- Professional: ["Resume Review", "Mock Interviews"]
- Technical: ["Selenium", "API Testing"]
- Volunteering: ["Content Creation"]
- Jobs (Hiring): ["Automation Test Engineer"]

**ASK:**
- Companies: ["Microsoft"]
- Professional: ["Career Mentoring"]
- Technical: ["Performance Testing", "Security Testing"]
- Volunteering: ["Event Coordination"]
- Jobs (Looking): ["Test Lead"]

---

### User B (A potential match)

**GIVE:**
- Companies: ["Microsoft India", "TCS"]
- Professional: ["Career Mentoring", "Project Guidance"]
- Technical: ["Performance Testing", "JMeter"]
- Volunteering: ["Event Coordination", "Speaker Support"]
- Jobs (Hiring): ["Test Lead", "QA Manager"]

**ASK:**
- Companies: ["Google", "Facebook"]
- Professional: ["Resume Review"]
- Technical: ["Selenium", "Playwright"]
- Volunteering: ["Content Creation", "Social Media"]
- Jobs (Looking): ["Automation Test Engineer"]

---

### Score Calculation

#### Q1: Companies
- A's GIVE → B's ASK: "Google" matches "Google" ✓ → 1/2 = 0.5
- A's ASK → B's GIVE: "Microsoft" matches "Microsoft India" ✓ → 1/1 = 1.0
- **Section Score: (0.5 + 1.0) / 2 = 0.75**

#### Q2: Professional
- A's GIVE → B's ASK: "Resume Review" matches ✓ → 1/1 = 1.0
- A's ASK → B's GIVE: "Career Mentoring" matches ✓ → 1/1 = 1.0
- **Section Score: (1.0 + 1.0) / 2 = 1.0**

#### Q3: Technical
- A's GIVE → B's ASK: "Selenium" matches ✓ → 1/2 = 0.5
- A's ASK → B's GIVE: "Performance Testing" matches ✓ → 1/2 = 0.5
- **Section Score: (0.5 + 0.5) / 2 = 0.5**

#### Q4: Volunteering
- A's GIVE → B's ASK: "Content Creation" matches ✓ → 1/2 = 0.5
- A's ASK → B's GIVE: "Event Coordination" matches ✓ → 1/1 = 1.0
- **Section Score: (0.5 + 1.0) / 2 = 0.75**

#### Q5: Jobs
- A's GIVE (Hiring) → B's ASK (Looking): "Automation Test Engineer" matches ✓ → 1/1 = 1.0
- A's ASK (Looking) → B's GIVE (Hiring): "Test Lead" matches ✓ → 1/2 = 0.5
- **Section Score: (1.0 + 0.5) / 2 = 0.75**

---

### Final Score

```
Total = (0.75 + 1.0 + 0.5 + 0.75 + 0.75) × 0.2 × 100
      = 3.75 × 0.2 × 100
      = 75%
```

**Match Score: 75%** 🎯

---

### Match Reasons Generated

Based on the calculation, the system generates these reasons:

1. ✅ "You can introduce them to companies they want" (Q1: Google)
2. ✅ "They can introduce you to companies you want" (Q1: Microsoft)
3. ✅ "You can help with their professional activities" (Q2: Resume Review)
4. ✅ "They can help with your professional activities" (Q2: Career Mentoring)
5. ✅ "You can train them in technical areas" (Q3: Selenium)
6. ✅ "They can train you in technical areas" (Q3: Performance Testing)
7. ✅ "You have job openings matching their search" (Q5: Automation Engineer)
8. ✅ "They have job openings matching your search" (Q5: Test Lead)

---

## Why This Algorithm Works

### 1. **Mutual Benefit**
The bidirectional scoring ensures both parties benefit. A high score means BOTH users can help each other.

### 2. **Equal Weights**
All sections are equally important (20% each). This prevents gaming the system by filling only one section.

### 3. **Partial Matching**
Company name matching allows for variations (e.g., "Google" = "Google India").

### 4. **Custom Inputs**
Users can add custom items beyond checkboxes, and these are included in matching.

### 5. **No Self-Matching**
Users are excluded from their own match results.

### 6. **Connection Exclusion**
Already connected profiles are excluded from suggestions.

---

## Score Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| 80-100% | Excellent match - high mutual benefit |
| 60-79% | Good match - multiple areas of overlap |
| 40-59% | Moderate match - some common interests |
| 20-39% | Weak match - limited overlap |
| 0-19% | Poor match - minimal compatibility |

---

## Technical Implementation

The matching algorithm is implemented in:

```
ui/services/matching.py
```

Key functions:
- `calculate_match_score(source, candidate)` - Main scoring function
- `get_top_matches(source, all_profiles, limit)` - Returns top N matches
- `calculate_list_overlap(list1, list2)` - Overlap calculation
- `calculate_company_similarity(give, ask)` - Company name matching

---

## Future Improvements (Not Implemented)

1. **Weighted Sections**: Allow users to prioritize certain sections
2. **Text Similarity**: Use NLP for open text field matching
3. **Activity Scoring**: Boost active users in rankings
4. **Geographic Matching**: Consider location proximity
5. **Network Effects**: Recommend friends-of-friends

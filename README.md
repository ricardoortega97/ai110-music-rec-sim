# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

  **Response:**  

  There are four sections that explain how major platforms have further designed their music recommendation for users. They applied collaborative filtering, where it recommends music that similar users enjoy. The metadata received from the songs assists with content-based recommendations for songs with similar characteristics. These are both used together to adjust the weight factors in cross-reference. With new technology, deep learning and neural networks were used to train. I think what I would use is contextual signals, where it relies on the specific context such as the time of day and user behavior.

  **Changes:**

  The recommendation uses the user's taste profile in the point-weight scoring system where each song is judged against the user's preferences and filtered based on the past feedback. When the feedback from each play happens, it will update the session state, allowing it to feed the next recommendations. 

  **Algorithm Recipe:**  
  Filter — Before scoring anything, rule out songs the user has already rejected (disqualified) or recently skipped (still in cooldown).

  Score — Every eligible song gets a score built from three signals: does the genre match (+2.0), does the mood match (+1.0), and how close is the song's sonic feel to the user's preference in energy, tempo, valence, and acousticness (+0 to +1.5). A previous skip shaves off -0.5.

  Rank — Sort all scored songs highest to lowest and return the top K.

  Play — The user listens. If they play it through, nothing changes.

  Feedback — If they skip, the song is penalized and put on a 25-song cooldown before it can return. A second skip or an "off" signal disqualifies it entirely. That feedback updates the session state and the cycle repeats from step 1.

  **Potential Biases:**

  - Since the profile only has limited options for the preferences, there could be more skew distance calculations against songs. Adding valence or acousticness could reduce it and improve recommendations.
  - Static profile during the session until the user shifts the context. If the user is listening to a genre but wants to slowly shift, it will not happen. 


  **Data Flow Draft**
  
  Inputs(User Profile, songs, session_state) ->  
  Eligibility Filter(ea. song in catalog: disqualify = drop music, queue less than cooldown = drop in cooldown, pass both = eligible ) ->  
  Process(Scoring Loop for the user's preference of each song in the csv file) ->  
  Ranking(sort song and score by descending -> slice Top K) ->  
  Output( list of songs = Top K results ) ->  
  Feedback Signals(play through = no change, skipped = first strike, 2nd strike will disqualify the song)

  **Mermaid Data Flow**
  ```mermaid
flowchart TD
    UP["User Profile\n(genre, mood, energy, tempo)"]
    SC["Song Catalog\n(songs.csv)"]
    SS["Session State\n(skip_count, disqualified, cooldown_until, queue_position)"]

    EF{"Eligibility Filter"}
    DROP["Drop Song"]

    SL["Scoring Loop\nscore_song(user, song)"]
    G["+2.0 Genre Match"]
    M["+1.0 Mood Match"]
    V["+0.0 → +1.5 Vibe Closeness\n(energy, tempo, valence, acousticness)"]
    SK["-0.5 if skip_count == 1"]

    RK["Ranking\nSort by score → Top K"]
    OUT["Output\n(song, score, explanation) × K"]

    FB{"Feedback Signal"}
    PLAYED["No Change"]
    SKIP1["1st Strike\nskip_count += 1\ncooldown_until = queue_pos + 25"]
    SKIP2["2nd Strike\ndisqualified = True"]
    OFF["Disqualified = True\n(immediate)"]

    UP --> EF
    SC --> EF
    SS --> EF

    EF -- "disqualified or in cooldown" --> DROP
    EF -- "eligible" --> SL

    SL --> G & M & V & SK --> RK
    RK --> OUT
    OUT --> FB

    FB -- "played through" --> PLAYED
    FB -- "skipped (1st)" --> SKIP1
    FB -- "skipped (2nd)" --> SKIP2
    FB -- "off" --> OFF

    SKIP1 --> SS
    SKIP2 --> SS
    OFF --> SS
    SS --> EF
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"


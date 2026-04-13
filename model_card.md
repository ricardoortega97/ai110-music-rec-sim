# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **moodcatcher 1.0**  

---

## 2. Intended Use  

This recommender is a classroom simulation that generates a ranked list of songs based on a user's stated genre, mood, and energy preferences. It assumes the user can describe their taste through those three labels and that those labels map directly onto songs in the catalog. It is not intended for production use — the goal is to explore how scoring weights and catalog design affect what gets recommended.

---

## 3. How the Model Works  


Each song is scored by comparing it against the user's preferences across three things: whether the genre matches (+1 point), whether the mood matches (+1 point), and how close the song's energy level is to the user's target (up to +1.5 points, where energy is weighted twice as heavily as other audio features). The three components are added together, and the top five songs by total score are returned as the recommendation. Genre was originally worth +2 points but was reduced to +1 during experimentation to give energy a stronger influence on the final ranking.

---

## 4. Data  

There are a total of 20 songs in the songs.csv file from relaxing music to help with studying to cleaning the house to intense such as pushing your limits at the gym while being hyped. I did noticed that the song added shifted more to a lower energy that prevents other intense preference to stay in the shift. It lacks of mood of the user's ideal time or feeling. Planning to add ten more with more flexibility and range. 

---

## 5. Strengths  

Where does your system seem to work well  

The system does work well with making sure it will keep the range of the user's preference based on the temp_bpm and energy such as the user wants to listen to lofi, the system will keep it from shifting afar and recommend music closely match to the vibe. 

---

## 6. Limitations and Bias 


### Categorical Blind Spot Creates a Hidden Filter Bubble

The system awards up to 50% to %60 range of the maximum possible score (2.0 out of 3.5) through genre and mood label matches alone. Users that preferred genres ended up being absent from the catalog, receiving zero signal and ranked entirely by energy proximity. During the testing for a trap profile with angry mood, it ended up routed to dreampop and lofi songs, they are far off from the requested preference. The cluster near the energy midpoint was 0.4 to 0.58 in the dataset, so it will imply a no warning or fall back. May return a confident list that looks 'reasonable' but reflects from the dataset structure rather than user's preference. Looking into the dataset, most of them only appear once while others have another song that will strongly match it. 

A future mitigation would be to detect when categorical scores are uniformly zero and either flag the result as low-confidence or broaden the candidate pool before ranking.

---

## 7. Evaluation  


Five user profiles were tested: three standard profiles (Late-Night Studier: lofi/chill/0.3, Gym Grinder: rock/intense/0.9, Sunday Morning: jazz/relaxed/0.4) and two adversarial profiles designed to stress the scoring logic (Ghost Listener: trap/angry/0.5, Mismatch Maximizer: kpop/chill/0.97). For each run, I looked at which genres appeared in the top 5, what scores were assigned, and whether the explanation column reflected the user's actual stated preferences.

The most surprising result came from Sunday Morning: Coffee Shop Stories scored 3.46 as a near-perfect match, but positions 2 through 5 were all pure vibe matches with no genre or mood signal — because jazz has only one song in the catalog. The recommender filled the remaining slots with lofi songs that happened to have similar energy, which would feel completely off to a real jazz listener. The catalog depth problem became visible immediately.

The Ghost Listener result confirmed the filter bubble finding from Section 6: every top-5 result was a calm, indie-adjacent song (dreampop, lofi, citypop) with scores clustered tightly between 1.35 and 1.44. There was no indication that the user asked for trap or angry — the output looked confident and normal. Running Mismatch Maximizer (kpop/chill, energy 0.97) surfaced a different issue: lofi/chill songs ranked #2 and #3 despite having energy of 0.42, because the mood match bonus (+1.0) outweighed their vibe penalty. Iron Pulse, which had a perfect energy match (vibe 1.50/1.50), was beaten by softer songs simply because it shared no mood label with the user.

---

## 8. Future Work  

- [ ] Adding the recommend features to implement of different scoring modes. 
- [ ] Adding 10 to 20 more songs to test case 
- [ ] Visual chart how each song is at within the user's preferences.
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Learning how to build a system that involves with weighting a score base on user preference along with real consequences if we shift the weight of the score. The tradeoffs between how much it was applied depended on the audio's features and there is no 'correct' output as each algorithm results differently. The dataset did play a huge part with shifting the genre if there were some that had multiple songs in the set, causing it to shift the top k no matter how it was well-tuned. 

The most unexpected discovery was how the Ghost Listener profile — a genre and mood that did not exist in the catalog — returned a confident, normal-looking top-5 list of calm indie songs with no warning at all. I expected the output to look obviously wrong, but it looked reasonable, which is exactly what makes that kind of bias hard to catch in a real system.

This changed how I think about apps like Spotify or Apple Music: when they show me a confident "You might like this" list, I now wonder how much of it reflects my actual taste versus the shape of their catalog and the weight of whichever label matched first. A recommendation that looks good is not the same as a recommendation that is right. Also, I think Spotify can and could improve the algorithm of their "smart shuffle" but decides not too... 

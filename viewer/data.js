window.SIMULATION_DATA = {
  "meta": {
    "timestamp": "2026-04-01T01:24:36",
    "model": "claude-sonnet-4-20250514",
    "scenario": "bar_night"
  },
  "target": {
    "id": "T",
    "name": "Vera",
    "gender": "female",
    "role": "target",
    "archetype": "Curator",
    "big5": {
      "openness": 85,
      "conscientiousness": 78,
      "extraversion": 70,
      "agreeableness": 62,
      "neuroticism": 42
    },
    "attachment": "secure",
    "traits": {
      "kindness": 68,
      "intelligence": 88,
      "attractiveness": 82,
      "status": 75,
      "humor": 72,
      "stability": 80
    },
    "strategy": "long-term",
    "bio": "Gallery director who curates contemporary art shows and rarely gives second chances. Values depth over performance. Can spot a rehearsed line from across the bar. Looking for someone who surprises her, not someone who tries to.",
    "color": "#E8607A"
  },
  "suitors": [
    {
      "id": "S1",
      "name": "Marcus",
      "gender": "male",
      "role": "suitor",
      "archetype": "Architect",
      "big5": {
        "openness": 72,
        "conscientiousness": 82,
        "extraversion": 65,
        "agreeableness": 75,
        "neuroticism": 28
      },
      "attachment": "secure",
      "traits": {
        "kindness": 80,
        "intelligence": 82,
        "attractiveness": 75,
        "status": 78,
        "humor": 68,
        "stability": 88
      },
      "strategy": "long-term",
      "bio": "Structural engineer who designs public spaces. Unhurried and self-contained. Asks one precise question per conversation rather than filling silence with noise. Comfortable with pauses in a way most people aren't.",
      "color": "#5B9BD5"
    },
    {
      "id": "S2",
      "name": "Theo",
      "gender": "male",
      "role": "suitor",
      "archetype": "Performer",
      "big5": {
        "openness": 78,
        "conscientiousness": 48,
        "extraversion": 92,
        "agreeableness": 70,
        "neuroticism": 78
      },
      "attachment": "anxious-preoccupied",
      "traits": {
        "kindness": 75,
        "intelligence": 65,
        "attractiveness": 88,
        "status": 55,
        "humor": 90,
        "stability": 35
      },
      "strategy": "short-term",
      "bio": "Stand-up comic who uses laughter as both weapon and shield. Brilliant for ten minutes, exhausting by eleven. His need to be liked radiates off him like heat. Has never met a silence he didn't immediately try to fill.",
      "color": "#E8A838"
    },
    {
      "id": "S3",
      "name": "Elliot",
      "gender": "male",
      "role": "suitor",
      "archetype": "Analyst",
      "big5": {
        "openness": 90,
        "conscientiousness": 75,
        "extraversion": 32,
        "agreeableness": 42,
        "neuroticism": 35
      },
      "attachment": "dismissive-avoidant",
      "traits": {
        "kindness": 50,
        "intelligence": 95,
        "attractiveness": 62,
        "status": 88,
        "humor": 45,
        "stability": 72
      },
      "strategy": "long-term",
      "bio": "Quantitative researcher at a hedge fund. Treats every conversation as a data problem to be solved. Emotionally self-sufficient to the point of appearing cold. Finds most people intellectually uninteresting, which he does not bother to hide.",
      "color": "#7B68C8"
    },
    {
      "id": "S4",
      "name": "Rafael",
      "gender": "male",
      "role": "suitor",
      "archetype": "Romantic",
      "big5": {
        "openness": 82,
        "conscientiousness": 52,
        "extraversion": 74,
        "agreeableness": 82,
        "neuroticism": 72
      },
      "attachment": "anxious-preoccupied",
      "traits": {
        "kindness": 90,
        "intelligence": 68,
        "attractiveness": 80,
        "status": 58,
        "humor": 74,
        "stability": 38
      },
      "strategy": "long-term",
      "bio": "Pastry chef who falls in love with ideas and people too quickly. Genuinely warm but reads emotional subtext into neutral statements. Has been told he comes on too strong. Means every word he says, which is part of the problem.",
      "color": "#4BAE8A"
    },
    {
      "id": "S5",
      "name": "Dex",
      "gender": "male",
      "role": "suitor",
      "archetype": "Drifter",
      "big5": {
        "openness": 88,
        "conscientiousness": 38,
        "extraversion": 60,
        "agreeableness": 58,
        "neuroticism": 68
      },
      "attachment": "fearful-avoidant",
      "traits": {
        "kindness": 65,
        "intelligence": 75,
        "attractiveness": 85,
        "status": 48,
        "humor": 80,
        "stability": 30
      },
      "strategy": "short-term",
      "bio": "Travel writer perpetually between apartments and relationships. Magnetic in the first five minutes. Prone to saying something genuinely vulnerable then immediately deflecting with a joke. Sabotages things that start to matter.",
      "color": "#E07B54"
    }
  ],
  "encounters": [
    {
      "suitor": {
        "id": "S1",
        "name": "Marcus",
        "gender": "male",
        "role": "suitor",
        "archetype": "Architect",
        "big5": {
          "openness": 72,
          "conscientiousness": 82,
          "extraversion": 65,
          "agreeableness": 75,
          "neuroticism": 28
        },
        "attachment": "secure",
        "traits": {
          "kindness": 80,
          "intelligence": 82,
          "attractiveness": 75,
          "status": 78,
          "humor": 68,
          "stability": 88
        },
        "strategy": "long-term",
        "bio": "Structural engineer who designs public spaces. Unhurried and self-contained. Asks one precise question per conversation rather than filling silence with noise. Comfortable with pauses in a way most people aren't.",
        "color": "#5B9BD5"
      },
      "conversation": [
        {
          "speaker": "Marcus",
          "text": "*settles into chair, taking a moment to actually look at you before speaking*\n\nI noticed you watching how people enter the room earlier - do you curate conversations the same way you curate exhibitions?\n\n*slight pause, genuinely curious about the answer*",
          "analysis": {
            "label": "Strategic observation opening",
            "detail": "Marcus's Openness (72) drives his perceptive observation about Vera's behavior patterns, while his Conscientiousness (82) structures this into a thoughtful, work-relevant question. His secure attachment enables him to take time for genuine assessment rather than rushing into superficial topics.",
            "theory": "Per Hazan & Shaver (1987), secure attachment facilitates comfortable exploration of partner characteristics without anxiety-driven rushing or avoidant superficiality."
          }
        },
        {
          "speaker": "Vera",
          "text": "*raises eyebrow with genuine intrigue*\n\nThat's... surprisingly perceptive. Most people lead with what I do, not how I think. *leans forward slightly* I suppose I do - I'm always looking for the unexpected detail that reveals something deeper, whether it's in a piece or a person.\n\n*studies him with renewed interest* So what did you notice about how I was watching?",
          "analysis": {
            "label": "Secure intellectual mirroring",
            "detail": "Vera's high Openness (85) drives her appreciation for Marcus's perceptiveness, while her secure attachment enables her to reciprocate his observational depth without defensiveness. Her moderate Agreeableness (62) allows direct engagement without excessive accommodation, and her low Neuroticism (42) supports confident vulnerability in revealing her curatorial mindset.",
            "theory": "Per Hazan & Shaver (1987), secure attachment facilitates reciprocal self-disclosure and genuine interest in partner perspectives, creating positive relationship spirals through mutual understanding."
          }
        },
        {
          "speaker": "Marcus",
          "text": "*meets her gaze steadily, a slight smile forming*\n\nYou were cataloguing - not just looking at people, but filing away details like you would with an artwork. The way someone holds their drink, their posture when they think no one's watching. *pauses briefly* I'm curious what you've catalogued about me so far.",
          "analysis": {
            "label": "Secure directness",
            "detail": "Marcus's low neuroticism (28) and secure attachment enable him to directly address potentially vulnerable territory without defensiveness. His high conscientiousness (82) drives the methodical observation of Vera's behavior, while his moderate extraversion (65) allows comfortable eye contact and personal inquiry without overwhelm.",
            "theory": "Per Hazan & Shaver (1987), secure attachment facilitates open communication and comfort with interdependence, enabling direct engagement with potentially sensitive topics without fear of rejection."
          }
        }
      ],
      "fatigue_at_start": 0.0
    },
    {
      "suitor": {
        "id": "S2",
        "name": "Theo",
        "gender": "male",
        "role": "suitor",
        "archetype": "Performer",
        "big5": {
          "openness": 78,
          "conscientiousness": 48,
          "extraversion": 92,
          "agreeableness": 70,
          "neuroticism": 78
        },
        "attachment": "anxious-preoccupied",
        "traits": {
          "kindness": 75,
          "intelligence": 65,
          "attractiveness": 88,
          "status": 55,
          "humor": 90,
          "stability": 35
        },
        "strategy": "short-term",
        "bio": "Stand-up comic who uses laughter as both weapon and shield. Brilliant for ten minutes, exhausting by eleven. His need to be liked radiates off him like heat. Has never met a silence he didn't immediately try to fill.",
        "color": "#E8A838"
      },
      "conversation": [
        {
          "speaker": "Theo",
          "text": "*fidgets with his drink coaster, then looks up with a slightly nervous grin*\n\nOkay, so I was going to open with a joke about how this whole speed dating thing is like performance art - you know, artificial constraints, forced interactions, everyone pretending it's not totally weird - but then I realized you probably hear that exact comparison at least twice a week. *laughs and runs hand through hair* So instead I'm just gonna ask: what's the weirdest thing someone's ever said about one of your exhibits?",
          "analysis": {
            "label": "Self-conscious meta-commentary",
            "detail": "Theo's high Neuroticism (78) and anxious-preoccupied attachment drive his need to acknowledge the artificial nature of the interaction while simultaneously seeking validation. His Extraversion (92) pushes him to perform, but his anxiety manifests as nervous fidgeting and preemptive explanation of his conversational choices before pivoting to engage Vera's professional identity.",
            "theory": "Per Mikulincer & Shaver (2007), anxious attachment leads to hypervigilance about social evaluation, creating self-referential commentary to manage impression formation while maintaining connection-seeking behaviors."
          }
        },
        {
          "speaker": "Vera",
          "text": "*leans back slightly, genuinely intrigued by the self-awareness*\n\nActually, that's the first time someone's made that connection tonight - and you're not wrong, there's definitely a performative element to all this. *swirls wine thoughtfully* The weirdest comment... someone once told me that a piece about urban isolation made them \"feel claustrophobic in a good way,\" which honestly became my favorite review ever. What made you pivot away from the joke - second thoughts about the material, or reading the room?",
          "analysis": {
            "label": "Intellectual boundary-testing",
            "detail": "Vera's high Openness (85) and secure attachment drive her to probe Theo's meta-cognitive awareness about his own performance anxiety. Her follow-up question about his pivot tests whether he can engage in genuine self-reflection rather than deflection, revealing her long-term mating strategy's emphasis on authenticity over surface charm.",
            "theory": "Per Hazan & Shaver (1987), secure attachment enables comfortable exploration of a partner's internal world without fear of abandonment or engulfment."
          }
        },
        {
          "speaker": "Theo",
          "text": "*fidgets with his collar, clearly pleased by the engagement*\n\nOh wow, you actually listened! Most people just wait for their turn to talk. *grins nervously* Honestly? I was reading you - saw that little spark when I mentioned the performative thing and thought maybe there was something real there worth exploring instead of just... *gestures vaguely* ...throwing punchlines at the wall until something sticks. Plus \"claustrophobic in a good way\" is such a perfect description of intimacy, isn't it?",
          "analysis": {
            "label": "Anxious validation-seeking disclosure",
            "detail": "Theo's N78 and anxious-preoccupied attachment drive his immediate expression of surprise and gratitude at being listened to, followed by nervous admission of strategic behavioral reading. His E92 fuels the rapid, stream-of-consciousness sharing while his high neuroticism creates the fidgeting and nervous grin as he seeks reassurance that his authenticity is valued.",
            "theory": "Per Mikulincer & Shaver (2007), anxious attachment hyperactivates proximity-seeking behaviors, including excessive self-disclosure and vigilant monitoring of partner responsiveness to maintain connection."
          }
        }
      ],
      "fatigue_at_start": 0.25
    },
    {
      "suitor": {
        "id": "S3",
        "name": "Elliot",
        "gender": "male",
        "role": "suitor",
        "archetype": "Analyst",
        "big5": {
          "openness": 90,
          "conscientiousness": 75,
          "extraversion": 32,
          "agreeableness": 42,
          "neuroticism": 35
        },
        "attachment": "dismissive-avoidant",
        "traits": {
          "kindness": 50,
          "intelligence": 95,
          "attractiveness": 62,
          "status": 88,
          "humor": 45,
          "stability": 72
        },
        "strategy": "long-term",
        "bio": "Quantitative researcher at a hedge fund. Treats every conversation as a data problem to be solved. Emotionally self-sufficient to the point of appearing cold. Finds most people intellectually uninteresting, which he does not bother to hide.",
        "color": "#7B68C8"
      },
      "conversation": [
        {
          "speaker": "Elliot",
          "text": "*glances up from checking phone* \n\nYou know, I've been analyzing the conversation patterns at these events for the past hour, and approximately 73% of opening lines involve career questions or weather commentary. *slight pause* So instead, I'm curious - when you're looking at a piece that everyone else dismisses as pretentious nonsense, what data points tell you they're wrong?",
          "analysis": {
            "label": "Intellectual gatekeeping display",
            "detail": "Elliot's high Openness (90) drives his need to demonstrate intellectual superiority, while his dismissive-avoidant attachment creates emotional distance through analytical framing. His moderate Agreeableness (42) allows him to subtly devalue others' conventional approaches while positioning himself as uniquely perceptive.",
            "theory": "Per Hazan & Shaver (1987), dismissive-avoidant individuals maintain distance through intellectual superiority displays, converting emotional vulnerability into cognitive challenges."
          }
        },
        {
          "speaker": "Vera",
          "text": "*raises an eyebrow, genuinely intrigued*\n\nWell, that's refreshingly direct. *leans forward slightly* It's never really data points - it's more like watching someone's pupils dilate when they think no one's looking, or the way they unconsciously mirror the piece's rhythm with their breathing. *pauses, studying him* The body reveals what the mind won't admit, even in a gallery full of people performing their sophistication.",
          "analysis": {
            "label": "Intimate behavioral observation",
            "detail": "Vera's high Openness (85) and secure attachment drive her to share deeply personal observational insights about human behavior, revealing intimate awareness of physiological responses and unconscious behaviors. Her moderate Agreeableness (62) allows her to be direct about people's performative nature without excessive concern for social pleasantries.",
            "theory": "Per Hazan & Shaver (1987), secure attachment enables comfortable emotional intimacy and self-disclosure, while high Openness facilitates complex psychological observations and willingness to share unconventional insights."
          }
        },
        {
          "speaker": "Elliot",
          "text": "*straightens slightly, processing this unexpected depth*\n\nHm. Most people think they're unreadable when they're actually broadcasting at full volume. *brief pause, genuinely curious* But you're talking about involuntary physiological responses to aesthetic stimuli - that's essentially measuring emotional volatility in real-time. *tilts head* Do you find that your professional eye for human authenticity makes personal connections more... complicated?\n\n*studies her with renewed interest*",
          "analysis": {
            "label": "Intellectualized vulnerability testing",
            "detail": "Elliot's dismissive-avoidant attachment and low Extraversion (32) drive him to probe for emotional depth while maintaining analytical distance. His high Openness (90) enables sophisticated reframing of personal topics into intellectual discourse, allowing connection without threatening his autonomy. The genuine curiosity signals potential interest despite his typical avoidant patterns.",
            "theory": "Per Mikulincer & Shaver (2007), dismissive-avoidant individuals use intellectualization as a secondary attachment strategy to explore intimacy while preserving emotional distance and self-reliance."
          }
        }
      ],
      "fatigue_at_start": 0.5
    },
    {
      "suitor": {
        "id": "S4",
        "name": "Rafael",
        "gender": "male",
        "role": "suitor",
        "archetype": "Romantic",
        "big5": {
          "openness": 82,
          "conscientiousness": 52,
          "extraversion": 74,
          "agreeableness": 82,
          "neuroticism": 72
        },
        "attachment": "anxious-preoccupied",
        "traits": {
          "kindness": 90,
          "intelligence": 68,
          "attractiveness": 80,
          "status": 58,
          "humor": 74,
          "stability": 38
        },
        "strategy": "long-term",
        "bio": "Pastry chef who falls in love with ideas and people too quickly. Genuinely warm but reads emotional subtext into neutral statements. Has been told he comes on too strong. Means every word he says, which is part of the problem.",
        "color": "#4BAE8A"
      },
      "conversation": [
        {
          "speaker": "Rafael",
          "text": "*leans forward with genuine curiosity, eyes lighting up*\n\nYou know, I was just thinking - curating art and making pastries are probably more similar than people realize! We both have to know when something's perfectly balanced versus when it's trying too hard to impress. *pauses, looking slightly uncertain* Sorry, that might sound like a line, but I genuinely just thought of that when I saw you.",
          "analysis": {
            "label": "Anxious authenticity signaling",
            "detail": "Rafael's N72 and anxious-preoccupied attachment drive him to immediately qualify his genuine insight with self-deprecating doubt ('Sorry, that might sound like a line'). His high A82 produces the authentic connection attempt, but his attachment anxiety compels preemptive damage control to avoid potential rejection.",
            "theory": "Per Mikulincer & Shaver (2007), anxious attachment hyperactivates proximity-seeking behaviors while simultaneously fearing negative evaluation, creating this self-sabotaging pattern of authentic engagement followed by anxious qualification."
          }
        },
        {
          "speaker": "Vera",
          "text": "*straightens slightly, a flicker of genuine interest cutting through the evening's fatigue*\n\nActually, that's... not terrible. Most people either ask if I \"paint too\" or launch into how they \"don't get modern art.\" *takes a sip of her drink* But you're right about the balance thing - overworked pieces scream desperation, whether it's a canvas or a croissant.\n\n*tilts head, studying him* So what happens when your perfectly balanced pastry meets someone who insists on adding extra frosting anyway?",
          "analysis": {
            "label": "Defensive vulnerability testing",
            "detail": "Vera's Agreeableness of 62 and secure attachment create controlled openness, while her high Openness (85) drives intellectual engagement. She reveals fatigue and frustration with shallow interactions, then immediately tests Rafael's reaction to client criticism\u2014probing whether he can handle relationship challenges without defensiveness.",
            "theory": "Per Hazan & Shaver (1987), secure attachment enables balanced self-disclosure that tests partner reliability while maintaining emotional regulation."
          }
        },
        {
          "speaker": "Rafael",
          "text": "*eyes light up with unexpected delight*\n\nOh wow, you actually understand! *leans forward eagerly* Most people would just say \"give the customer what they want,\" but you get that it's about... integrity, right? *gestures animatedly* When someone drowns my work in extra sweetness, it's like they're saying the original vision wasn't enough.\n\n*pauses, suddenly looking vulnerable* I probably care too much about that stuff - my ex used to say I took everything too personally. *searches her face* But isn't there something beautiful about trusting the artist's intent? Whether it's your curation or my ganache?",
          "analysis": {
            "label": "Anxious validation-seeking disclosure",
            "detail": "Rafael's anxious-preoccupied attachment (N72, A82) drives him to immediately share vulnerable personal information about his ex's criticism after receiving validation. His high agreeableness makes him hyper-attuned to Vera's approval, leading to premature emotional disclosure as a proximity-seeking behavior despite the relationship risk.",
            "theory": "Per Mikulincer & Shaver (2007), anxious attachment hyperactivates proximity-seeking, manifesting as excessive self-disclosure to test partner responsiveness and secure emotional connection."
          }
        }
      ],
      "fatigue_at_start": 0.75
    },
    {
      "suitor": {
        "id": "S5",
        "name": "Dex",
        "gender": "male",
        "role": "suitor",
        "archetype": "Drifter",
        "big5": {
          "openness": 88,
          "conscientiousness": 38,
          "extraversion": 60,
          "agreeableness": 58,
          "neuroticism": 68
        },
        "attachment": "fearful-avoidant",
        "traits": {
          "kindness": 65,
          "intelligence": 75,
          "attractiveness": 85,
          "status": 48,
          "humor": 80,
          "stability": 30
        },
        "strategy": "short-term",
        "bio": "Travel writer perpetually between apartments and relationships. Magnetic in the first five minutes. Prone to saying something genuinely vulnerable then immediately deflecting with a joke. Sabotages things that start to matter.",
        "color": "#E07B54"
      },
      "conversation": [
        {
          "speaker": "Dex",
          "text": "*glances at the timer, then back with a slightly crooked smile*\n\nSo, I'm guessing you've heard every \"I'd love to curate a night with you\" line in the book, right? *fidgets with coffee cup* I was actually going to ask if you ever get tired of people trying to be the most interesting piece in your collection, but then I realized I just did that exact thing.",
          "analysis": {
            "label": "Self-sabotaging meta-awareness",
            "detail": "Dex's fearful-avoidant attachment and high Neuroticism (68) create a classic approach-avoidance conflict. His moderate Extraversion (60) enables initial engagement, but his attachment style triggers self-protective behaviors that undermine connection potential. The meta-commentary serves as preemptive damage control against expected rejection.",
            "theory": "Per Mikulincer & Shaver (2007), fearful-avoidant individuals simultaneously desire and fear intimacy, leading to self-defeating behaviors that maintain distance while appearing to seek connection."
          }
        },
        {
          "speaker": "Vera",
          "text": "*pauses mid-sip, genuinely surprised by the self-awareness*\n\nYou know what? That's the first time tonight someone's caught themselves in the act. *sets glass down with interest* Most people double down when they realize they're performing.\n\n*leans forward slightly* So now I'm curious - what were you actually going to say before your brain went into art-pickup-line mode?",
          "analysis": {
            "label": "Secure vulnerability invitation",
            "detail": "Vera's secure attachment and high Openness (O85) enable her to appreciate Dex's self-awareness without judgment, while her moderate Agreeableness (A62) allows her to call out performative behavior directly. Her secure base provides the confidence to lean into vulnerability by asking what he really wanted to say, creating psychological safety for authentic connection.",
            "theory": "Per Hazan & Shaver (1987), secure attachment facilitates comfortable intimacy and trust, manifesting as the ability to encourage authentic self-disclosure in others without fear of rejection or engulfment."
          }
        },
        {
          "speaker": "Dex",
          "text": "*laughs and runs hand through hair, looking genuinely caught*\n\nI was going to ask if you ever feel like you're living behind glass too - always arranging beautiful things for other people to look at but never... *catches myself getting too real, deflects with a grin* \n\nSee? There I go again, turning a perfectly good conversation into some deep metaphor about emotional distance. *takes a sip* Maybe we should stick to whether you prefer Rothko or Pollock - safer territory.",
          "analysis": {
            "label": "Fearful-avoidant self-sabotage",
            "detail": "With fearful-avoidant attachment and Neuroticism at 68, Dex begins authentic vulnerability then immediately retreats with deflection and self-deprecation. His high Openness (88) drives the initial deep metaphor, but his attachment system triggers withdrawal when intimacy threatens, creating the classic approach-avoidance conflict.",
            "theory": "Per Mikulincer & Shaver (2007), fearful-avoidant individuals simultaneously crave and fear intimacy, leading to self-sabotaging behaviors that maintain emotional distance while expressing underlying connection needs."
          }
        }
      ],
      "fatigue_at_start": 1.0
    }
  ],
  "rankings": [
    {
      "rank": 1,
      "name": "Marcus",
      "reaction": "He sees how I think rather than just what I do, and that kind of perceptive observation suggests real depth beneath the surface.",
      "is_rejection": false
    },
    {
      "rank": 2,
      "name": "Elliot",
      "reaction": "His analytical approach could be insufferable, but he actually engaged with my ideas about human authenticity in a way that felt genuinely curious rather than performative.",
      "is_rejection": false
    },
    {
      "rank": 3,
      "name": "Dex",
      "reaction": "The self-awareness is refreshing, and that glimpse of vulnerability about living behind glass hit closer to home than I expected.",
      "is_rejection": false
    },
    {
      "rank": 4,
      "name": "Rafael",
      "reaction": "His passion for craft mirrors mine, but the neediness about his ex and requiring validation for his artistic vision feels emotionally exhausting.",
      "is_rejection": false
    },
    {
      "rank": 5,
      "name": "Theo",
      "reaction": "Sweet and self-aware, but the nervous energy and tendency to overthink his own performance suggests he'd constantly need reassurance I don't have patience to give.",
      "is_rejection": false
    }
  ],
  "chosen": {
    "id": "S1",
    "name": "Marcus",
    "gender": "male",
    "role": "suitor",
    "archetype": "Architect",
    "big5": {
      "openness": 72,
      "conscientiousness": 82,
      "extraversion": 65,
      "agreeableness": 75,
      "neuroticism": 28
    },
    "attachment": "secure",
    "traits": {
      "kindness": 80,
      "intelligence": 82,
      "attractiveness": 75,
      "status": 78,
      "humor": 68,
      "stability": 88
    },
    "strategy": "long-term",
    "bio": "Structural engineer who designs public spaces. Unhurried and self-contained. Asks one precise question per conversation rather than filling silence with noise. Comfortable with pauses in a way most people aren't.",
    "color": "#5B9BD5"
  },
  "compatibility": {
    "big5_similarity": 0.988,
    "trait_similarity": 0.996,
    "attachment_compat": 0.95,
    "strategy_match": 1.0,
    "overall": 0.979
  },
  "svr": {
    "stimulus": 0.72,
    "value": 0.988,
    "role": 0.994,
    "svr_total": 0.909
  },
  "gottman": {
    "four_horsemen": {
      "criticism": 0.143,
      "contempt": 0.145,
      "defensiveness": 0.402,
      "stonewalling": 0.08
    },
    "positive_negative_ratio": 4.33,
    "stability_score": 83.4,
    "prediction": "Likely stable"
  },
  "evaluation": "**PSYCHOLOGICAL EVALUATION:**\n\nThis pairing works exceptionally well through **assortative mating principles** - their near-identical Big Five profiles (99% similarity) create a rare foundation of shared cognitive processing and values, while both secure attachment styles enable effective emotional regulation and conflict resolution (Gottman's research shows secure pairs maintain positive interaction ratios naturally). Their conversation demonstrates **synchronized depth-seeking behavior** - Marcus's perceptive opening question and Vera's authentic response show they're operating on the same intellectual wavelength without performance anxiety.\n\nThe biggest risk factor is **similarity-induced stagnation** - when partners are this psychologically similar, they may lack the complementary differences that drive growth and maintain novelty over time (while assortative mating predicts stability, extreme similarity can create relationship staleness). Their predicted conflict pattern would be **intellectual withdrawal** - both being highly conscientious and emotionally stable, they'd likely avoid direct confrontation but might gradually drift into parallel lives when facing major decisions, with neither pushing for resolution due to their shared conflict-avoidant tendencies.\n\nHowever, their matching long-term strategies, secure attachment, and demonstrated mutual fascination with depth over surface create a strong foundation for **earned security reinforcement** - each partner's emotional availability will strengthen the other's already-secure base.\n\n**Verdict: Likely stable** - the extreme compatibility outweighs the stagnation risk, particularly given their shared appreciation for subtlety and depth."
};

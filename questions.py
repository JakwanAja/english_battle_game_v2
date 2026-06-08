"""
questions.py — Bank soal untuk English Battle Pets 2 Player
"""

ALL_QUESTIONS_POOL = [
    # ── TENSES ──
    {"q": "Past tense of 'go'?",
     "opts": ["A. goed", "B. went", "C. gone", "D. going"], "ans": 1,
     "exp": "'Went' is the irregular past tense of 'go'."},

    {"q": "Past tense of 'eat'?",
     "opts": ["A. eated", "B. eaten", "C. ate", "D. eating"], "ans": 2,
     "exp": "'Ate' is the simple past tense of 'eat'."},

    {"q": "Past tense of 'run'?",
     "opts": ["A. runned", "B. ran", "C. run", "D. running"], "ans": 1,
     "exp": "'Ran' is the irregular past tense of 'run'."},

    {"q": "Past tense of 'see'?",
     "opts": ["A. seed", "B. seen", "C. saw", "D. seeing"], "ans": 2,
     "exp": "'Saw' is the simple past tense of 'see'."},

    {"q": "Past tense of 'write'?",
     "opts": ["A. writed", "B. written", "C. writing", "D. wrote"], "ans": 3,
     "exp": "'Wrote' is the simple past; 'written' is past participle."},

    {"q": "Past tense of 'buy'?",
     "opts": ["A. buyed", "B. buy", "C. bought", "D. buyed"], "ans": 2,
     "exp": "'Bought' is the irregular past tense of 'buy'."},

    {"q": "Past tense of 'come'?",
     "opts": ["A. comed", "B. came", "C. come", "D. coming"], "ans": 1,
     "exp": "'Came' is the irregular past tense of 'come'."},

    {"q": "Past tense of 'take'?",
     "opts": ["A. taked", "B. taken", "C. took", "D. taking"], "ans": 2,
     "exp": "'Took' is the simple past tense of 'take'."},

    {"q": "Past tense of 'give'?",
     "opts": ["A. gived", "B. gave", "C. given", "D. giving"], "ans": 1,
     "exp": "'Gave' is the irregular past tense of 'give'."},

    {"q": "Past tense of 'know'?",
     "opts": ["A. knowed", "B. known", "C. knew", "D. knowing"], "ans": 2,
     "exp": "'Knew' is the simple past tense of 'know'."},

    # ── PLURALS ──
    {"q": "Plural of 'wolf'?",
     "opts": ["A. wolfes", "B. wolfs", "C. wolves", "D. wolven"], "ans": 2,
     "exp": "When a word ends in -f or -fe, change to -ves."},

    {"q": "Plural of 'leaf'?",
     "opts": ["A. leafs", "B. leaves", "C. leafes", "D. leafves"], "ans": 1,
     "exp": "'Leaf' ends in -f, so plural is 'leaves'."},

    {"q": "Plural of 'child'?",
     "opts": ["A. childs", "B. childes", "C. childrens", "D. children"], "ans": 3,
     "exp": "'Children' is the irregular plural of 'child'."},

    {"q": "Plural of 'mouse'?",
     "opts": ["A. mouses", "B. mice", "C. mices", "D. mouse"], "ans": 1,
     "exp": "'Mice' is the irregular plural of 'mouse'."},

    {"q": "Plural of 'tooth'?",
     "opts": ["A. tooths", "B. teeths", "C. teeth", "D. toothes"], "ans": 2,
     "exp": "'Teeth' is the irregular plural of 'tooth'."},

    {"q": "Plural of 'box'?",
     "opts": ["A. boxs", "B. boxies", "C. boxes", "D. boxen"], "ans": 2,
     "exp": "Words ending in -x add -es in plural."},

    {"q": "Plural of 'city'?",
     "opts": ["A. citys", "B. cities", "C. cityes", "D. city"], "ans": 1,
     "exp": "When -y follows a consonant, change -y to -ies."},

    {"q": "Plural of 'foot'?",
     "opts": ["A. foots", "B. feets", "C. feet", "D. footies"], "ans": 2,
     "exp": "'Feet' is the irregular plural of 'foot'."},

    # ── PARTS OF SPEECH ──
    {"q": "Which word is an adjective?",
     "opts": ["A. quickly", "B. run", "C. beautiful", "D. happiness"], "ans": 2,
     "exp": "'Beautiful' describes a noun, making it an adjective."},

    {"q": "Which word is an adverb?",
     "opts": ["A. happy", "B. slowly", "C. table", "D. eat"], "ans": 1,
     "exp": "'Slowly' modifies a verb, making it an adverb."},

    {"q": "Which word is a noun?",
     "opts": ["A. jump", "B. angry", "C. freedom", "D. silently"], "ans": 2,
     "exp": "'Freedom' names a concept, making it an abstract noun."},

    {"q": "Which word is a verb?",
     "opts": ["A. book", "B. warm", "C. destroy", "D. golden"], "ans": 2,
     "exp": "'Destroy' expresses an action, making it a verb."},

    {"q": "Which word is a preposition?",
     "opts": ["A. quickly", "B. between", "C. happy", "D. run"], "ans": 1,
     "exp": "'Between' shows a spatial relationship between things."},

    {"q": "Which is a conjunction?",
     "opts": ["A. because", "B. table", "C. blue", "D. walk"], "ans": 0,
     "exp": "'Because' connects clauses, making it a conjunction."},

    # ── VOCABULARY / OPPOSITES ──
    {"q": "Opposite of 'ancient'?",
     "opts": ["A. old", "B. modern", "C. historical", "D. antique"], "ans": 1,
     "exp": "'Modern' means new or current, opposite of ancient."},

    {"q": "Opposite of 'brave'?",
     "opts": ["A. bold", "B. strong", "C. cowardly", "D. weak"], "ans": 2,
     "exp": "'Cowardly' means lacking courage, opposite of brave."},

    {"q": "Opposite of 'generous'?",
     "opts": ["A. kind", "B. selfish", "C. wealthy", "D. humble"], "ans": 1,
     "exp": "'Selfish' means only caring about oneself."},

    {"q": "Synonym of 'happy'?",
     "opts": ["A. sad", "B. angry", "C. joyful", "D. tired"], "ans": 2,
     "exp": "'Joyful' means feeling great happiness — a synonym."},

    {"q": "Synonym of 'big'?",
     "opts": ["A. tiny", "B. enormous", "C. slim", "D. short"], "ans": 1,
     "exp": "'Enormous' means very large — a synonym of 'big'."},

    {"q": "Opposite of 'victory'?",
     "opts": ["A. win", "B. champion", "C. defeat", "D. success"], "ans": 2,
     "exp": "'Defeat' means losing, opposite of victory."},

    # ── GRAMMAR / FILL-IN ──
    {"q": "I ___ to school every day.",
     "opts": ["A. goes", "B. go", "C. going", "D. gone"], "ans": 1,
     "exp": "First person singular 'I' uses the base verb form."},

    {"q": "She ___ her homework last night.",
     "opts": ["A. finish", "B. finishing", "C. finishes", "D. finished"], "ans": 3,
     "exp": "Past tense is used for completed actions."},

    {"q": "They ___ playing football now.",
     "opts": ["A. is", "B. was", "C. are", "D. were"], "ans": 2,
     "exp": "Present continuous with 'they' uses 'are'."},

    {"q": "He ___ a doctor when he grows up.",
     "opts": ["A. will be", "B. is", "C. was", "D. were"], "ans": 0,
     "exp": "Future intention uses 'will be'."},

    {"q": "We ___ to the cinema yesterday.",
     "opts": ["A. go", "B. goes", "C. gone", "D. went"], "ans": 3,
     "exp": "'Yesterday' signals past tense; 'went' is correct."},

    {"q": "There ___ many students in the class.",
     "opts": ["A. is", "B. was", "C. are", "D. am"], "ans": 2,
     "exp": "'Many students' is plural, so 'are' is correct."},

    {"q": "I have ___ this movie before.",
     "opts": ["A. see", "B. saw", "C. seen", "D. seeing"], "ans": 2,
     "exp": "Present perfect uses past participle: 'seen'."},

    # ── SENTENCE STRUCTURE ──
    {"q": "Which sentence is correct?",
     "opts": ["A. She don't like cats.", "B. She doesn't like cats.", "C. She not like cats.", "D. She didn't likes cats."], "ans": 1,
     "exp": "Third person singular uses 'doesn't' in negative."},

    {"q": "Which sentence is correct?",
     "opts": ["A. He have a car.", "B. He has a car.", "C. He having a car.", "D. He haves a car."], "ans": 1,
     "exp": "Third person singular uses 'has', not 'have'."},

    {"q": "Which question is correct?",
     "opts": ["A. Where you going?", "B. Where are you going?", "C. Where you are going?", "D. Where going you?"], "ans": 1,
     "exp": "Question form: auxiliary verb before subject."},

    {"q": "Which sentence uses 'their' correctly?",
     "opts": ["A. Their going home.", "B. I like their house.", "C. Their over there.", "D. Can you their?"], "ans": 1,
     "exp": "'Their' is a possessive pronoun — it shows ownership."},

    # ── IDIOMS & EXPRESSIONS ──
    {"q": "\"Break a leg\" means:",
     "opts": ["A. Get injured", "B. Good luck", "C. Run fast", "D. Stop working"], "ans": 1,
     "exp": "'Break a leg' is an idiom meaning good luck, especially in performance."},

    {"q": "\"It's raining cats and dogs\" means:",
     "opts": ["A. Animals are falling", "B. It's very windy", "C. It's raining heavily", "D. Pets are outside"], "ans": 2,
     "exp": "This idiom means it's raining very hard."},

    {"q": "\"Hit the books\" means:",
     "opts": ["A. Throw books away", "B. Study hard", "C. Buy new books", "D. Go to library"], "ans": 1,
     "exp": "'Hit the books' is an idiom meaning to study."},

    {"q": "\"Bite the bullet\" means:",
     "opts": ["A. Eat metal", "B. Shoot a gun", "C. Endure something painful", "D. Run away"], "ans": 2,
     "exp": "This idiom means to endure a painful situation bravely."},

    # ── SPELLING ──
    {"q": "Which spelling is correct?",
     "opts": ["A. recieve", "B. receive", "C. receve", "D. receeve"], "ans": 1,
     "exp": "Remember: 'i before e, except after c' — receive."},

    {"q": "Which spelling is correct?",
     "opts": ["A. occured", "B. occurred", "C. ocurred", "D. occurrd"], "ans": 1,
     "exp": "Double the 'r' when adding -ed: occurred."},

    {"q": "Which spelling is correct?",
     "opts": ["A. beleive", "B. beleeve", "C. believe", "D. belive"], "ans": 2,
     "exp": "The correct spelling is b-e-l-i-e-v-e."},

    {"q": "Which spelling is correct?",
     "opts": ["A. definately", "B. definitly", "C. definitely", "D. definitley"], "ans": 2,
     "exp": "The correct spelling is d-e-f-i-n-i-t-e-l-y."},

    # ── ARTICLES ──
    {"q": "Fill in: ___ elephant is a large animal.",
     "opts": ["A. A", "B. An", "C. The", "D. Some"], "ans": 1,
     "exp": "Use 'An' before words starting with a vowel sound."},

    {"q": "Fill in: She plays ___ piano.",
     "opts": ["A. a", "B. an", "C. the", "D. —"], "ans": 2,
     "exp": "Use 'the' with musical instruments."},

    {"q": "Fill in: He is ___ honest man.",
     "opts": ["A. a", "B. an", "C. the", "D. some"], "ans": 1,
     "exp": "'Honest' starts with a vowel sound /ɒ/, so use 'an'."},
]

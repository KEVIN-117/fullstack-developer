## **Product Refinement and Evolution**

The startup team had survived their launch. Drowning in support email and facing a cash-flow crunch, they had built an AI support agent on a prayer and an API key. After a rocky start, they created a knowledge base and utilized a prompt template to provide the LLM with context, which ultimately made it useful.

A month later, that solution was handling over half their support requests. They were even successfully using an LLM to battle back against social media trolls. Its automated sentiment analysis flawlessly identified negative posts and generated near-perfect responses. They still needed a human in the loop, but that interaction took only seconds.

They had made incredible progress on a shoestring budget, but as they gained more customers, their first-pass AI solutions were already hitting a wall. The growth meant more feature requests, and their existing AI solutions needed to evolve. Product strategy meetings kept circling back to the same question: “Can your platform make better product recommendations so we can boost sales?”

Their current keyword-based recommendations weren’t enough. The model could match products by titles and even handle synonyms, but it still missed obvious connections when the wording was completely different. Customers weren’t seeing related products they would likely want, and the team knew they were leaving money on the table.

They had seen how well recommendation systems could work. Amazon, Netflix, and Spotify all offer spot-on recommendations. Sometimes those companies’ customers didn’t even know they wanted something until it showed up and they ended up buying it.

The difference? These big tech platforms were using vector databases powered by special pretrained AI models that understand text, images, and even audio in a way that’s closer to the way humans think about meaning. If the team could figure out how to load and query a vector database, they could move beyond simple keyword matches and start delivering recommendations that actually felt intelligent.

It was also clear that the AI support agent needed an upgrade. In a live chat, sluggish responses felt like an eternity, and as the team signed more clients, usage costs were climbing fast. On top of that, they couldn’t keep adding new knowledge base articles to the prompt without hitting the context window limit.

The problem boiled down to the context size they were cramming into every prompt. Including _all_ the knowledge base articles every time was wasteful and inefficient. They had pushed prompt engineering as far as it could take them. The next step was context engineering.

They needed a smarter way to target _only_ specific articles that could answer a user’s question. This was exactly how many companies were already using vector databases: breaking documents into smaller chunks, loading them into the database, and then searching for just the pieces that mattered. Only the retrieved text would be sent along with the prompt. No wasted space, no irrelevant content.

The approach had a name: retrieval-augmented generation (RAG). And it sounded like the perfect solution.
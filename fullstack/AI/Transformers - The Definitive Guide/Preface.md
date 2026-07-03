When I first started working with transformers in 2019, I was immediately drawn to them. Two years later, I built my own deep learning architecture based on attention, and that same year I taught my first university lecture on vision transformers. What struck me then, and continues to do so today, is just how versatile this architecture really is. Once you understand how transformers work, patterns begin to emerge. You start to see how the same principles apply across images, video, audio, and beyond. The deeper insight is not found in treating each domain as a separate problem, as is often the case in deep learning, but in recognizing how naturally the transformer architecture extends across domains.

As it turns out, it doesn’t matter whether you’re modeling discrete tokens, image patches, or spectrogram frames. The core logic remains the same. You may change the axis of representation, but the underlying architecture stays intact. That’s the elegance of transformers, at least to me, and the reason I decided to write this book: to share my passion for transformers and let you discover that elegance at your own pace.

What also continues to fascinate me is what happens when transformers are used as part of a larger system. Their real power shows up when you combine multiple models into an agent that can reason, act, and iterate on a task. Beyond simply connecting models, my recent focus has been on pairing transformers with test-time compute and reinforcement learning. Together, these ideas make it possible to build systems that adapt, improve, and learn from their own behavior. That’s what led me to focus my PhD research on self-improving AI agents.

As you read through this book, you’ll follow both the development of transformers across diﬀerent domains and my own path working with them, up to my most recent work on building AI agents. Along the way, I’ll share how I personally think about these models—the mental models I use to reason about architectures, trade-oﬀs, and system behavior and how those models shape the design decisions I make in practice. My goal isn’t just to show you what works but to help you see why it works.

By the end of the book, my hope is that you arrive at the same place I did: seeing transformers not as isolated models but as building blocks inside larger systems. Transformers aren’t just another architecture. They’re a framework for abstraction. That’s why they aren’t a passing trend but a shift in how we generalize and connect modeling across domains. Arthur C. Clarke once said:

> Any sufficiently advanced technology is indistinguishable from magic.

I hope, as you read through the book, that it gives you the tools to turn the “magic” of attention into a reliable, engineered reality.

# What This Book Is About

This book is a practical systems guide for building intelligent transformer-powered applications across modalities, written by someone who has designed, debugged, and deployed these architectures in real products.

You’ll start with first principles: tokenization, embeddings, attention, encoder and decoder design, and modern architectural enhancements for long-context reasoning. From there, the book expands across domains, showing how the same core transformer abstraction applies to time series forecasting, computer vision, image and video generation, audio understanding, reinforcement learning, and reasoning-driven coding systems.

Rather than treating each modality in isolation, the chapters build on shared structure: how tokens become patches, frames, or spectrogram slices; how attention adapts across domains; and how architectural choices propagate into performance, stability, and cost.

Later chapters move into reinforcement learning, test-time compute, reasoning models, and AI agents, connecting transformers with world models, planning algorithms, and multi-agent architectures. The goal is to help you understand how transformers evolve from standalone predictors into components of adaptive systems.

Beyond individual models, this book focuses on systems-level thinking. You’ll learn how transformers behave when deployed in production, how to optimize inference and training pipelines, how to manage memory and compute, and how to integrate models into agentic workflows that can plan, reflect, and improve over time.

Throughout the book, theory is paired with concrete implementations, production considerations, and design trade-oﬀs drawn directly from real deployments.

# What This Book Is Not

This is not an introductory deep learning book or an introduction to large language models. I assume you already understand neural networks, backpropagation, basic machine learning workflows, and large language models. While core concepts are explained, the focus is on how transformers operate across domains and in practice.

This is also not a prompt engineering guide or a collection of model or API recipes. Although modern foundation models appear throughout the book, the emphasis is on understanding fundamentals. Model names are ephemeral. Instead, this book teaches the abstraction behind multimodal systems. My goal is to give you a kind of grand unified theory for transformers that remains relevant regardless of which model happens to be state of the art. Along the way, it focuses on training dynamics, optimization, and deployment, not on crafting prompts or consuming hosted endpoints.

This book is also not an academic exercise. While I include math where it’s needed, I ensure not to overindulge. You’ll see equations and architectural details throughout the book; they’re always paired with practical engineering explanations. If you’re looking for exhaustive theoretical proofs or benchmark-only discussions, this book takes a diﬀerent, more applied approach.

# Who This Book Is For

This book is tailored for intermediate to advanced machine learning (ML) engineers, data scientists, and AI architects who are ready to look beyond language models. It’s for those who find themselves at the intersection of research and engineering: people who need to understand the why of an architecture to solve the how of a production problem.

Specifically, I wrote this for:

- The architect who needs to design systems that handle data beyond just text, such as video and image generation, image and audio classification, or time-series forecasting
    
- The engineer tasked with moving a model from a local notebook into a high-performance production environment and handling the production “gotchas,” such as spiking memory usage while optimizing key-value (KV) cache in decoder-only models
    
- The systems thinker interested in how individual transformers can be coordinated into AI agents that learn from their own test-time experience
    

Throughout these chapters, I don’t shy away from the complexity and math that a technical book demands. However, I am a firm believer that technical complexity should always serve a practical purpose and be accompanied with clear coding examples. I share production insights: hard-won lessons I’ve gathered from building attention-based architectures and deploying them in the wild, so you don’t have to. These are the nuances that research papers often leave out but that make the diﬀerence between a model that works in a demo and one that survives in production.

# Navigating This Book

The book is organized to move from foundations to increasingly complex systems.

[Chapter 1, “From First Principles to State-of-the-Art Transformers”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch01.html#chapter_1), establishes transformer fundamentals, including tokenization, embeddings, attention, encoder and decoder architectures, and modern enhancements for long-context modeling.

[Chapter 2, “Transformers for Time Series”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch02.html#chapter_2), applies transformers to time series, covering domain-specific challenges such as stationarity and autocorrelation, and introduces foundation models for forecasting and anomaly detection.

[Chapter 3, “Transformers for Vision Tasks”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch03.html#chapter_3), focuses on vision tasks, including classification and segmentation, with practical examples using modern vision transformers.

[Chapter 4, “Transformers for Image Generation”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch04.html#chapter_4), and [Chapter 5, “Transformers for Video Generation”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch05.html#chapter_5), move into generative modeling for images and video, exploring diﬀusion transformers and latent representations for scalable generation.

[Chapter 6, “From Sound to Token and Back: Transformers in the Audio Domain”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch06.html#chapter_6), covers audio, from waveform fundamentals to speech, multimodal audio models, and music generation.

[Chapter 7, “Reinforcement Learning Transformers”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch07.html#chapter_7), introduces reinforcement learning with transformers, including decision transformers and world models.

[Chapter 8, “Embracing the Era of Experience: Transformers for Planning, Reasoning, and Coding”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch08.html#chapter_8), shifts toward reasoning and coding, examining how transformers learn to plan, reason, and solve open-ended problems using reinforcement learning and test-time compute.

[Chapter 9, “From Scripts to Thinking: AI Agents for Complex Tasks”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch09.html#chapter_9), builds on this by introducing AI agents, multi-agent architectures, memory systems, and human-in-the-loop workflows.

[Chapter 10, “Smarter, Better, Faster, Stronger: Optimizing LLMs and AI Agents”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch10.html#chapter_10), focuses on optimization, including reinforcement learning for agents, adaptive compute, and systems-level training strategies.

[Chapter 11, “Deploying Transformer Models”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch11.html#chapter_11), addresses deployment: runtime engineering, quantization, evaluation, security, and cost-aware production design.

[Chapter 12, “Where to Go Next: From Models to Intelligent Systems”](https://learning.oreilly.com/library/view/transformers-the-definitive/9781098167004/ch12.html#chapter_12), looks forward, integrating models into intelligent systems and discussing how agentic architectures scale.

Each chapter is largely self-contained, so you can read selectively depending on your interests. However, the material builds conceptually, and reading sequentially provides the strongest mental model.

Now it’s your turn. From first principles and multimodal foundations to reinforcement learning, agentic systems, optimization, and deployment, the system is yours to design. Transformers are tools, and the chapters ahead are built around one goal: reliability beyond the demo stage.

The difference between a model that impresses in a notebook and one that survives in production lies in the details, in architectural choices, memory constraints, training dynamics, evaluation strategy, and system design. This book gives you those details. What you build next is where your own journey with transformers begins.

# Conventions Used in This Book

The following typographical conventions are used in this book:

_Italic_

Indicates new terms, URLs, email addresses, filenames, and file extensions.

`Constant width`

Used for program listings, as well as within paragraphs to refer to program elements such as variable or function names, databases, data types, environment variables, statements, and keywords.

###### Tip

This element signifies a tip or suggestion.

###### Note

This element signifies a general note.

###### Warning

This element indicates a warning or caution.

# Using Code Examples

Supplemental material (code examples, exercises, etc.) is available for download at [_https://oreil.ly/github-transformers_](https://oreil.ly/github-transformers).

If you have a technical question or a problem using the code examples, please send email to [_support@oreilly.com_](mailto:support@oreilly.com).

This book is here to help you get your job done. In general, if example code is offered with this book, you may use it in your programs and documentation. You do not need to contact us for permission unless you’re reproducing a significant portion of the code. For example, writing a program that uses several chunks of code from this book does not require permission. Selling or distributing examples from O’Reilly books does require permission. Answering a question by citing this book and quoting example code does not require permission. Incorporating a significant amount of example code from this book into your product’s documentation does require permission.

We appreciate, but generally do not require, attribution. An attribution usually includes the title, author, publisher, and ISBN. For example: “_Transformers: The Definitive Guide_ by Nicole Koenigstein (O’Reilly). Copyright 2026 Nicole Koenigstein, 978-1-098-16701-1.”

If you feel your use of code examples falls outside fair use or the permission given above, feel free to contact us at [_permissions@oreilly.com_](mailto:permissions@oreilly.com).

# O’Reilly Online Learning

###### Note

For more than 40 years, [O’Reilly Media](https://oreilly.com/) has provided technology and business training, knowledge, and insight to help companies succeed.

Our unique network of experts and innovators share their knowledge and expertise through books, articles, and our online learning platform. O’Reilly’s online learning platform gives you on-demand access to live training courses, in-depth learning paths, interactive coding environments, and a vast collection of text and video from O’Reilly and 200+ other publishers. For more information, visit [_https://oreilly.com_](https://oreilly.com/).

# How to Contact Us

Please address comments and questions concerning this book to the publisher:

- O’Reilly Media, Inc.
- 141 Stony Circle, Suite 195
- Santa Rosa, CA 95401
- 800-889-8969 (in the United States or Canada)
- 707-827-7019 (international or local)
- 707-829-0104 (fax)
- [_support@oreilly.com_](mailto:support@oreilly.com)
- [_https://oreilly.com/about/contact.html_](https://oreilly.com/about/contact.html)

We have a web page for this book, where we list errata and any additional information. You can access this page at [_https://oreil.ly/transformers-the-definitive-guide_](https://oreil.ly/transformers-the-definitive-guide).

For news and information about our books and courses, visit [_https://oreilly.com_](https://oreilly.com/).

Find us on LinkedIn: [_https://linkedin.com/company/oreilly_](https://linkedin.com/company/oreilly).

Watch us on YouTube: [_https://youtube.com/oreillymedia_](https://youtube.com/oreillymedia).

# Acknowledgments

Writing a book or pursuing a career in a ﬁeld such as AI is never truly a solitary eﬀort. This feels especially true today, as the pace of progress in AI continues to accelerate, and the exchange of ideas becomes increasingly important, even though much of the work itself still happens during long, solitary days of research, coding, and writing. I would like to take this moment to thank the people who supported and inspired me at important moments throughout this journey.

In this spirit, I would like to thank colleagues, peers, students, readers, and course participants who engage with my work. Through discussions, questions, collaborations, and a shared curiosity about AI, these exchanges provide perspective and inspiration that shape how ideas develop and mature over time.

Special thanks go to Nicole Butterﬁeld for her continued support during some of the more challenging moments while ﬁnishing this book. I would also like to express my appreciation to the rest of the team at O’Reilly who helped guide this book from manuscript to publication. In particular, I am grateful to Sarah Grey and Liz Faerm for their thoughtful support throughout the development process and for making my work as an author both easier and genuinely enjoyable. I would also like to thank the many members of the production team whose work behind the scenes helps bring a book like this to life.

Finally, I would like to thank the technical reviewers, Chris Fregly, Al Krinker, and Dibyendu Roy Chowdhury. Your careful review, questions, and feedback helped clarify important points and strengthen the overall quality of the book.
With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 7th chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

The diagrams we’ve seen so far provide an approach to think about, describe, and communicate the static structure of a software system at different levels of abstraction - software systems, containers, components, and code. Whenever I’ve needed to document a software system in the past, most of the diagrams I’ve created have also been descriptions of the static structure.

Software isn’t static though, and it needs to be executed in order to actually _do_ something. For this reason, it can be useful to create diagrams that illustrate what happens at runtime during the execution of individual features. This is the purpose of the dynamic diagram in the C4 model.

# Intent

The static structure diagrams show the complete set of static elements and relationships that make up the software system, but an individual feature only involves a subset of those elements collaborating at runtime. The intent of a dynamic diagram is to illustrate how an individual feature works at runtime, by only showing the elements that are used in the delivery of that feature.

# Scope

The scope of a dynamic diagram will vary based upon the story that you want to tell, and how you want to tell it. At the highest level of abstraction, you could show how software systems collaborate at runtime to provide a specific business capability. At the lowest level you could show how the code elements within a component interact at runtime to perform a specific function of the component.

As with static structure diagrams, I recommend constraining the scope of your diagrams as far as possible. You could show, for example, how components in one container interact with components in another container, but resist the temptation to do this, particularly when those containers span multiple software systems. I’ll explain more about the rationale behind this in Chapter 11 when we look beyond the basics.

# Content

Dynamic diagrams show how elements, or more specifically, _instances of elements_, interact at runtime. We can use the concept of _sequence_ and _collaboration_ diagrams from UML as a way to illustrate behaviour.

## Sequence diagram

A [UML sequence diagram](https://en.wikipedia.org/wiki/Sequence_diagram) ([Figure 7-1](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch07.html#ch07_figure_1_1773432249030359)) shows a number of element instances that are interacting (left to right) and a timeline (top to bottom). The diagram illustrates how the elements collaborate (using horizontal arrows) by sending messages, making requests, etc. The vertical order of the arrows illustrates the sequencing, from start to finish.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch07_figure_1_1773432249030359.png)

 Figure 7-1. An example UML sequence diagram

UML sequence diagrams usually show instances of classes (objects) collaborating at runtime, but there’s nothing preventing you showing instances of other static elements such as people, software systems, containers, or components.

If you’re already familiar with UML sequence diagrams, you will probably know that you can specify additional precision with guard conditions, loops, and lifeline events (e.g. creation and destruction). If you are using a UML tool to create dynamic diagrams, feel free to use these UML features if you find they add value.

## Collaboration diagram

The other approach to diagramming behaviour is a [UML collaboration diagram](https://en.wikipedia.org/wiki/Communication_diagram) ([Figure 7-2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch07.html#ch07_figure_2_1773432249030396), known as a “UML communication diagram” in UML 2.x). Essentially this shows the same information as a sequence diagram, although that information is presented as a simpler “boxes and arrows” style diagram with free-form arrangement, with the lines numbered to indicate the ordering of interactions.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch07_figure_2_1773432249030396.png)

 Figure 7-2. An example UML collaboration/communication diagram

Sequence and collaboration diagrams can be used to show the same information in a different way, so feel free to use whichever you prefer. I tend to prefer the collaboration diagram because it’s visually simpler and easier to draw, especially on a whiteboard, but either diagram type works provided you’re not trying to show too many collaborations.

# Motivation

The static structure diagrams that make up the core of the C4 model provide a way to see a summary of the elements that exist across the various levels of abstraction. But it’s usually hard to see how an individual feature works in isolation. This is the motivation behind the dynamic view.

# Audience

The audience will depend upon the level of abstraction(s) that you show on the diagrams, and mirror the audience suggestions for the corresponding static structure diagrams:

- Software systems collaborating: the same audience as system context diagrams (technical and non-technical people).
    
- Containers collaborating: the same audience as container diagrams (architects and engineers).
    
- Components collaborating: the same audience as component diagrams (architects and engineers).
    
- Code elements collaborating: the same audience as code diagrams (engineers).
    

# Recommended?

Yes, but with a caveat. If you’re building a software system that provides one hundred unique features, there’s likely little value in creating one hundred dynamic diagrams, one per feature. It would be a considerable amount of work to create this large collection of dynamic diagrams and keep them up to date when the code changes. For this reason I recommend using dynamic diagrams sparingly, perhaps only to show interesting or recurring patterns (e.g. to describe architectural styles), or perhaps features that involve a complicated set of interactions best described with a diagram rather than text.

# Example

Let’s see an example from the fictional _Internet Banking System_, in this case showing how the “sign in” feature might work, specifically focussing on the component level of the _Backend_ container. Both the sequence style ([Figure 7-3](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch07.html#ch07_figure_3_1773432249030420)) and collaboration style ([Figure 7-4](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch07.html#ch07_figure_4_1773432249030441)) example diagrams show the same information:

1. The _UI_ container submits user credentials via an API request to the _Sign In API_ component in the Backend.
    
2. The _Sign In API_ component uses the _Security Component_ to validate the credentials.
    
3. The _Security Component_ in turn retrieves the user’s account information from the _Database container_.
    
4. The _Database_ returns the requested information.
    
5. The _Security Component_ validates the credentials (e.g. compares the hashed password), and issues a session token to the _Sign In API_ component if successful.
    
6. The _Sign In API_ component sends back the session token to the _UI_.
    

[Figure 7-3](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch07.html#ch07_figure_3_1773432249030420) shows the sequence style diagram.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch07_figure_3_1773432249030420.png)

 Figure 7-3. An example dynamic diagram (sequence style) for the sign in feature of the Internet Banking System

[Figure 7-4](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch07.html#ch07_figure_4_1773432249030441) shows the collaboration style version, which uses a subset of the boxes and arrows that we used on the example component diagram (Figure 5-4) back in Chapter 5, to illustrate how the sign in feature works.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch07_figure_4_1773432249030441.png)

 Figure 7-4. An example dynamic diagram (collaboration style) for the sign in feature of the Internet Banking System

# Summary

This chapter has introduced the dynamic diagram. It’s a useful tool, when used sparingly, to illustrate how an individual feature works at runtime through a subset of static structure elements collaborating. The next chapter will look at the deployment diagram.
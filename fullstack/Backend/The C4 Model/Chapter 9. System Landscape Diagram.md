With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 9th chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

The core of the C4 model provides a static view of a _single software system_ but software systems never live in isolation. For this reason, and particularly if you are responsible for a collection of software systems, it’s often useful to understand how all of these software systems fit together. To do this, I’ll add another diagram that sits “on top” of the C4 diagrams, to show the software system landscape. This is the purpose of the system landscape diagram, and the focus of this chapter.

# Intent

The system landscape diagram allows you to answer the following types of questions:

- How do the various software systems in the group/department/organisation fit together?
    
- What is the impact if a particular software system changes or is removed from the environment?
    
- What is the impact if we decide to restructure, merge, or break up the organisation?
    

# Scope

The scope of a system landscape diagram is really your choice, and some common examples are to include all software systems that reside inside:

- An organisation (this only works for small organisations).
    
- A group or department.
    
- A product domain.
    
- A business capability.
    
- A DDD bounded context.
    

# Content

From a practical point of view, a system landscape diagram is really just a system context diagram without a specific focus on a single software system. It shows the people and software systems that are related to a given scope. A system landscape diagram usually includes two types of elements: _people_ and _software systems_.

# Motivation

Although the discipline of enterprise architecture isn’t just about software systems, in my experience, many organisations don’t have a top-down holistic view of their IT landscape. In fact, it shocks me how often I see organisations of all sizes that lack such a view, especially when you consider that technology is usually a key part of the way they implement business processes and serve customers. Diagramming the landscape from a software system perspective at least provides a way to think outside the typical silos that form around IT systems and the teams that are responsible for them.

# Audience

The audience for the system landscape diagram is the same as that for the system context diagram - technical and non-technical people, inside and outside the software development team.

# Recommended?

Yes, particularly for larger organisations. The system landscape diagram is a bridge into the world of enterprise architecture. Larger organisations tend to find this diagram useful because it forms a map of the software systems that exist within all or part of the organisation. Make this diagram interactive (e.g. double-click a software system to navigate to the C4 model diagrams for that software system) and you have an interactive map of your system landscape.

# Example

When drawing a system context diagram, I usually only include the people and software systems that have a _direct relationship_ with the software system in focus. In contrast, a system landscape diagram shows a wider view in order to tell a broader story.

[Figure 9-1](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch09.html#ch09_figure_1_1773432250712677) illustrates the starting point for a partial system landscape diagram for the fictional bank. It shows the same content as the system context diagram for the _Internet Banking System_ that we saw back in Figure 3-4.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch09_figure_1_1773432250712677.png)

 Figure 9-1. The start of a system landscape diagram for the bank

We can now start to diagram some of the wider landscape, as illustrated by [Figure 9-2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch09.html#ch09_figure_2_1773432250712707).

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch09_figure_2_1773432250712707.png)

 Figure 9-2. An example system landscape diagram for the bank

We additionally have the _ATM_ software system along with _Customer Support Staff_ and _Back Office Staff_ that are internal to the bank, all of which have a relationship to the _Core Banking System_. I’ve also chosen to include the relationship between the _Personal Banking Customer_ and _Customer Support Staff_ too, because it helps tell the story of why the support staff use the _Core Banking System_.

[Figure 9-3](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch09.html#ch09_figure_3_1773432250712727) shows the visual diagram key that I would use to accompany the system landscape diagram. Since the example diagram shows the same types of elements (people and software systems) as the example system context we saw in Chapter 3, the visual style of the key is the same too.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch09_figure_3_1773432250712727.png)

 Figure 9-3. A diagram key for the example system landscape diagram

[Figure 9-4](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch09.html#ch09_figure_4_1773432250712745) shows a further modified example of the system landscape diagram, which additionally has two boxes with a dotted border to represent the organisational boundary of _Big Bank_ and _Amazon Web Services_. This helps to highlight which of the software systems and people reside within the boundaries of the bank, versus those that reside outside.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch09_figure_4_1773432250712745.png)

 Figure 9-4. An example system landscape diagram for the bank, now additionally showing organisational boundaries

# Summary

This chapter has described the purpose of the C4 system landscape diagram, which is essentially a C4 system context diagram without the focus on a single software system. It’s a simple yet effective way to create a map of the software systems that reside within a particular group, department, or organisation.

With our look at the diagram types provided by the C4 model complete, the next chapter will shift the discussion from diagram content to diagram notation.
With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 5th chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

This chapter looks at the C4 component diagram, which provides a way to zoom in to show the components that reside inside a single container.

# Intent

A component diagram helps you answer the following questions, particularly for the containers that are _applications_ rather than data stores:

- How has the container been decomposed into a collection of components?
    
- What are the responsibilities of those components?
    
- How do the components collaborate and communicate with one another?
    
- What are the primary technology choices (e.g. frameworks and libraries) used to implement the components?
    
- As a software engineer, where do I need to write code to add a feature?
    

If you’re drawing a component diagram during an up-front design exercise, you might not have some of the technical details to hand. Once again, don’t worry, add what you know. If, on the other hand, you’re drawing a diagram to document an existing system, you’ll have those finer details to hand, such as the frameworks and libraries you are using to implement a component.

# Scope

The scope of a component diagram is a _single container_. If you’re building a software system that consists of three applications, you might be tempted to create a single component diagram that shows the components inside all three of those containers at the same time. I would resist the temptation to do this and draw three separate component diagrams instead - one component diagram per container. Doing this will result in three smaller and simpler component diagrams, and you’ll reduce the cognitive load of trying to understand the internals of three applications simultaneously.

# Content

A component diagram usually includes six types of elements - _people_, _software systems_, and _containers (from the previous container diagram) plus_ _components_, the _container boundary_, and the _software system boundary_.

## People, Software Systems, and Containers

The component diagram is a zoom in of a single container from a container diagram, which itself is surrounded by a number of people, software systems, and other containers. Those same elements should be repeated on the component diagram to provide continuity. Again, you’re telling a more detailed version of the same story.

## Components

The component diagram shows the set of components that exist within the boundary of the container. I’ll capture the following information for each component:

Name

The name of the component.

Technology

The primary implementation technology.

Description

A short summary of the component’s responsibilities.

In the context of an application, a component is a group of related code. The component diagram should therefore reflect the components (groupings of code) that reside within your container, and the architectural style in use. If you consider your application to consist of components organised in architectural layers, your component diagram should show components organised in layers. If your container makes use of components organised in a “ports and adapters” or “hexagonal” style, the diagram should reflect this too.

## Container Boundary

To avoid confusion, I recommend drawing a box around the components on your component diagram to explicitly show the container boundary. This container boundary should correspond to the single box representing the container on the container diagram.

## Software System Boundary

You can additionally show the boundary of the parent software system if you’d like to be even more explicit about the hierarchy of elements. We’ll see an example of this shortly.

## Relationships

To reiterate the same advice given for other diagram types, I recommend unidirectional arrows, each labelled with the following information:

Description

A summary of the relationship (e.g. “reads data from”, “validates token using”, etc).

Technology

If applicable, the major protocol in use (e.g. JSON/HTTP, gRPC, etc).

It’s worth noting that the majority of component-to-component interactions are usually just method/function calls between code that exists inside the same process space. In these cases you don’t need to add information about the technology. As before though, you could include information about whether the interaction is synchronous or asynchronous, perhaps using different types of line styles (e.g. solid for synchronous, dashed for asynchronous).

# Motivation

A component diagram shows the components that reside inside an individual container. This is useful because:

- It shows the high-level decomposition of a container into components, providing a summary of the high-level structure of the codebase for a given application.
    
- It shows where there are relationships and dependencies between components.
    
- It provides a high-level summary of the implementation details, including any frameworks or libraries being used.
    

# Audience

The intended audience for a component diagram is the technical people within the software engineering team (e.g. architects and engineers), along with anybody else that has an interest in how the code is structured (e.g. third level support staff, maintenance engineers, etc). Component diagrams may be useful for non-technical people, but this isn’t the intended audience.

# Recommended?

Generally not. First of all, I don’t create component diagrams for data storage containers (e.g. databases, file systems, content stores, etc) because they are better documented using existing approaches such as entity relationship diagrams. I also wouldn’t create component diagrams for application containers that are very simple in nature, such as an application that exposes a single API endpoint - the sort you might find with the microservices architectural style, where each service provides a single purpose.

Component diagrams are more suited to documenting the internals of larger applications, but I still recommend them as an _optional level of detail_ to most engineering teams, both for up front design exercises and for long-lived documentation.

If I’m designing a small to medium size application, it can be useful to sketch out a component diagram to illustrate an initial idea for the intended high-level code structure. This might become tedious and time consuming if you are designing a larger application though.

The same is true for long-lived documentation when you are creating a component diagram for an application that already exists, but you additionally have the overhead of keeping the component diagram up to date when the code changes. Unlike the system context and container diagrams that potentially don’t change often, component diagrams are subject to a higher level of volatility and will age rapidly when the code changes. You can counter this by adopting a tool that is able to analyse your codebase and automatically generate a component diagram. As we’ll see in Chapter 12 though, this is a non-trivial exercise for most programming languages, and the effort required to set this up may exceed the value you get from the resulting component diagrams, particularly if your codebase is well structured.

Finally, there’s also the visual element to consider. You’ll find the diagram starts to become cluttered very quickly once you have more than a handful of components, which reduces the usefulness of the diagram. We’ll look at some strategies for dealing with this in Chapter 11.

To summarise, the component diagram is a useful tool to have in your diagramming toolbox, but I wouldn’t recommend it to all engineering teams.

# Example

Let’s continue with the Internet Banking System example, and zoom in to the Backend container to show the components that reside inside it. The starting point for our component diagram is illustrated in [Figure 5-1](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch05.html#ch05_figure_1_1768319632970567). It shows the same _UI_, _Database, Statement Store_, _Core Banking System_, and _Amazon Web Services Simple Email Service_ as the container diagram in Chapter 4. The _Backend_ box is now representing the boundary of the container, inside of which will be the components. The software system boundary surrounds this container boundary, along with the other containers (the UI, Database, and Statement Store) that reside inside the Internet Banking System software system.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch05_figure_1_1768319632970567.png)

 Figure 5-1. An example component diagram for the Backend of a fictional Internet Banking System (step 1)

Customers will need to sign in to the Internet Banking System before they can access any of the functionality, so let’s start our story with the sign in flow, as illustrated in [Figure 5-2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch05.html#ch05_figure_2_1768319632970606). In this example, the UI will make a sign in request, via a JSON/HTTP API call, to the _Sign In API_ (built using the Spring MVC framework). This will in turn use the _Security Component_ (a Spring Bean - a Java component managed by the Spring Framework) to validate the user’s credentials against the database, and issue an authentication token if successful. The Security Component may also send emails via the _Email Component_ (another Spring Bean), for example if multi-factor authentication is enabled or to warn of a sign in from a new location.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch05_figure_2_1768319632970606.png)

 Figure 5-2. An example component diagram for the Backend of a fictional Internet Banking System (step 2)

[Figure 5-3](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch05.html#ch05_figure_3_1768319632970628) shows that the UI can request a list of the customer’s bank accounts via a JSON/HTTP API call that is handled by the _Accounts Summary API_ (also built using Spring MVC). It in turn uses the _Security Component_ to validate the authentication token, and requests a list of bank accounts from the _Core Banking System_ using the _Core Banking System Adapter_ component (another Spring Bean).

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch05_figure_3_1768319632970628.png)

 Figure 5-3. An example component diagram for the Backend of a fictional Internet Banking System (step 3)

To access bank account statements, customers can use the UI to request a statement, which results in a JSON/HTTP API call to the _Statement API_ (also built using Spring MVC). Assuming the authentication token is validated successfully by the _Security Component_, the _Statement API_ subsequently uses the _Statement Component_ (a Spring Bean), which will either return the statement from the _Statement Store_ if it has already been generated and cached, or generate it by first requesting the required statement information from the _Core Banking System_ via the _Core Banking System Adapter_. [Figure 5-4](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch05.html#ch05_figure_4_1768319632970645) shows this additional flow.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch05_figure_4_1768319632970645.png)

 Figure 5-4. An example component diagram for the Backend of a fictional Internet Banking System (step 4)

You may have noticed that, as we increase the number of elements and relationships, the diagram starts to become more cluttered. In particular, you can see that some of the relationships are starting to cross one another, and this will become more prevalent if we add yet more elements to the diagram. This often leads to the question of whether this approach is scalable, and how to diagram software systems that are much larger in size and complexity than what we see here. That topic will be covered in Chapter 11 when we look beyond the basics.

[Figure 5-5](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch05.html#ch05_figure_5_1768319632970661) shows the visual diagram key that I would use to accompany the component diagram. The visual style extends that used by the system context and container diagrams, with all components rendered using a UML component shape.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch05_figure_5_1768319632970661.png)

 Figure 5-5. A diagram key for the example component diagram

# Summary

This chapter has described the C4 model component diagram, which shows the components inside a single container, which themselves should be a reflection of the high-level code structures that exist in the codebase. The next chapter completes the static structure story by using the code diagram to zoom in to a single component.
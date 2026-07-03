With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 2nd chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

This chapter looks at the basics of the C4 model for visualising software architecture. The first part discusses the importance of creating a shared language through the set of hierarchical abstractions that form the heart of the C4 model, and the second part introduces the set of diagrams from which C4 takes its name - _System Context, Containers, Components, and Code_.

# Common Abstractions Over a Common Notation

The diagrams we’ve seen so far have been a collection of ad hoc “boxes and arrows”, with a wildly different use of colours, shapes, line styles, etc. But it’s not just the notation that varies, it’s the abstractions that vary too.

Other professions are much more mature in this respect. Let’s take electrical engineering as an example. A typical circuit diagram may include one of several symbols that are commonly used to represent a resistor, as shown in Figure 2-1. That symbol is a standard notational element on the diagram, and a resistor is an object that exists in the real world.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch02_figure_1_1758915929068878.png)

 Figure 2-1. Symbols that are used to represent different types of electrical resistors

The software development industry does have UML, SysML, and ArchiMate that provide us with a shared language. UML, for example, has some standard notational elements that can be used to designate a component, as shown in Figure 2-2.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch02_figure_2_1758915929068903.png)

 Figure 2-2. Symbols that are used to represent components in UML

The problem here is that the definition of “component” is arguably vague and ambiguous. From the [UML specification](https://www.omg.org/spec/UML/2.5.1/About-UML), a component is defined as:

> “a modular unit with well-defined Interfaces that is replaceable within its environment”

Similarly, a typical dictionary definition for the word “component” is:

> “a part of a larger whole”

Imagine that you’re building a software system that consists of a web application and a database. Given the previous definitions, both of the following uses of the word “component” are valid:

- The web application is a _component_ of the software system.
    
- The web application is made up of a number of _components_.
    

The word “component” here is being used to describe two very different levels of abstraction. This can easily lead to a situation where team members are using the same type of words in conversation and the same boxes (notation) on their diagrams, but they represent very different things (abstractions) from a structural perspective.

Notation is certainly important, however, one of the fundamental problems I believe we have in the software development industry is that we lack a common shared vocabulary with which to think about and describe the software systems we build from a structural perspective - the architectural building blocks that our software systems are composed of. I’d definitely like us to reach a point where I can draw a specific symbol on a diagram, and that symbol is universally understood across the software development industry–much like the electrical resistor example that I previously mentioned. But given the industry’s lack of maturity and discipline in this area, and software architecture diagramming in general, I think we have a way to go before this is feasible. For now then, perhaps having a common set of abstractions is potentially much more important than having a common notation.

Most maps are a great example of this principle in action. If you take two different maps of your local area and place them side by side, they will both show the major roads, rivers, lakes, forests, towns, districts, schools, churches, and so on. Visually though, these maps will likely use different notation in terms of colour coding, line styles, iconography, etc. In other words, the maps are showing the same things (the same abstractions), but the notation varies. The key to understanding a map is exactly that - a key or legend tucked away in a corner. A map is therefore a well-known set of abstractions with a varying or variable notation, described via a key/legend. This is a very powerful concept that we can borrow to create better software architecture diagrams - think of them as the maps that help software developers navigate a complex codebase.

In order to get to this point though, we need to agree upon some abstractions that we can use to describe our software systems. And this is the step that is usually missed during the initial iteration of my software architecture diagramming workshops. Teams charge headlong into the exercise without having a shared understanding of the words they are using. I’ve witnessed groups of people having design discussions in front of a diagram, each person using the word “component”, where they are clearly not talking about the same thing. Yet everybody in the group is oblivious to this. Each group needs to agree upon the vocabulary, terminology, and abstractions they are going to use to describe their software system. The notation can then evolve as a secondary concern.

# Abstractions

Notation aside for now (we’ll cover that in Chapter 10), my approach to tackling this problem is to introduce a shared vocabulary that we can use to describe our software. The primary aspect I’m interested in is the _static structure_. And I’m interested in the static structure from _different levels of abstraction_, as illustrated in Figure 2-3. Once the static structure is understood, it’s easy to supplement it with other information to illustrate runtime/behavioural characteristics, deployment topologies, etc.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch02_figure_3_1758915929068922.png)

 Figure 2-3. A lightweight model of hierarchical architectural constructs used to define the static structure of a software system

In summary, a _software system_ is made up of one or more _containers_ (applications and data stores), each of which contains one or more _components_, which in turn are implemented by one or more _code_ elements (e.g. classes, interfaces, objects, functions, etc). And _people_ (actors, roles, personas, named individuals, etc) use the software systems that we build.

Let’s look at each of these in turn.

## Software System

A software system is the highest level of abstraction and describes something that delivers value to its users, whether they are human or not. This includes the software system you are describing, and the other software systems upon which your software system depends (or vice versa).

The term “software system” is the hardest of these abstractions to define, and this isn’t helped by the fact that each organisation will also have its own terminology for describing the same thing, typically using terms such as “application”, “product”, “service”, etc.

One way to think about it is that a software system in the C4 model is something a single software development team is building, owns, has responsibility for, and can see the internal implementation details of. Perhaps the code for that software system resides in a single source code repository, and anybody on the team is permitted to modify it. In many cases, the boundary of a software system will correspond to the boundary of a single team. It may also be the case that everything inside the boundary of a software system is deployed at the same time.

The “Financial Risk System” that was the focus of the example diagrams in [Chapter 1](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch01.html#ch01_a_failure_to_communicate_1758915928497269) is a good example of a software system. Other examples include the “Trade Data System” and the “Reference Data System”.

Things that are not usually software systems in the C4 model include product domains, bounded contexts, business capabilities, feature teams, tribes, or squads. More about this in Chapter 11 when we look beyond the basics of the C4 model.

## Container

In the C4 model, a container represents an _application_ or a _data store_. A container is something that needs to be running in order for the overall software system to work. In real terms, an application container is something like:

Server-side web application

A Java EE web application running on Apache Tomcat, an ASP.NET MVC application running on Microsoft IIS, a Spring Boot application, a Ruby on Rails application running on WEBrick, a Node.js application, etc.

Client-side web application

A single-page application running in a web browser using JavaScript, AngularJS, React, Backbone.JS, jQuery, etc.

Client-side desktop application

A Windows desktop application written using Windows Presentation Foundation (WPF), a macOS desktop application written using Swift or Objective-C, a cross-platform desktop application written using JavaFX, etc.

Mobile app

An Apple iOS app, an Android app, etc.

Server-side console application

A standalone (e.g. “public static void main”) application written in Java, C#, C++, Python, Perl, etc.

Serverless function

A single serverless function (e.g. Amazon Web Services Lambda, Microsoft Azure Function, etc).

Shell script

A shell script written in Bash, Zsh, etc.

And a data store container might be:

Database

A schema in a relational database management system (e.g. MySQL, Microsoft SQL Server, Oracle Database, etc), a collection of documents in a document store (e.g. MongoDB), a graph in a graph database (e.g. Neo4j), or a collection of data in another NoSQL database (e.g. Redis, Riak, Cassandra, etc).

Blob or content store

A blob store (e.g. Amazon Web Services S3 bucket, Microsoft Azure Blob Storage container, etc) or set of files on a content delivery network.

File system

A full local file system or a portion of a larger networked file system (e.g. SAN, NAS, etc).

A container is a runtime concept, representing a boundary around some code that is being executed or some data that is being stored. The name “container” was chosen for this level of abstraction because I wanted a name that didn’t imply anything about the physical nature of how that container is executed or deployed. In other words, containers have some degree of isolation between them, irrespective of their deployment.

As an example, a single Java EE server like Apache Tomcat can run multiple Java EE web applications (A and B) inside a single Java Virtual Machine (JVM), although each of those web applications is isolated from the other via separate Java class loaders. The code in application A can’t make in-process method calls to the code in application B, despite both applications running in the same JVM and operating system process. I could alternatively choose to deploy each application to its own separate Apache Tomcat server, for additional isolation.

The same is true with relational database schemas. There are some exceptions but, generally speaking, tables in one database schema (A) cannot be joined to tables in another database schema (B). Again, there is a degree of isolation between the schemas A and B, irrespective of whether they are deployed into the same database server or not.

The idea here is that each container is a separately deployable/runnable thing, and there is a degree of isolation between them. The implication here is that communication between containers is likely to require an out-of-process/remote call across a process or network boundary.

As a final note, I do appreciate that the term container is now in widespread use because of containerisation and technologies such as Docker and Kubernetes, and the clash of naming is somewhat unfortunate. The majority of teams that use the C4 model don’t have an issue with this, and it’s not the first time that a term in software engineering has multiple meanings. If this does bother you though, feel free to say “C4 container” instead of just “container” to avoid any confusion.

## Component

As you have seen, the word “component” is a hugely overloaded term in the software development industry, but it’s a useful word to use to describe the internal structure of application containers. I like to think of a component in the C4 model as being a grouping of related functionality encapsulated behind a well-defined interface, running inside a container.

A component is essentially a collection of code. It’s a way to step up one level of abstraction from the code-level building blocks that you have in the technology you’re using. For example:

Java, C#, C++, and other object-oriented languages

A component could be a collection of classes, interfaces, and enums.

C and other procedural programming languages

A component could be a collection of files in a particular directory.

F#, Haskell, and other functional programming languages

A component could be a module - a logical grouping of related functions, types, etc.

JavaScript

A component could be a JavaScript module - a number of objects and functions.

With the C4 model, components are not separately deployable units. Instead, it’s the container that’s the deployable/runnable unit, with components running inside those containers. In other words, all of the components inside a container execute in the same process space, and can easily communicate with one another via in-process method calls, for example. “Containers contain components” is another way to remember this, and helps to explain where the “container” name came from.

Aspects such as how those components are packaged (e.g. one component vs many components per JAR file, DLL, shared library, etc) is an orthogonal concern and, from my perspective, doesn’t affect how we think about components. We will revisit this topic in Chapter 11 when we look beyond the basics of the C4 model.

## Code

Finally, and as we’ve just seen, this level represents the internals of our components in terms of the basic building blocks of the programming language that we’re using - classes, interfaces, enums, functions, objects, etc.

# Static Structure Diagrams

The abstractions that we’ve seen provide a way to create a shared non-visual vocabulary at four levels of abstraction and, with these in mind, we can now move on to draw some diagrams at varying levels of abstraction to visualise the static structure of a software system. Figure 2-4 provides an overview of the four levels of static structure diagrams, which is the heart of the C4 model and the origin of the “C4” name - System Context, Containers, Components, and Code.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch02_figure_4_1758915929068937.png)

 Figure 2-4. A summary of the C4 model - System Context, Containers, Components, and Code

You can think of these hierarchical static structure diagrams as being a set of maps for a software system, providing you with the ability to zoom in and out at varying levels of detail, and to tell different stories to different audiences.

System context diagram

My starting point for understanding any software system is to draw a system context diagram, showing how the software system in scope fits into the world around it. This helps me to understand the scope of the system, who is using it, what those users are doing, and what the external software system dependencies are. It’s usually quick to draw and quick to understand. Chapter 3 will look at the system context diagram in more detail.

Container diagram

Next I’ll zoom into the software system and draw a diagram showing the containers (applications and data stores) that reside inside the boundary of the software system. This shows the overall shape of the software system in terms of applications and data stores, how responsibilities have been distributed across them, how they interact, and the key technology choices that have been made. This is the focus of Chapter 4.

Component diagram

As developers, we sometimes need more detail, and a component diagram zooms into an individual application container, showing the components inside it. This is where we show how each application has been decomposed into components, again showing how responsibilities have been distributed across those components, how they interact, and the key technology choices that have been made. Component diagrams are the subject of Chapter 5.

Code diagram

A code (e.g. UML class) diagram can be used to zoom into an individual component, showing how that component is implemented via a collection of code-level elements. We’ll look at this in more detail in Chapter 6.

# Supporting Diagrams

Although the C4 model takes its name from the set of four hierarchical static structure diagrams, there are also three other supporting diagrams.

Dynamic diagram

A dynamic diagram can be useful when you want to show how elements in the static model (software systems, containers, components, and code) collaborate at runtime to implement a user story, use case, feature, etc. The most common example of a dynamic diagram is a UML sequence diagram but, as we’ll see later in Chapter 7, that’s not the only way to present this information.

Deployment diagram

A deployment diagram allows you to illustrate how instances of software systems and/or containers in the static model are deployed on to the infrastructure within a given deployment environment (e.g. production, staging, development, etc). This is useful for both on-premises and cloud deployments, helping to bridge the gap between the developers that build the software and the infrastructure/operations staff that run the software. Chapter 8 takes a look at deployment diagrams in more detail.

System landscape diagram

The system context, container, component, and code diagrams are designed to provide a narrow focussed static view of a single software system. In the real world, of course, software systems never live in isolation. This is the purpose of a system landscape diagram - it’s a map of the software systems within the chosen scope (e.g. organisation, group, department, business function, etc). We’ll look at system landscape diagrams in Chapter 9.

# Notation

The C4 model is _notation_ _independent_, and doesn’t prescribe any particular notation. That said, I will provide you with some tips for creating a good notation in Chapter 10, but you’re free to use whatever notation you like, provided it’s described with a diagram key/legend.

# Usage Notes and Recommendations

As we’ll see when we look at each of the diagram types in more detail over the next few chapters, having a collection of software architecture diagrams at different levels of abstraction allows us to tell different stories to different audiences. The system context diagram is reasonably high-level and therefore suitable for almost everybody associated with the process of building software. The code level diagrams, on the other hand, are really just for developers.

This concept can be used to your advantage. The different levels of diagrams will age at different rates, with the component and code level diagrams being more volatile and changing more rapidly than the system context and container diagrams. Although the “C4 model” has the number four in its name, you don’t need to use all four levels of diagrams. The four levels of diagram are there for completeness, providing a way to start with the software system as a single box on a diagram, gradually zooming in to navigate through the internals of that software system, through containers, components, and down to the code level.

My recommendation is to only use the diagram types that add value, and my experience suggests the system context and container diagrams are sufficient for most software development teams. You need to consider whether the benefit of having component and code level diagrams justifies the cost of creating and maintaining them over time. More about this when we talk about the C4 model in practice in Chapter 12.

It’s also worth noting that the C4 model was not designed as a replacement for all of the other diagram types that exist within the software development industry. The purpose of the C4 model is to bring structure to the ad hoc “boxes and arrows” diagrams that are typically created to describe software architecture. You can and should still use other diagrams to supplement and complement the C4 model diagrams where necessary. For example:

- UML activity diagrams to describe business processes and workflows.
    
- UML state charts to describe state machines.
    
- UML class diagrams to describe domain models.
    
- Entity relationship diagrams to describe relational data models.
    
- ArchiMate diagrams to describe the various aspects and layers of enterprise architecture.
    

A couple of additional notes. First of all, the C4 model is not a description of a software design process - it’s just a collection of hierarchical diagrams that you can use to describe the static structure of a software system at various levels of abstraction. Whenever I’m asked to create some software architecture diagrams, whether to understand an existing system, present a system overview, or do some software archaeology, I tend to start with the system context diagram and work my way down into the detail, iterating between levels to refine as necessary. You can create these diagrams anyway that you like though.

Finally, the C4 model is not universally applicable. It works well to describe, document, and diagram custom-built, bespoke software systems with a variety of software architectures (monolithic or distributed), built in a variety of general purpose programming languages, deployed on a variety of platforms (on-premises or cloud). Solutions that are perhaps less suited to the C4 model include embedded systems/firmware, and solutions that rely on heavy customization rather than bespoke development (e.g. SAP and Salesforce). Even with these solutions, you still may find the system context and container diagrams useful. The C4 model is also less suited to diagramming libraries, frameworks, and SDKs. All of these may be better described using UML, for example.

# Summary

This chapter has introduced the abstractions that sit behind C4 (software systems, containers, components, and code), and the set of diagrams that form the C4 model. The next chapters will take a look at each of these diagram types in turn.
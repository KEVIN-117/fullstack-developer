With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 4th chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

Once you’ve created a system context diagram, and you understand how your software system fits into the overall system landscape, the next step is to describe the _applications_ and _data stores_ (the C4 containers) that exist within the boundary of the software system. This is the purpose of the C4 container diagram and the topic of this chapter.

# Intent

A container diagram helps you to answer the following questions:

- How has the software system been decomposed into applications and data stores?
    
- What are the responsibilities of those applications and data stores?
    
- What are the primary technology choices (e.g. programming languages and products) used to implement those applications and data stores?
    
- How do the applications and data stores communicate with one another?
    
- As a software engineer, where do I need to write code to add a feature?
    

An important point to note here is that container diagrams should say very little (ideally nothing) about _deployment_ aspects such as cloud environments, servers, Kubernetes clusters, Docker containers, load balancers, firewalls, application gateways, failover, etc. Why? Because these will likely vary across _different deployment environments_ - for example development vs testing vs production. Deployment information is better captured via one or more deployment diagrams (see Chapter 8), one for each unique deployment environment.

# Scope

The scope of a container diagram is to depict a single software system. You’re zooming in to the software system that is the scope of a system context diagram to show the applications and data stores that exist inside the software system boundary.

# Content

A container diagram usually includes four types of elements: _people_, _software systems_, _containers_, and the _boundary of the software system_ that we’re zooming into.

## People and Software Systems

The container diagram is a zoom in of a single software system from a system context diagram, which itself is surrounded by a number of people and software systems. Those same people and software systems should be repeated on the container diagram to provide continuity. In essence, you’re telling a more detailed version of the same story.

## Containers

Containers are the applications and data stores that make up your software system. I’ll capture the following information about each container:

Name

The name of the container.

Technology

The implementation technology.

Description

A short summary of the container’s responsibilities (for applications) or the entities/tables/files/object/etc that are being stored (for data stores).

If you’re drawing a container diagram during an up-front design exercise, you might not have some of the technical details to hand. That’s fine, just add what you know, even if that’s a short-list of technology choices (e.g. “MySQL or PostgreSQL”) or the general type of technology (e.g. “Relational database schema”). On the other hand, you’ll be able to add the technology details if you’re drawing a diagram to document an existing system.

## Software System Boundary

To avoid confusion, I recommend drawing a box around the containers on your container diagram to explicitly show the software system boundary. This boundary allows you to explicitly show which software system the containers belong to, reinforcing the hierarchical nature of the abstractions that make up the C4 model.

## Relationships

Again, I recommend unidirectional arrows to represent the relationships between containers, each labelled with the following information:

Description

A summary of the relationship (e.g. “reads data from”, “makes API requests to”, etc).

Technology

The primary protocol in use (e.g. HTTP, HTTPS, JSON/HTTPS, SOAP/HTTPS, gRPC/TLS, etc).

The relationships between containers usually represent some form of inter-process communication - i.e. the interaction between containers requires communication outside of process boundaries, often across a network. This is very useful information, which is why I recommend adding the technology details (e.g. primary protocol) to the relationship. You could also include information about whether the interaction is synchronous or asynchronous, perhaps using different types of line styles (e.g. solid for synchronous, dashed for asynchronous).

# Motivation

Where a system context diagram shows your software system as a single box, a container diagram opens this box up to show what’s inside it. This is useful because:

- It shows the applications and data stores that ultimately need to be built, deployed, and operated.
    
- It makes the primary implementation technology choices explicit.
    
- It shows the relationships between containers, and how those containers communicate.
    
- It provides a way to review a new architecture or a change to an existing architecture.
    

This last point is important, and often overlooked in today’s fast paced world of software development. Drawing a container diagram during an up-front design exercise can be invaluable to sense check the proposed design will work. This is especially true when the technology choices are included on the diagram because it forces people to consider whether what they’ve designed is implementable.

For example, I’ve seen countless examples during my workshops where a group has drawn a container diagram showing a technology independent user interface (UI) reading from a technology independent database. I’ll then ask what technology choices the group has in mind, to which they reply something like “React for the UI, and MySQL for the database”. Once those technology choices are annotated on to the diagram, I will then ask, “so how will the React app, which is running in a web browser, communicate with the database? Also, how are you going to manage authentication and authorization of that database connection?”. At a glance, a UI communicating with a database seems sensible. It can seem much less sensible after the technology choices have been added though.

# Audience

Container diagrams are reasonably technical, so the intended audience is the software architects and engineers who are building/maintaining the software. That said, in my experience, a number of other people find container diagrams useful too.

Operations and support staff who are running the software tend to find the container diagrams useful to understand exactly what it is they are supposed to be running and operating. I’ve noticed that many organisations, despite claiming to have adopted a DevOps culture, have a gap between the developers (Dev) and the operations staff (Ops). The developers often don’t appreciate how software is deployed and operated in production, while the operations staff don’t understand how the software has been decomposed into a collection of applications and data stores, and how they all communicate at runtime. The container diagram helps bridge this gap, particularly when paired with the deployment diagrams that we’ll see in Chapter 8.

I’ve also noticed that quality assurance staff and testers can find container diagrams useful too, particularly if they are going to be performing technical testing (e.g. performance testing). On a similar note are the compliance teams and architecture review boards that often exist in larger organisations, who might be responsible for reviewing solutions before they are deployed into a production environment. The container diagram provides a technical summary of the solution, providing a good basis for technical risk reviews, threat modelling, etc.

Finally, I’ve seen non-technical product owners make use of container diagrams too, asking engineers to highlight which containers they are planning to change as a part of a feature that is going to be implemented. In this situation, the product owners are not really doing a technical review, but they do want to sanity check that the engineers have considered the changes they are planning to make.

# Recommended?

Yes, I’d recommend container diagrams to all engineering teams.

# Example

Let’s continue with the Internet Banking System example, and zoom in to the software system to show the containers that reside inside it. The starting point for our container diagram is illustrated in [Figure 4-1](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch04.html#ch04_figure_1_1765466780946206). It shows the same _Personal Banking Customer_, _Core Banking System_, and _Amazon Web Services Simple Email Service_ as the system context diagram. The _Internet Banking System_ box is now representing the boundary of the software system, inside of which will be the containers.

![A diagram of a banking systemAI-generated content may be incorrect.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch04_figure_1_1765466780946206.png)

 Figure 4-1. An example container diagram for a fictional Internet Banking System (step 1)

Now we can start telling the story of how the Internet Banking System is designed, in terms of its applications and data stores. For this fictional example, the _user interface_ (UI) is going to be a single-page JavaScript/Angular application running in a web browser. [Figure 4-2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch04.html#ch04_figure_2_1765466780946236) shows this container residing inside the software system boundary.

![A diagram of a banking systemAI-generated content may be incorrect.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch04_figure_2_1765466780946236.png)

 Figure 4-2. An example container diagram for a fictional Internet Banking System (step 2)

Although single-page applications run inside a web browser, they need to be loaded from somewhere - typically a web server or a content delivery network. [Figure 4-3](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch04.html#ch04_figure_3_1765466780946254) shows the addition of the _directory of static content_ (HTML, CSS, and JavaScript) that makes up the single-page application.

![A diagram of a computer banking systemAI-generated content may be incorrect.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch04_figure_3_1765466780946254.png)

 Figure 4-3. An example container diagram for a fictional Internet Banking System (step 3)

Some of you might be wondering why this box is labelled as “Static Content” and “Directory”, rather than something like a web server (e.g. nginx or Apache) or a content delivery network. As we’ll see in Chapter 8 when we look at deployment diagrams, this provides a way to serve the static content via different mechanisms in different deployment environments.

The UI needs to get data from the Core Banking System, but it can’t do this directly because, for security reasons, it would be unwise to allow connectivity to the Core Banking System over the public Internet. What we’ll do instead is create a _Backend_ that we can secure with the appropriate use of firewalls, routers, and network zones in the live production environment. This Backend will expose a JSON/HTTPS API to the UI via the public Internet, and make requests to the Core Banking System’s API via its XML/HTTPS protocol ([Figure 4-4](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch04.html#ch04_figure_4_1765466780946271)). Java and Spring Boot are widely in use across the bank already, so that will be our technology choice.

![A diagram of a banking systemAI-generated content may be incorrect.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch04_figure_4_1765466780946271.png)

 Figure 4-4. An example container diagram for a fictional Internet Banking System (step 4)

In order for customers to sign in to the Internet Banking System, they will need something like a username and password pair. The Core Banking System already stores customer information, but it’s an off-the-shelf product, so making changes to add a username and password pair is potentially costly and time consuming. For this reason we’ll opt to store user credentials ourselves in a relational database. Since the bank already uses MySQL, we’ll also use it. [Figure 4-5](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch04.html#ch04_figure_5_1765466780946287) shows the addition of a relational database schema to the container diagram.

![A diagram of a banking systemAI-generated content may be incorrect.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch04_figure_5_1765466780946287.png)

 Figure 4-5. An example container diagram for a fictional Internet Banking System (step 5)

The Internet Banking System needs to provide a way for customers to download their bank statements as PDF files. We know that we can request a list of transactions for a given statement period from the Core Banking System, but we understand there are some performance issues when transactions older than one year are requested. To isolate our customers from these performance issues, we’ve decided to cache the generated PDF statements. We already have a relational database schema as a part of our architecture, but it’s not a very good fit for storing PDF files. Since the bank has an existing contract with Amazon Web Services, and the Internet Banking System will be deployed into AWS, we’ll use the S3 object storage service as a way to cache the PDF statements. [Figure 4-6](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch04.html#ch04_figure_6_1765466780946302) adds a _Statement Store_ to the diagram.

![A diagram of a banking systemAI-generated content may be incorrect.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch04_figure_6_1765466780946302.png)

 Figure 4-6. An example container diagram for a fictional Internet Banking System (step 6)

You might have noticed that the container diagram shows two AWS services, with Simple Email Service being modelling as a software system, and the Statement Store S3 bucket being modelling as a container. Why the difference? The answer is as follows:

Simple Email Service

The Java/Spring Boot Backend uses the Simple Email Service API to send emails to our customers. It’s really just a service that we use - an external dependency. Provided that the API is stable, we don’t really need to know too much about how it works, so I’ve chosen to model it as a software system.

S3

Although Amazon Web Services operates and maintains the S3 service, the S3 bucket that we will create is a data store that’s an _integral part_ of our software system. We will have complete control and responsibility for what is stored inside that bucket in terms of the objects, how they are organised in the bucket, and the data format of each object. In summary, the S3 bucket is an integral part of our software system, despite being hosted elsewhere, so I’m modelling it as a container rather than a software system.

The notation used for the example container diagram builds upon that used for the system context diagram in [Chapter 3](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch03.html#ch03_system_context_diagram_1765466780090962) as follows:

- People are represented with a person shape, inside which is a name and short description.
    
- Software systems are represented as a rectangle with rounded corners, inside which is a name and short description.
    
- Containers are represented using different shapes, based upon the type of container. Inside each is a name, short description, and technology choice.
    
- The Internet Banking System software system boundary is shown as a dotted rectangle, surrounding the containers.
    
- Relationships are all unidirectional arrows using a dashed line style, with a short label to describe the intent of the relationship. Many of these also have technology (e.g. protocol) details.
    
- The diagram has been titled “Container View: Internet Banking System” to indicate that it’s illustrating the containers that reside inside the Internet Banking System.
    

[Figure 4-7](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch04.html#ch04_figure_7_1765466780946317) shows the visual diagram key that I would use to accompany the container diagram.

![A diagram of a software systemAI-generated content may be incorrect.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch04_figure_7_1765466780946317.png)

 Figure 4-7. A diagram key for the example container diagram

# Summary

This chapter has explained the purpose of the C4 model container diagram, zooming in to a single software system to show the applications and data stores that reside within it. The next chapter continues the story by zooming in further with a component diagram, showing the components that exist within a single container.
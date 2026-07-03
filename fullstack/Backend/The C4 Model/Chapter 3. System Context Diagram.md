With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 3rd chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

We begin our tour of the diagrams that make up the C4 model with the _system context diagram_ - a useful and logical starting point for diagramming and documenting software architecture. In summary, it provides a way to highlight the software system that we’re describing, surrounded by the people who use it and the other software systems that it interacts with. Lots of detail isn’t important here as this is our zoomed out view showing the “big picture” of the software system and the immediate world around it. The focus of the diagram should be on people (actors, roles, personas) and software systems rather than technologies, protocols, and other low-level details. It’s the sort of diagram that you should be able to show to technical and non-technical people alike.

# Intent

A system context diagram helps you to answer the following questions:

- What is the software system that we are building (or have built)?
    
- Who is using the software system?
    
- What are the various types of users doing with the software system?
    
- How does the software system fit into the existing system landscape?
    

# Scope

The scope of a system context diagram is a single software system. In other words, a system context diagram focuses on a single software system, showing the people and software systems that have a relationship with that software system.

# Content

A system context diagram includes two types of elements; _people_ and _software systems_.

## People

These are the people who use your software system. I usually model users via the different roles they play when using the software, but whether you model your users as individual people, roles, actors, or personas is your choice. I’ll capture the following information about people:

Name

The name of the person, role, actor, or persona.

Description

A short description of the person.

I typically only include the people who are using the software system from a “functional” perspective, such as using the software system to achieve a specific business goal. You can also choose to include system administrators and operational staff too, although I would generally only do this when these people are using a part of your software system that has been built specifically for them. For example, I would include system administrators if the software system includes an administrative user interface. I probably wouldn’t include operational staff who might only be looking at log files. The choice is yours though - include as many people as you feel is appropriate to tell the story that you want to tell. You can also create multiple versions of a system context diagram - perhaps one for the functional users, and one for the system administrators/operational staff.

## Software Systems

These are the other software systems that your software system has a relationship with. Again, I’ll capture the following information about each software system:

Name

The name of the software system.

Description

A short description of the software system.

## Relationships

As we’ll see in Chapter 10 about notation, my recommendation is to represent relationships as unidirectional arrows, each labelled with a summary of the relationship. This helps avoid creating a diagram where a collection of boxes are somehow connected via a set of ambiguous lines. These relationship summaries can be reasonably high level on a system context diagram, and don’t need to include lots of technical details such as protocols and data formats.

# Motivation

A system context diagram doesn’t need to show much detail, so you might ask what the point of such a simple diagram is. Here’s why it’s useful:

- It makes the context and scope of the software system explicit so there are no assumptions.
    
- It shows what is being added to an existing system landscape.
    
- It’s a high-level diagram that technical and non-technical people can use as a starting point for discussions, onboarding new engineers, etc.
    
- It provides a starting point for identifying who you potentially need to go and talk to when understanding inter-system interfaces.
    
- It’s a starting point for the other, more detailed, diagrams that are a part of the C4 model.
    

A system context diagram is a great analysis tool too. I’ve drawn a system context diagram during requirements gathering workshops, to ensure that everybody understands the scope of what we’ve been tasked to build, in terms of what features sit _inside_ the system boundary and what features sit _outside_ the system boundary.

# Audience

The audience for a system context diagram is everybody, both technical and non-technical people, inside and outside the engineering team.

# Recommended?

Yes, I’d recommend system context diagrams to all engineering teams.

# Example

Let’s look at an example. Imagine that we work in an engineering team for a bank, and we’ve been asked to build an Internet Banking System. We’ll start with a system context diagram. Step 1, shown in [Figure 3-1](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch03.html#ch03_figure_1_1765466780086782), is to draw a diagram with a single box representing the software system that is the scope/focus of the system context diagram. In this case it’s the _Internet Banking System_.

![[../../assets/Pasted image 20260524184005.png]]

 Figure 3-1. An example system context diagram for a fictional Internet Banking System (step 1)

Next we need to identify the various people that use the Internet Banking System. In this example there’s just one type of user - _Personal Banking Customers_ who have one or more bank accounts, and want to view their account balances and make payments online. [Figure 3-2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch03.html#ch03_figure_2_1765466780086818) adds this user and their relationship with the Internet Banking System.

![[../../assets/Pasted image 20260524184030.png]]
 Figure 3-2. An example system context diagram for a fictional Internet Banking System (step 2)

With the people identified, we next need to understand the other software systems that the Internet Banking System interacts with. In this example, let’s assume that the bank has been in existence for a few decades, which means they already have customers with bank accounts. As the team building the Internet Banking System, we’re not building a bank or a database of customers and transactions; we’re just building a way for existing customers to do things online, via the web.

The bank already has a _Core Banking System_ (an off-the-shelf product) that manages all of the banking data, and we know that it provides an API that we can use to access the banking data and make transactions. So we’ll add this to the diagram, as shown in [Figure 3-3](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch03.html#ch03_figure_3_1765466780086848).

![[../../assets/Pasted image 20260524184047.png]]
 Figure 3-3. An example system context diagram for a fictional Internet Banking System (step 3)

We likely need to send emails to our customers, for multi-factor authentication, fraud alerts, transaction success/failure notifications, and more. As the team building the Internet Banking System, we don’t want to reinvent the wheel and waste time by building an email delivery service. Instead, we just want to use whatever the bank is using already. In this case the bank has an existing cloud contract with Amazon Web Services (AWS), and already uses the _Simple Email Service_ to send emails elsewhere in the bank. We’ll use this too. [Figure 3-4](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch03.html#ch03_figure_4_1765466780086866) shows this added to the diagram.

![[../../assets/Pasted image 20260524184104.png]]
 Figure 3-4. An example system context diagram for a fictional Internet Banking System (step 4)

That completes the system context diagram. In summary, it shows that:

1. Personal Banking Customers use the Internet Banking System to view information about their bank accounts, and to make payments.
    
2. The Internet Banking System itself uses the bank’s existing Core Banking System, which is the store of banking information and handles banking functionality such as making payments.
    
3. The Internet Banking System also makes use of Amazon Web Services Simple Email Service to send e-mails to customers, for use cases such as multi-factor authentication, fraud alerts, etc.
    

As I’ve already mentioned, the C4 model is notation independent, and we’ll look at notation in detail during Chapter 10. For now though, here’s a summary of the notation that I’ve used for this example diagram:

- People are represented with a person shape, inside which is a name and short description.
    
- Software systems are represented as a rectangle with rounded corners, inside which is a name and short description.
    
- Relationships are represented by unidirectional arrows using a dashed line style, with a short label to describe the intent of the relationship.
    
- The diagram has been titled “System Context View: Internet Banking System” to indicate that it’s showing the system context for the Internet Banking System.
    

[Figure 3-5](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch03.html#ch03_figure_5_1765466780086883) shows the visual diagram key/legend I would use to accompany the system context diagram.

![[../../assets/Pasted image 20260524184123.png]]
 Figure 3-5. A diagram key/legend for the example system context diagram

You will additionally notice that each element on the example diagram has some descriptive text to explicitly indicate the _type_ of the element. For people this is “[Person]”, and for software systems this is “[Software System]”. As we’ll see in Chapter 10, this is something that I firmly recommend to avoid any ambiguity about what the boxes on a diagram represent.

# Summary

This chapter has described the purpose of the C4 system context diagram - a high-level zoomed out view of a software system, illustrating how it fits into the world around it, in terms of the people who use it and the relationships with other software systems. The next chapter will zoom in to the software system with a container diagram.
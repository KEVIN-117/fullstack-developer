With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 6th chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

The fourth and final zoom level defined by the C4 model is _code_. This chapter describes the code-level diagram that can be used to show the internal implementation details of a component.

# Intent

The intent of a code diagram is to illustrate the structure of the code within a single component, which can help answer the following questions:

- How is a component decomposed into code-level building blocks?
    
- Which of these code-level building blocks are publicly exported/exposed by the component, and which are internal implementation details?
    
- How large and complicated is the component?
    

# Scope

The scope of a code diagram is a _single component_. As we’ll see shortly, a UML class diagram is a good way to illustrate code if you’re using an object-oriented (OO) programming language such as Java, C#, C++, etc. UML class diagrams have often been used to describe an _entire application_, but this approach rarely works in the real world.

Imagine you have a Java application that is built from thousands of Java classes. Creating a single UML class diagram to illustrate the entire application will result in a huge diagram with thousands of boxes and arrows, which is not particularly useful to anybody, irrespective of how well-structured the code is. The key to using UML class diagrams is to _limit their scope_. The C4 model code diagram does this by limiting the scope to show the internals of a single component.

# Content

The code diagram should show the various code-level building blocks supported by the programming language being used. With Java and C#, for example, this would be _classes and interfaces_ in _packages and namespaces_. You could certainly invent your own way to visually represent these concepts but, if you’re using an object-oriented programming language, a good way to do this is to simply use a UML class diagram.

A word of caution. It’s very easy to include a considerable amount of detail on a UML class diagram, and this is especially true if you are reverse-engineering a diagram from code that has already been written. Although it’s tempting to include every property and method for each class, I would resist this temptation and only include as much information as you need to tell the story that you want to tell. As an example, you usually don’t need to show every property and method if your goal is to provide a high-level summary of how a component works.

# Motivation

I’ll be honest with you - there are very few reasons to create code-level diagrams, because the questions that I listed in the Intent section of this chapter can usually be answered by looking at the code. I rarely use code diagrams myself. That said, code diagrams can be a useful way to summarise large and complicated components, or perhaps to illustrate how a particular pattern works within a component (we’ll see an example of this shortly).

# Audience

As you will have likely guessed, the intended audience for code diagrams are the engineers building or maintaining the software. This level of detail is typically far too much for other audiences.

# Recommended?

For software that is already written, this level of detail already exists in the code, and code diagrams are usually available _on-demand_ from tooling such as Integrated Development Environments (IDEs). I wouldn’t recommend diagrams at this level of detail for anything but the most important or complicated components though.

This does raise the question of why the C4 model defines a code level diagram, but we’ll answer this in Chapter 11 when we look beyond the basics.

# Example

Let’s complete our journey through the static structure diagrams that make up the C4 model, by zooming into the _Core Banking System Adapter_ component to show the code inside it. Since we’ve chosen to use Java for the implementation, and Java is an Object Oriented (OO) language, a UML class diagram works well here.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch06_figure_1_1768319633559539.png)

 Figure 6-1. An example code diagram for the Core Banking System Adapter

[Figure 6-1](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch06.html#ch06_figure_1_1768319633559539) shows a UML class diagram that I’ve created manually, in this case using PlantUML (a “diagrams as code” tool). It shows that the Core Banking System Adapter component has a public interface (_CoreBankingSystemAdapter_) that defines the component’s contract, and a package-protected implementation class (_CoreBankingSystemAdapterImpl_). This in turn creates and pools connections to the Core Banking System using a _CoreBankingSystemConnection_ class, which is able to send XML requests to and receive XML responses from the Core Banking System.

Each specific type of request we need to send is implemented by a class that knows how to format an XML document representing that request. Similarly each response is implemented by a class that knows how to deserialize an XML response into our own domain classes. The example I’ve chosen to show is the pair of _BankAccountsRequest_ and _BankAccountsResponse_ classes, which are used when requesting the set of bank accounts owned by a customer.

There’s much more to the internals of the component when you consider authentication, error handling, and so on, but this simplified diagram is enough to summarise how it works, and to provide some guidance to other engineers as to how they should implement further calls to the Core Banking System using the same pattern - in this case a pair of request and response classes.

The alternative to manually creating a UML class diagram is to reverse-engineer it from the code. This obviously only works if the software exists, and it will likely show you too much detail by default. [Figure 6-2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch06.html#ch06_figure_2_1768319633559569) shows a screenshot of IntelliJ IDEA after asking it to generate a UML class diagram of a particular Java package (folder), which corresponds to the boundary of the _Core Banking System Adapter_ component.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch06_figure_2_1768319633559569.png)

 Figure 6-2. An alternative example code diagram for the Core Banking System Adapter, generated on demand from an IDE

This nicely illustrates that this level of detail is potentially available on demand from your IDE. The trade-off here is that you may need to configure the resulting diagram to hide the properties and methods that are not required for explaining how a particular feature works.

# Summary

This chapter has described the code diagram - the lowest level of static structure diagram defined by the C4 model that shows the internal code-level implementation details of a single component. Is this diagram useful in day-to-day activities? Arguably not, but it’s there if you do need it. Next we will take a look at the first of three supporting diagrams defined by the C4 model.

table of contents

search

settings

Previous chapter

[5. Component Diagram](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch05.html)

Next chapter

[7. Dynamic Diagram](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch07.html)

Table of contents collapsed
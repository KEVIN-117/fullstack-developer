With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 1st chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

We’ve reached an interesting point in the software development industry. Globally distributed teams are building Internet-scale software systems in all manner of programming languages, with architectures ranging from monolithic systems through to those composed of dozens of distributed microservices. Agile and lean approaches are now no longer seen as niche ways to build software, and even the most traditional of organisations are seeking fast feedback with minimum viable products to prove their ideas. Techniques such as automated testing and continuous delivery, coupled with the power of cloud computing make this a reality for organisations of any size too. But something is still missing.

Ask somebody in the building industry to visually communicate the architecture of a building and you’ll likely be presented with site plans, floor plans, elevation views, cross-section views, and detailed drawings. In contrast, ask a software developer to visually communicate the software architecture of a software system and you’ll likely get a confused mess of boxes and lines.

Through my workshops since the mid-2000s, I’ve asked thousands of software developers around the world to draw software architecture diagrams, and continue to do so today. Sometimes this is done as part of a software architecture kata, where groups of people are tasked with designing a software system. Other times it’s done as part of a diagramming workshop where I ask software developers to draw some diagrams to describe the software architecture of a software system/product they are currently working on. Either way, the result is the same - an ad hoc collection of “boxes and arrows” diagrams that make little sense to anybody outside of the group that created them. This is clearly a huge blocker for communication.

Are software architecture diagrams still important and relevant in today’s modern world of software development though? Yes, and arguably more so than ever before given the increased delivery cadence many organisations are seeking, and the complexity of the solutions they are building. Software architecture diagrams are an incredibly useful tool for building a technical vision inside and outside of your team, scaling the team itself (e.g. onboarding new team members), and for capturing knowledge that will be used by your future self when maintaining long-lived software.

This chapter will start by taking a look at some of the common problems associated with software architecture diagrams, along with a discussion about how we’ve reached this point in the software development industry.

# What is Software Architecture?

To have a discussion about software architecture diagrams, we need to make sure that we have a good enough understanding of what software architecture is. A huge body of knowledge about software architecture already exists, tackling the subject from a wide range of sociotechnical angles, so what I’m about to say is going to be imperfect and incomplete, but it will suffice for the purposes of this book.

Grady Booch, one of the creators of the Unified Modeling Language (UML), once wrote that “architecture represents the significant decisions, where significance is measured by cost of change”. I really like this quote as a quick way to consider what is architectural in nature and what isn’t. During my workshops, I’ll ask the attendees what they consider to be difficult, and therefore expensive, to change about the software they are working on. The themes that emerge are:

Technology

The choice of programming languages, libraries, frameworks, target deployment environments, etc.

Elements

How software is decomposed into smaller executable building blocks at different levels of abstraction (e.g. monoliths vs microservices, code packaged by layer vs code packaged by feature) and how data is stored and structured (e.g. data schemas and formats).

Relationships

Dependencies and interactions between elements (e.g. synchronous vs asynchronous communication, data formats, protocols, etc).

My view is that software architecture diagrams should communicate the outcome of the decision making process, highlighting the set of significant decisions related to the themes above - technology, elements, and relationships. All of these are important concerns because they are a reflection of both the design choices that the team has made, along with the constraints of the surrounding organisation (e.g. technology constraints and vendor relationships, availability of people/skills, existing systems, integration protocols, existing deployment environments, operational practices, etc).

# Draw One or More Diagrams

Back to the workshops. The diagramming exercises I run are simply phrased as “draw one or more software architecture diagrams to describe your software system”. As you can probably imagine, the resulting diagrams are all very different. Some diagrams show a very high level of abstraction, others present low-level design details. Some diagrams show static structure, others show runtime and behavioural aspects. Some diagrams show technology choices, most don’t.

When you think about it, this result is unsurprising. Unlike the building industry, the software development industry lacks a standard, consistent way to think about, describe, and visually communicate software architecture. Yes, we do have UML, and I’ll talk about this later in the chapter, but arguably UML doesn’t help.

The diagramming exercise is group-based, typically with between two and four people per group. Rather than making the exercise easier, having a group of people with different backgrounds and experience tends to complicate matters, as time is wasted debating how best to complete the task. Asking people what they found challenging about the diagramming exercise reveals that visual communication of software architecture isn’t something that is proactively being taught. My experience suggests there are very few people teaching software teams how to effectively model, visualise, and communicate software architecture - both in industry and academic settings. It’s still seen as quite a niche topic, despite the impact that poor communication can have on software development teams.

I regularly hear the following questions during the exercise:

- “What types of diagrams should we draw?”
    
- “What notation should we use?”
    
- “What level of detail should we present?”
    
- “Who is the audience for these diagrams?”
    

Let’s look at some examples. The small selection of images that follow are recreations of photos of diagrams taken from my workshops, where groups have been asked to design a small “Financial Risk System” for a bank, and to draw one or more software architecture diagrams to communicate the software architecture of it. The purpose of the Financial Risk System is to import data from two data sources (a “Trade Data System” and a “Reference Data System”), merge the datasets, perform some risk calculations, and produce a Microsoft Excel compatible report for a number of internal business users. A subset of those business users can additionally modify some of the parameters that are used during the risk calculations.

It’s a small set of functional requirements, and the quality attributes (performance, scalability, etc) are equally constrained to ensure that the resulting solutions are as simple as possible and the exercise can be completed in 60-90 minutes. This is ultimately a software design exercise, but the focus is on the diagrams.

## Example 1

This first example, Figure 1-1, presents the group’s decomposition of the solution into a number of “functional” units, often referred to as a “functional view” of the solution.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_1_1758915928488024.png)

 Figure 1-1. Example diagram from a workshop that focuses on the functional decomposition of the solution

This diagram has the type of functions you would expect to see given the functional requirements of importing data, performing risk calculations, and generating reports. This diagram lacks information about relationships between the functional units though. Additionally we have a colour coding (the text in the boxes) to decipher. Are the text styles related to input vs output functions? Or perhaps business domain vs infrastructure? Existing vs new? Buy vs build? Different technology choices? Or maybe different people simply had different colour pens? It’s a useful diagram, but it only provides one viewpoint of the solution.

## Example 2

This next example, Figure 1-2, similarly shows the collection of high-level “logical” building blocks the software system is composed of, additionally with the relationships between them. Unfortunately the arrows are unlabelled, so we have almost no information about the purpose or intent of those relationships.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_2_1758915928488066.png)

 Figure 1-2. Example diagram from a workshop that shows a “logical view” of the solution, with unlabelled relationships

## Example 3

Figure 1-3 shows another very common style of diagram - most of the content is very generic, and describes almost every type of software system that we build as software developers.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_3_1758915928488088.png)

 Figure 1-3. Example diagram from a workshop that shows a very generic description of the solution

The large box labelled “RS” represents the boundary of the Financial Risk System that is being designed, and there are nested boxes showing how the system has been decomposed into smaller building blocks. The problem here is the boxes and lines are all labelled using very general words - “transport”, “error”, “DB”, etc. In particular, the box in the centre is labelled “bus. logic” (business logic), which is not hugely descriptive. Renaming this to “Financial Risk Calculator” would at least allow you to infer something about the business domain.

## Example 4

Figure 1-4 shows one of my all-time favourite diagrams - it looks like an airline route map!

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_4_1758915928488104.png)

 Figure 1-4. Example diagram from a workshop that resembles an airline route map

The central spine of this diagram makes some sense. It shows how data comes in from the source data systems (TDS and RDS) and then flows through a series of steps to import the data, perform some calculations, generate reports, and finally distribute them. From this perspective, it’s a relatively simple process diagram that provides a high-level overview of what the system is doing. It then becomes cluttered and confusing.

The circle on the right of the diagram seems important because everything is pointing to it, but I’m not sure why. It could be that the circle is some sort of an orchestration process, started on a schedule, starting each of the process steps in turn. But then how do you interpret the arrows between the process steps themselves?

The left of the diagram is equally confusing, with various lines of differing colours and styles zipping across one another. There are also boxes within boxes. If you look carefully you’ll see the letters “UI” (User Interface) upside-down too. The reason? Somebody wrote that from wherever they sat around the table!

I’ve seen similar diagrams play out on many of my workshops too, and the process tends to go something like this:

1. A simple diagram is created by the group.
    
2. The group then has a conversation about a particular feature, and starts adding lines to the diagram to represent the interactions between boxes to implement that feature.
    
3. Repeat step 2 a few times.
    
4. Somebody new joins the group, and more lines are added while trying to explain the intent of the original simple diagram.
    

This type of diagram can be useful during an up front design exercise, when you’re trying to understand the problem space and identify a solution. It shouldn’t be used to present a solution though, and it certainly should never be used for long-lived documentation.

## Example 5

Figure 1-5 is significantly more complicated than the other examples we’ve seen so far!

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_5_1758915928488120.png)

 Figure 1-5. Example diagram from a workshop that shows how a solution supports a number of behavioural scenarios

It’s a little like those “choose your own adventure” books that I used to read when I was young. You would start reading at page 1, to start the story, and eventually arrive at a fork where you need to decide what should happen next, perhaps by rolling some dice. If you want to attack the big scary creature you’ve just encountered, you turn to page 47. If you want to run away, turn to page 183. You keep making similar choices and eventually, and annoyingly, your character ends up being killed by a large dragon, so you have to start over again from page 1.

This diagram is similar. You start at the top and weave your way downwards through a complicated asynchronous and event-driven style of architecture. You often get to make a choice - should you follow the “fail event” or the “complete event”? As with the adventure books, all paths eventually lead to the (SNMP) trap on the left of the diagram. The diagram is too complicated. It’s trying to show how the solution can support a number of different behavioural scenarios simultaneously and is very overwhelming as a result.

## Example 6

Figure 1-6 describes the overall shape of a solution, showing how it is composed of a web application, a batch process, and a data store.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_6_1758915928488134.png)

 Figure 1-6. Example diagram from a workshop that shows responsibilities, but lacks technology choices

The diagram also includes the responsibilities of each part of the solution, which I really like because it shows how the functionality has been partitioned across the solution. The technology choices are missing though. Asking people why their diagrams don’t show any technology decisions results in a number of different responses:

- “the [financial risk system] solution is simple and can be built with any technology”
    
- “we don’t want to force a solution on developers”
    
- “it’s an implementation detail”
    

I firmly encourage technology choices to be included on software architecture diagrams, for a variety of reasons that are discussed later in this chapter.

## Example 7

Figure 1-7 is almost the complete opposite. It includes technology choices but neglects everything else, particularly given the unexplained acronym of “RS”, a box unhelpfully labelled “Error”, and the lack of lines connecting anything together. Essentially this diagram is just a set of technology choices drawn as a collection of boxes.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_7_1758915928488146.png)

 Figure 1-7. Example diagram from a workshop that focuses on technology choices

## Example 8

This next example, Figure 1-8, shows a mix of technology choices and functionality, but we’ve again lost the relationships. It’s a “boxes and no arrows” diagram!

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_8_1758915928488159.png)

 Figure 1-8. Example diagram from a workshop that shows boxes, but no arrows

The top section shows an ASP.NET web application, which I assume is being used for some sort of user interaction, although this diagram lacks any representation of users, and the function of the web application isn’t shown.

The bottom section is labelled “SQL Server” and there are a number of separate cylinders. It’s not clear to me whether these are separate database servers, database schemas, database tables, or something else entirely.

The middle section shows a collection of boxes, and I assume the intent here was to show how the solution is decomposed into smaller building blocks. And the building blocks are certainly reflective of what I would expect to see here - there’s something to import data, something to calculate risk, something to generate the report, and so on. I’m left confused from a structural perspective though. Are these boxes representing components or modules inside the ASP.NET application? Or are they services that sit between the ASP.NET application and the database?

As we’ve seen with previous diagrams, this one also lacks lines. It’s telling you something about how the solution has been decomposed into smaller building blocks, but it’s not showing you how those building blocks interact. It’s telling a story, but not the whole story.

## Example 9

The next example, Figure 1-9, resolves some of the issues we saw with the previous example (namely it adds relationships), but mixes different levels of abstraction, resulting in a diagram that can be interpreted in a number of different ways.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_9_1758915928488173.png)

 Figure 1-9. Example diagram from a workshop that shows an ambiguous mix of different abstraction levels

At the bottom of the diagram are a couple of SQL Server databases, and at the top of the diagram is a box labelled “Application”. Notice how that same box is additionally annotated “Console-C#”. So this solution seems to be made up of a C# console application and a couple of SQL Server databases. But what about the other boxes? Most are annotated “C#” and they’re much like what we’ve seen on some of the other diagrams. But it’s unclear what these boxes represent. Some people may view this diagram as describing a collection of C# microservices, but I suspect all of those C# boxes are actually components/modules inside the C# console application. The lack of boundaries makes this diagram confusing.

In summary, this diagram is probably showing multiple levels of abstraction, but it’s doing so in an ambiguous way. A quick fix here is to draw a big box around most of the C# boxes to indicate that they all reside inside the C# console application.

## Example 10

Much of the software that we build is used by humans, and having some representation of those human users on the diagrams helps readers to understand how the software fits into the real world. But those users need to be given a name, otherwise they are just anonymous clones, in the case of Figure 1-10, attacking the reporting service.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_10_1758915928488185.png)

 Figure 1-10. Example diagram from a workshop that shows unlabelled users

Whenever I see users represented, I want to know who those users are, and what sort of things they are doing with the software. This diagram shows neither.

# Common Diagramming Problems

Ideally, I’m looking for software architecture diagrams to illustrate the outcome of the design process the groups have gone through, showing a thoughtful balance of the decisions related to technology, elements, and relationships. The diagrams we’ve seen have a focus on some of these aspects, but not all of them. Specifically, the diagrams suffer from one or more of the following problems:

- Notation (e.g. colour coding, shapes, element sizes, line styles, etc) is not explained or is inconsistent.
    
- The purpose and meaning of elements is ambiguous.
    
- Relationships between elements are missing.
    
- Relationships between elements are unlabelled.
    
- Generic terms such as “business logic” are used.
    
- Acronyms and abbreviations are not explained.
    
- Technology choices are missing.
    
- Levels of abstraction are mixed.
    

Furthermore, the problems associated with a single diagram are often exacerbated when a collection of diagrams is created:

- The notation (shapes, colour coding, line styles, etc) is not consistent between diagrams.
    
- The naming of elements is not consistent between diagrams.
    
- The logical order in which to read the diagrams isn’t clear.
    
- There is no clear transition between one diagram and the next.
    

The example diagrams typify what I see during my workshops, but these types of problems are incredibly common in the real world too. A quick image search on the web for “software architecture diagram” will uncover a plethora of similar “boxes and arrows” diagrams that suffer from many of the same problems we’ve seen already.

# What Happened to UML?

Some of you might be thinking a couple of things - what happened to UML, and doesn’t UML solve many of these problems?

I graduated from university in 1996, and I remember attending a week-long introduction to UML relatively early in my career. As a software developer working for consulting companies, I had a regular need to write documentation that we could provide to our clients in order for them to run and maintain the software that we had built for or with them. In many cases we would use UML, creating a variety of diagrams with a variety of tools over the years. This became even more prevalent during the Use Case and Rational Unified Process (RUP) era around the year 2000. In short, I had a good level of experience with UML, I was reasonably familiar with it, and many of our clients requested its use. This all started to change somewhere around the mid-2000s, with UML usage declining rapidly.

I believe there are a number of factors that contributed to this. The early 1.x versions of UML were very lean when compared to UML 2.x, which was partly a result of the trend towards Model-Driven Architecture (MDA). The PDF version of the current UML specification (v2.5.1) is almost 800 pages in length. You don’t need to use or understand _all_ of the language, but the sheer size of UML is a considerable barrier to entry for many software developers.

UML has a variety of different diagrams addressing a variety of different concerns and levels of abstraction, yet much of the focus has historically been centered around UML class diagrams, which are generally a one-to-one reflection of the code. Whether you’re using UML for design or for documentation purposes, UML class diagrams can be useful if you have a small codebase of a dozen classes. It rapidly becomes overwhelming if you have anything at real world scale, with hundreds or thousands of classes. There was also a collection of tools in the early 2000’s that provided a way to reverse-engineer code _to_ UML class diagrams, forward-generate code _from_ UML diagrams, and even some tools that featured a full round-trip experience from code to diagrams and back again. These tools tended to be fragile (it was easy to break the reverse-engineering process) and perform poorly.

Most software developers today don’t sit down and sketch out a UML class diagram before writing code though. Instead they use a combination of techniques such as Test-Driven Development (TDD) and refactoring, all made possible with modern IDEs. This historic focus of UML on the code level is just too much, and it comes across as “too detailed” for many people today. On a related note, I’ve never felt there has been enough guidance about how to actually use UML, particularly at higher levels of abstraction, to model real-world enterprise software systems on a day-to-day basis. As I’ll illustrate shortly, using UML effectively is much more than just using the notation.

Then we have the wider Agile influence. 2001 saw the publication of the Manifesto for Agile Software Development, which describes a shift away from heavyweight documentation centric approaches with long feedback loops, to something more iterative and adaptive. The manifesto says, “we value working software over comprehensive documentation”, which many people have misinterpreted as, “don’t write any documentation”. In their haste to adopt Agile approaches, many software teams have “thrown out the baby with the bath water”. Diagrams and documentation have a strong association with traditional plan-driven approaches. Software development teams threw away the plan-driven approaches, but unfortunately diagrams and documentation were also discarded. That may sound a little extreme, but many of the software teams I work with have a very limited quantity of documentation for their software systems. I still regularly hear statements such as, “Agile doesn’t require documentation”, which is not true.

Those software teams that still do see the value in diagrams and documentation have abandoned or ignored UML, for a variety of reasons, in favour of something much more lightweight and, unfortunately, ad hoc. My anecdotal evidence, based upon speaking to thousands of software developers in over forty countries, suggests that UML is optimistically only used by a small percentage of the industry. My guess would be less than 10%, perhaps significantly less. There are certainly some exceptions to this based upon domain (e.g. teams building embedded software may use UML more than software developers building enterprise web apps), country, and even individual cities within a country, but the overall trend still remains the same. Even then, many teams that do claim to use UML tend to only use a fraction of the language - typically just class and sequence diagrams.

Academia has realised that we, as an industry, don’t use UML so much, and I know several universities that have reduced the number of hours they allocate to teaching it to students. One week of UML in a three year engineering course is not uncommon. The impact is that students are not really being exposed to UML at university and, after graduation, they’re joining teams in industry that are not using it. Fast-forward five years - these students are now tech leads and need to draw some diagrams. Will they use UML? Likely not, because they don’t have experience of using it. I don’t see how this situation can change without a major change to UML, or a major shift in the perception of UML.

All of that aside, UML arguably doesn’t solve the main problems with the diagrams we’ve seen anyway. If you’re wondering why, take a look at Figure 1-11, which is a version of Figure 1-2 that I’ve redrawn with UML notation.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch01_figure_11_1758915928488202.png)

 Figure 1-11. A version of Figure 1-2 that uses UML notation instead of ad hoc “boxes and arrows”

This shows a collection of UML components with dependency relationships between them. Does this convey more information than the “boxes and arrows” version shown previously in Figure 1-2? Arguably not. Is this even a “good” UML diagram? Not really. The diagram could be improved by adding details about the provided and required interfaces for each component, but even just adding some descriptions of the dependencies would help. Even with those improvements, this diagram is still quite vague because it’s missing information about the behaviour provided by the components. The addition of UML’s notation doesn’t help here. Many of the problems we’ve seen are far more fundamental, and can’t be fixed by introducing a standard notation.

# Technology Details on Diagrams

One of the things you may have noticed from the examples is that most don’t include much information about technology choices. This is very typical. Should software architecture diagrams include technology choices? In short, yes, absolutely!

Unfortunately there’s a common point of view that software architecture diagrams should be “high-level” and “logical” in nature rather than showing implementation details. In other words, they should show how the software system is decomposed into functional building blocks without showing how those building blocks are to be implemented. I disagree, and it’s worth looking at where this point of view comes from.

The world before Agile was a very different place, with “waterfall” style delivery cycles being the norm. These would typically have some type of an up front architecture/design phase followed by a separate implementation/coding phase. Many methodologies and frameworks suggested these separate phases were undertaken by separate teams, with the architecture team doing architecture/design, and the development team doing the implementation/coding. In my experience, it wasn’t uncommon for the architecture team to be staffed by non-developers or ex-developers who hadn’t coded for a few years. The architecture team was tasked with creating the logical architecture diagrams because, even if capable, it wasn’t their job to choose implementation details. These logical architecture diagrams were then handed over to the development team, who were tasked with turning that vision into reality. I believe this historic separation of activities and individuals is one of the primary reasons for the separation between “logical” and “physical” architecture diagrams, ultimately resulting in the belief that software architecture diagrams shouldn’t include technology choices today.

Modern software development is much more collaborative, teams are smaller, delivery cycles are shorter, and “hands-on coding architects” are more common. When you take all of this into account, it perhaps makes less sense to create and maintain multiple sets of architecture diagrams - one showing the logical view and one showing the physical implementation details. More importantly though, these high-level logical architecture diagrams miss an important part of the overall story. They don’t tell you anything about many of the aspects that are expensive to change, particularly with regards to technology choices.

“But we don’t want to tell developers what to do” is a phrase I still hear today inside many organisations. The fix for this is surprisingly simple - include the developers in the architecture and design work, collaborating together to decide upon the overall structure and the set of technology choices that will be used to implement that structure. Earlier in the chapter I said that architecture is the set of decisions that are difficult/expensive to change. This includes how we decompose the software system into smaller building blocks (elements), how those building blocks interact (relationships), and the technology choices that are used for their implementation. Software design is about making all of these decisions, carefully balancing the needs and skills of the development team with the needs and constraints of the surrounding environment. Technology choices are not just an implementation detail, particularly when they are expensive to change later.

Technology choices can help bring an otherwise idealistic and conceptual software design back down to earth so that it is grounded in reality, communicating the entirety of the design decisions rather than just a subset of them. The other side effect of adding technology choices to diagrams, particularly during the software design process, is that it helps to ensure the right people (i.e. people who understand technology) are drawing them.

# Ambiguity Leads to Assumptions

Understanding and resolving notational issues will certainly make the example diagrams better, but that alone won’t solve the bigger problem here. In many cases, the actual solutions are not evident. I wouldn’t advocate doing what I’m about to suggest, so please don’t do this! But you couldn’t give any of the example diagrams to a team of software developers and ask them to build the solution. Put simply, there’s nowhere near enough information being conveyed about the solution.

One of the easiest ways to understand whether a diagram makes sense is to give it to somebody else and ask them to interpret it without providing a narrative. I’m a firm believer that diagrams should be able to stand alone, to some degree anyway. Any narrative should complement the diagram rather than explain it. However, I often hear groups in my workshops say the following:

- “We’ll talk through the diagrams.”
    
- “This doesn’t make sense, but we’ll explain it during the presentation.”
    

The assumption that a diagram will be accompanied by a verbal narrative creates a gap between the information captured on the paper and the information that remains in people’s heads. Diagrams that need explaining have limited value, especially when used for the purpose of creating long-lived documentation.

Ambiguity on diagrams leads to assumptions being made. Sometimes these will be the correct assumptions, and sometimes they won’t. It depends upon the experience of the reader when compared to the experience of the diagram author. I’ve witnessed a group of three people happily designing a solution and drawing a diagram that has a number of boxes representing things that need to be built as a part of the solution. Sixty minutes pass and we switch from drawing diagrams to reviewing diagrams. Only then do you hear the following conversation:

Attendee 1

These boxes are components in a monolith, right?

Attendee 2

Oh, I thought we were designing a microservices architecture?

Attendee 3

Yes, I thought they were microservices too.

This has played out many times during my workshops, particularly those where the attendees are from different teams and/or organisations, and have different experience as a result. It demonstrates a failure to establish a shared context during the design exercise, with each individual team member viewing the world through their eyes only, and fitting the diagram to fit that world view.

# Summary

A big part of learning how to do something well is to also learn how not to do something. We often call these patterns and anti-patterns in software development. Having a knowledge of both the good (what to do) and the bad (what not to do) will make you better at whatever you’re trying to learn.

This chapter has introduced the problem that we’re trying to solve - software developers struggle to create good software architecture diagrams. Why is this important? In today’s world of modern software delivery, many teams have lost the ability to communicate what it is they are building, and it’s therefore no surprise that these same teams often seem to lack technical leadership, direction, and consistency. If you want to ensure that everybody is contributing to the same end-goal, you need to be able to effectively communicate that end-goal. And if you want agility and the ability to move fast, you need to be able to communicate that vision efficiently too.

In short, moving fast requires good communication. And good communication:

- Helps everybody understand the “big picture” of what is being built, and how this fits into the “bigger picture” of the organisational landscape in which it exists.
    
- Creates a shared vision for the software development team.
    
- Provides a “map” that can be used by software developers to navigate the source code.
    
- Provides a point of focus for technical conversations about new features, technical debt, risk reviews, threat modelling, architecture reviews, the impact of change, etc.
    
- Helps to fast-track the onboarding of new software developers into the team.
    
- Provides a way to explain what’s being built to people outside of the development team, whether they are technical or non-technical.
    

[Chapter 2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch02.html#ch02_the_basics_1758915929073866) will introduce my solution to the problems we’ve looked at - the C4 model for visualising software architecture - an easy to learn, developer friendly approach to software architecture diagramming.
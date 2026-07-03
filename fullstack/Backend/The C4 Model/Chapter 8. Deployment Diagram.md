With Early Release ebooks, you get books in their earliest form—the author’s raw and unedited content as they write—so you can take advantage of these technologies long before the official release of these titles.

This will be the 8th chapter of the final book.

If you’d like to be actively involved in reviewing and commenting on this draft, please reach out to the editor at [mcronin@oreilly.com](mailto:mcronin@oreilly.com).

To deliver value, the software that we build needs to be deployed somewhere so that it can be executed. Historically that infrastructure would be physical servers, but today it could be anything from virtualized servers and “Infrastructure as a Service” (IaaS) through to Docker, Kubernetes, and “Platform as a Service” (PaaS) environments on the cloud. The C4 model deployment diagram provides a way to diagram the deployment topology of your software.

# Intent

A deployment diagram allows you to illustrate how instances of software systems and containers in the static model are deployed on to the infrastructure within a given deployment environment (e.g. development, test, staging, live, etc).

# Scope

As a general guideline, I recommend scoping a deployment diagram to a single software system. In other words, the deployment diagram should show how a single software system is deployed into a given deployment environment. However, if you’re responsible for multiple software systems, all of which are deployed onto the same infrastructure, there’s nothing preventing you from relaxing this guideline to show how multiple software systems share that infrastructure.

# Content

The C4 deployment diagram is loosely based upon a [UML deployment diagram](https://en.wikipedia.org/wiki/Deployment_diagram), and includes a number of elements - container instances, software system instances, deployment nodes, and infrastructure nodes.

## Container instances

The primary purpose of a deployment diagram is to show how _instances_ of your applications and data stores (C4 containers) are deployed in a given deployment environment. For example, you might show how a Java application is deployed onto a server in your on-premises data center, or into a Docker container that runs on a cloud environment.

## Software system instances

In the same way that you might model an external dependency as a software system, you might want to model a specific _instance_ of that software system in a given deployment environment. We’ll see an example of this shortly.

## Deployment nodes

I use the _deployment node_ concept to represent a piece of infrastructure that you deploy software into. It represents where an instance of a software system or container is running, for example:

- Physical infrastructure (e.g. a physical server or device).
    
- Virtualized infrastructure (e.g. a server on an “infrastructure as a service” environment or a virtual machine).
    
- Containerised infrastructure (e.g. a Docker container).
    
- A server environment (e.g. a database server, Java EE web/application server, Microsoft IIS server).
    

Deployment nodes can themselves be nested to show a hierarchy of infrastructure.

## Infrastructure nodes

Where deployment nodes represent infrastructure that software is deployed into, I use the _infrastructure node_ concept to represent items or services that are _used_ in the environment, such as DNS services, routers, load balancers, firewalls, etc.

# Motivation

It’s very common to see C4 container diagrams that include too much information about how those applications and data stores will be deployed, usually into a live/production environment. For example, you might see references to Docker containers or Kubernetes pods. Or perhaps you’ll see references to cloud infrastructure such as Amazon Web Services, Microsoft Azure, or Google Cloud.

The problem with deployment details on a container diagram is that it’s typically only reflective of a _single_ deployment environment (the live/production environment), whereas most software systems are deployed into multiple different deployment environments simultaneously (e.g. development, test, and staging). I might run a Java application directly on a Java Virtual Machine on my laptop when doing development, but that same Java application might be built into a Docker image and deployed onto Amazon Web Services for the production deployment. It’s very confusing to show both of these deployment environments on a single diagram. A deployment diagram therefore provides a way to see how the applications and data stores inside a software system will be deployed to a single environment, resulting in two diagrams - one for the development environment and one for the live deployment environment.

# Audience

The audience for deployment diagrams is, broadly speaking, the same as that for container diagrams: the software architects and engineers who are building/maintaining the software, along with operations and support staff.

# Recommended?

Yes, I’d recommend deployment diagrams to all software engineering teams, particularly for documenting the live/production deployment environment since this is the most critical deployment environment, and information can be required quickly when operational incidents occur.

# Example

Let’s walk through a couple of example deployment diagrams for the fictional _Internet Banking System_. The first will illustrate a development environment, and the second will illustrate the live environment.

Figure 8-1 shows the starting point for the development environment. The outermost box is a deployment node that represents the bank’s wide area network, signalling that all development activities take place within the bank’s network. Within this is a deployment node representing a developer laptop, and developers can choose a Microsoft Windows or Apple macOS laptop when they join the organisation.

To start the rest of the story, we’ll begin with the _Backend_ - the Java and Spring Boot application that provides a JSON/HTTP web API to the _UI_, which in turn communicates with the _Database_ and the _Statement Store_ along with the two external software systems. During development, the _Backend_ will be run on the developer laptop, inside a Java Virtual Machine that is installed locally. This makes it easy to start and stop the application, view the logs, and attach a profiler/debugger if required.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_1_1773432250071600.png)

 Figure 8-1. An example deployment diagram for the development environment of a fictional Internet Banking System (step 1)

Similarly, to facilitate easy development and debugging of the _UI_, [Figure 8-2](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch08.html#ch08_figure_2_1773432250071639) shows that the _UI_ will be run in a web browser that is locally installed. Communication between the _UI_ and _Backend_ can therefore be done by simple HTTP requests via a local address such as http://localhost:8080, negating the effort and complexity required to configure local TLS certificates.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_2_1773432250071639.png)

 Figure 8-2. An example deployment diagram for the development environment of a fictional Internet Banking System (step 2)

The _UI_, which is running in the web browser, needs to be loaded from somewhere that is accessible from the web browser itself. For development purposes, we’ve chosen to host the _Static Content_ via a local nginx server. Rather than install this directly on our laptop, we’ve instead chosen to run nginx via Docker, as shown in Figure 8-3.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_3_1773432250071664.png)

 Figure 8-3. An example deployment diagram for the development environment of a fictional Internet Banking System (step 3)

It’s a similar story with the _Database_. Figure 8-4 shows that we’ll run MySQL via Docker rather than installing it locally on the developer laptop.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_4_1773432250071683.png)

 Figure 8-4. An example deployment diagram for the development environment of a fictional Internet Banking System (step 4)

The _Statement Store_ is an object store, and more precisely an Amazon Web Services S3 object store that will be communicated with using the AWS S3 API via the AWS Java SDK that will be included in the _Backend_. This presents some options for how to configure a development environment, the two primary options being:

1. Create a real AWS S3 bucket on the cloud.
    
2. Run a service locally that can simulate the AWS S3 API.
    

The first option is arguably easier, but the potential downsides include the cost of hosting the bucket, Internet connectivity is required in the development environment, and there’s a possibility of leaking data if the bucket is not secured properly. For this reason we’ll select option 2, and in this case we’ll use MinIO (a high-performance, S3-compatible object store) that we will again run via Docker. Figure 8-5 shows this addition.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_5_1773432250071699.png)

 Figure 8-5. An example deployment diagram for the development environment of a fictional Internet Banking System (step 5)

The diagram in its current form shows how instances of the applications and data stores (the C4 containers) that make up the _Internet Banking System_ are deployed onto a developer laptop. We still have the _AWS Simple Email Service_ and _Core Banking System_ that the _Backend_ integrates with. Ideally these also need to be running in our development environment so that we can do development work and integration testing.

When it comes to configuring _AWS Simple Email Service_ in our development environment, we again have a choice of using the real service on the cloud or installing an SES compatible service locally. Given the risks of leaking data via e-mails that could potentially be sent to the outside world, we’ll instead use a local service. Since this is a common use case across the bank, it turns out that another team in the bank has built a _Mock Simple Email Service_ that logs emails rather than sending them via the Internet, prepackaged as a Docker container. Figure 8-6 shows that we’ve chosen to use this.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_6_1773432250071714.png)

 Figure 8-6. An example deployment diagram for the development environment of a fictional Internet Banking System (step 6)

Finally we need access to a development version of the _Core Banking System_ so that we can do development and testing work of the _Core Banking System Adapter_ component that makes requests to retrieve a customer’s bank account information, make payments, etc. Again, this is a common use case in the bank, so the _Core Banking System_ team have made a development instance of the _Core Banking System_ available for developers to access, running on a server named corebanking-dev somewhere inside the bank’s data center. Figure 8-7 shows this addition.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_7_1773432250071729.png)

 Figure 8-7. An example deployment diagram for the development environment of a fictional Internet Banking System (step 7)

It’s worth mentioning that we’re using the concept of abstraction to our advantage here. The diagram illustrates that an _instance_ of the _Core Banking System_ software system is running on the corebanking-dev server, but that may not be strictly true. From our perspective as a developer on the _Internet Banking System_ team, the _Core Banking System_ is a software system dependency - we’re treating it as an opaque box that we can’t see inside of. We don’t really understand how it works, but the _Core Banking System_ is itself likely to be a collection of applications and data stores, potentially running on a collection of servers in the data center. We don’t really need to understand the complexity of this though. All I need to know as a developer is that I can point my _Backend_ instance to corebanking-dev in order to make API calls to the development instance of the _Core Banking System_.

Figure 8-8 completes the development environment story by showing the visual diagram key, which is almost the same as that used for the example container diagram (Figure 4-7), with the addition of a deployment node shape.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_8_1773432250071743.png)

 Figure 8-8. A diagram key for the example deployment diagra

The live environment for the Internet Banking System is necessarily more complicated, as illustrated in [Figure 8-9](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch08.html#ch08_figure_9_1773432250071763), but follows a similar approach. The majority of the software runs inside the Amazon Web Services cloud environment, with the exception of the _UI_ and the _Core Banking System_.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_9_1773432250071763.png)

 Figure 8-9. An example deployment diagram for the live environment of a fictional Internet Banking System

In summary:

- The UI runs outside of our infrastructure, in the web browser of our customer’s computer.
    
- The customers load the UI by accessing https://ib.bigbank.com in their web browser.
    
- ib.bigbank.com is a DNS CNAME, configured on Cloudflare, that is an alias for an AWS S3 bucket into which the _Static Content_ is deployed. This CNAME is configured to use Cloudflare as a proxy, taking advantage of Cloudflare’s ability to cache static content, thereby reducing traffic to the S3 bucket, increasing performance, and saving money.
    
- The _UI_ makes API calls to the backend via https://ib-api.bigbank.com, which is another Cloudflare hosted DNS CNAME that is an alias for an AWS Application Load Balancer that forwards traffic to the _Backend_. Requests are not proxied here, since they can’t be cached.
    
- The _Backend_ itself is packaged up as a Docker image and executed inside the AWS environment via the AWS Fargate service, which provides an easy way to run Docker images without the need to provision servers ourselves. The Docker image would need to be pushed to a Docker repository (such as a private AWS Elastic Container Registry), but this isn’t shown on the diagram for brevity.
    
- The _Database_ is hosted via the AWS Relational Database Service, which is another AWS service that takes care of provisioning the underlying infrastructure for us.
    
- The _Statement Store_ S3 bucket is hosted via the real AWS S3 service.
    
- Similarly, the real AWS Simple Email Service is being used, shown as an instance of the software system running in the same AWS region.
    
- The live _Core Banking System_ is running on a server named corebanking-live, again within the bank’s data center, and the AWS Direct Connect service is being used to create a secure and fast private network between the AWS infrastructure and the bank’s data center.
    

A subtle change from the development version of the deployment diagram is that many of the protocols are now HTTPS rather than HTTP, reflecting the increased level of security in the live environment.

The diagram shows that everything is running inside the AWS eu-west-1 region, but I’ve chosen not to include the specific AWS availability zones. This is predominantly for brevity, but there’s nothing preventing you from adding these to your own deployment diagrams, along with other information such as subnets, network zones, etc.

Finally, the diagram key ([Figure 8-10](https://learning.oreilly.com/library/view/the-c4-model/9798341660113/ch08.html#ch08_figure_10_1773432250071782)) is very similar to that used for the development environment diagram (Figure 8-8), with the addition of an infrastructure node shape and a solid arrow to depict the special private network connection. A box with a dotted border has also been used to denote the various separate organisational boundaries - Cloudflare, Amazon Web Services, and the bank.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341660113/files/assets/ch08_figure_10_1773432250071782.png)

 Figure 8-10. A diagram key for the example live deployment diagram

# Summary

This chapter has introduced the C4 deployment diagram - a very useful tool for documenting how instances of your containers and software systems are deployed onto your infrastructure in a given deployment environment.

The next chapter takes a look at the system landscape diagram, which is a way to zoom out from a single software system in order to create a map of the software systems that reside within a particular group, department, or organisation.
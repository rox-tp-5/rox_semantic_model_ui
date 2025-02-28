# RoX Semantic Model UI

A Streamlit application for describing assets using both DCAT and OPC UA information models.

<!-- TOC -->

- [RoX Semantic Model UI](#rox-semantic-model-ui)
    - [Running with Docker](#running-with-docker)
        - [Prerequisites](#prerequisites)
        - [Quick Start](#quick-start)
        - [Data Persistence](#data-persistence)
    - [Manual Setup without Docker](#manual-setup-without-docker)
    - [Application Structure](#application-structure)
    - [Information Models](#information-models)
        - [DCAT-3 Data Catalog Vocabulary](#dcat-3-data-catalog-vocabulary)
            - [Key Components of DCAT-3](#key-components-of-dcat-3)
            - [Core Classes and Properties](#core-classes-and-properties)
        - [OPC UA Robotics Information Model](#opc-ua-robotics-information-model)
            - [Key Concepts of OPC UA](#key-concepts-of-opc-ua)
            - [Hierarchical Structure](#hierarchical-structure)
            - [Key Components in Robotics Model](#key-components-in-robotics-model)
    - [RoX Asset Types](#rox-asset-types)
        - [Raw Data](#raw-data)
        - [Models](#models)
            - [ROS Applications](#ros-applications)
            - [ROS Nodes](#ros-nodes)
            - [Movement Algorithms](#movement-algorithms)
        - [Software Services](#software-services)

<!-- /TOC -->

## Running with Docker

### Prerequisites
- Docker and Docker Compose installed on your system

### Quick Start

1. Clone this repository:
   ```
   git clone <repository-url>
   cd SemanticModel_UI
   ```

2. Build and start the Docker container:
   ```
   docker-compose up -d
   ```

3. Access the application in your browser:
   ```
   http://localhost:8501
   ```

4. To stop the application:
   ```
   docker-compose down
   ```

### Data Persistence

- Asset descriptions saved in the application will be stored in the `output` directory
- This directory is mounted as a volume, so data will persist even if the container is restarted

## Manual Setup (without Docker)

If you prefer to run the application without Docker:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

## Application Structure

- `app.py`: Main Streamlit application
- `assets/`: Directory containing data files
  - `dcat3.csv`: DCAT-3 standard classes and properties
  - `opcua_robotics_object_hierarchy.csv`: OPC UA robotics model hierarchy
- `output/`: Directory where asset descriptions are saved

## Information Models

### DCAT-3 (Data Catalog Vocabulary)

DCAT-3 is a W3C recommendation designed to facilitate interoperability between data catalogs published on the Web. It provides a standardized way to describe datasets in catalogs, making it easier to discover and use data across different domains and platforms.

#### Key Components of DCAT-3

1. **Catalog**: A curated collection of metadata about datasets and data services
2. **Dataset**: A collection of data, published or curated by a single agent
3. **Distribution**: A specific representation of a dataset, such as a downloadable file
4. **DataService**: A service that provides access to data
5. **CatalogRecord**: A record in a catalog that describes a single dataset or data service

#### Core Classes and Properties

- **dcat:Catalog**
  - Properties: dcat:dataset, dcat:service, dcat:catalog, dcterms:title, dcterms:description
  
- **dcat:Dataset**
  - Properties: dcterms:title, dcterms:description, dcat:distribution, dcat:contactPoint, dcterms:publisher
  
- **dcat:Distribution**
  - Properties: dcat:accessURL, dcat:downloadURL, dcterms:format, dcat:mediaType, dcterms:license
  
- **dcat:DataService**
  - Properties: dcat:endpointURL, dcat:servesDataset, dcterms:title, dcterms:description

DCAT-3 extends previous versions with improved support for data services, relationships between datasets, and dataset series. It also enhances compatibility with other standards like PROV-O for provenance information and VoID for RDF datasets.

### OPC UA Robotics Information Model

OPC UA (Open Platform Communications Unified Architecture) is a platform-independent, service-oriented architecture for industrial automation. The OPC UA Robotics specification extends this framework specifically for robotics applications.

#### Key Concepts of OPC UA

1. **AddressSpace**: A structured collection of Nodes that represent real objects, their definitions, and references between them
2. **Nodes**: Basic elements in OPC UA that represent objects, variables, methods, and types
3. **References**: Connections between Nodes that establish relationships
4. **TypeDefinition**: Templates that define the structure and semantics of Nodes

#### Hierarchical Structure

The OPC UA Robotics model is organized hierarchically:

1. **ObjectTypes**: Define templates for objects (e.g., MotionDeviceSystemType)
2. **Objects**: Instances of ObjectTypes (e.g., Controllers, MotionDevices)
3. **Variables/Methods**: Properties or actions associated with Objects

#### Key Components in Robotics Model

- **MotionDeviceSystemType**: Represents the entire robotic system
  - Contains Controllers, MotionDevices, and other components
  
- **MotionDeviceType**: Represents a specific robot or motion device
  - Contains Axes, PowerTrains, and other mechanical components
  
- **ControllerType**: Represents the control system for motion devices
  - Contains software components, task controls, and execution information

The OPC UA Robotics model provides a standardized way to represent and interact with robotic systems, enabling interoperability between different vendors and components.

## RoX Asset Types

In RoX, assets are categorized into three primary types: raw data, models, and software services. These assets form the foundation of the digital ecosystem and are designed to be shared across stakeholders to ensure interoperability, scalability, and innovation. 

### Raw Data

Data serves as the lifeblood of AI-driven robotic systems. This includes sensor data, operational logs, ROS-bags and environmental inputs that robots utilize for decision-making. The ecosystem ensures that raw data is standardized for seamless integration into various applications while maintaining data sovereignty. 

### Models

AI and semantic models are critical for enabling robots to interpret complex environments and tasks. These models include pre-trained machine learning algorithms, CAD-related files (i.e. .step-files), ROS-nodes, semantic frameworks for contextual understanding, and transformation mechanisms that adapt data formats to specific requirements. In the context of the RoX project, an example of a model asset is a ROS (Robot Operating System) application, node, or movement algorithm, which plays a critical role in enabling robotic systems to perform specific tasks efficiently and effectively. Below, we detail how these assets contribute to the robotic domain and their relevance within the RoX ecosystem. 

#### ROS Applications

A ROS application is a collection of nodes, libraries, and tools designed to execute complex robotic tasks. For instance, an application might integrate perception, motion planning, and control functionalities to enable a robot to autonomously navigate through an environment. ROS applications are modular and reusable, making them ideal for collaborative ecosystems like RoX. They provide a standardized framework for developers to build and deploy robotic solutions across various hardware platforms. 

#### ROS Nodes

A ROS node is a fundamental building block in robotic software architecture. It represents a single executable that performs specific functions, such as sensor data processing or actuator control. Nodes communicate with each other using topics, services, or actions within the ROS middleware. For example: 

- A perception node might process camera data to detect objects in the robot's environment. 
- A motion control node could compute joint trajectories for a robotic arm based on input from a planning algorithm.  
 
These nodes can be shared as assets within the RoX ecosystem, allowing developers to reuse existing functionality or extend it for new applications. 

#### Movement Algorithms

Movement algorithms are another critical type of model asset. These algorithms define how a robot moves within its workspace to achieve specific goals, such as picking up an object or navigating around obstacles. An example is the use of Probabilistic Movement Primitives (ProMPs), which provide a data-driven representation of movements. ProMPs enable robots to generalize learned trajectories to novel situations while maintaining adaptability and precision. For instance: 

- A pick-and-place task for an industrial robot could use ProMPs to adapt its trajectory when the target object is slightly displaced. 
- A mobile robot might employ a motion planning algorithm based on probabilistic roadmaps (PRMs) for collision-free navigation in dynamic environments. 
 
These algorithms are often encapsulated within ROS nodes or libraries and can be integrated into larger applications. 

### Software Services

These include APIs, middleware solutions, and cloud-edge integration tools that facilitate functionalities like real-time communication, task orchestration, and system diagnostics. Software services in RoX are designed to be modular and reusable across multiple use cases, ensuring efficient resource utilization. 
 
The ability to share these assets across the ecosystem fosters collaboration among stakeholders and accelerates innovation cycles. Advanced governance mechanisms ensure secure access while protecting intellectual property.
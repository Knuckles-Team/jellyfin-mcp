# NODE_AGENTS.md - Dynamic Agent Registry

This file tracks the generated agents from MCP servers, Universal Skills, and Skill Graphs.

## Agent Mapping Table

| Name | Description | System Prompt | Tag | Skills | Tools | Skill Count | Tool Count | Avg Score |
|------|-------------|---------------|-----|--------|-------|-------------|------------|-----------|
| rust_programmer | You are a Rust systems and performance expert specializing in writing extremely safe, high-performance, and reliable systems using Rust. Your mission is to leverage Rust's unique guarantees around... | prompts/rust_programmer.md | - | rust-docs | - | 1 | 0 | 60 |
| browser_automation | **Observed in**: Assistant internal architecture | prompts/browser_automation.md | - | web-design-guidelines, browser-tools, web-artifacts, web-crawler, agent-browser | - | 5 | 0 | 40 |
| base_agent | --- | prompts/base_agent.md | - | - | - | 0 | 0 | 5 |
| typescript_programmer | You are an elite TypeScript programmer and reviewer with expertise in building type-safe, scalable, and resilient applications using modern web engineering principles. You also specialize in creating... | prompts/typescript_programmer.md | - | svelte-docs, react-docs, react-development, nestjs-docs, canvas-design, nextjs-docs, nodejs-docs, tdd-methodology, web-artifacts, shadcn-docs, vitejs-docs, remix-docs, reactrouter-docs, tanstack-docs, redux-docs, vercel-docs, vuejs-docs | - | 17 | 0 | 100 |
| verifier | You are an elite quality assurance expert and verification specialist. Your goal is to evaluate if the results accurately and comprehensively address the user's query, while also actively attempting... | prompts/verifier.md | - | spec-verifier, tdd-methodology | - | 2 | 0 | 60 |
| data_scientist | You are an elite Data Scientist and Machine Learning engineer. You possess unparalleled skills in exploring tabular data, building neural networks, analyzing trends, and constructing production ML... | prompts/data_scientist.md | - | tensorflow-docs, langchain-docs, matplotlib-docs, pandas-docs, pytorch-docs, jupyter-notebook, scipy-docs, huggingface-docs, scikit-learn-docs, numpy-docs | - | 10 | 0 | 90 |
| tool_guidance | --- | prompts/tool_guidance.md | - | - | - | 0 | 0 | 5 |
| database_expert | You are a database architecture and optimization specialist responsible for ensuring the reliability, integrity, and performance of application data layers. Your mission is to design efficient... | prompts/database_expert.md | - | falkordb-docs, redis-docs, database-tools, couchbase-docs, mariadb-docs, qdrant-docs, postgres-docs, chromadb-docs, neo4j-docs, mongodb-docs, mssql-docs | - | 11 | 0 | 100 |
| project_manager | You are an expert Technical Project Manager and Scrum Master. You orchestrate humans, agents, roadmaps, and communication channels. You effortlessly bridge the gap between high-level engineering... | prompts/project_manager.md | - | github-tools, session-handoff, internal-comms, google-workspace, spec-generator | - | 5 | 0 | 70 |
| agent_engineer | You are an agent engineering mastermind! You live and breathe agentic systems—designing agents that design agents, building MCP servers that unlock new capabilities, and weaving skill graphs that... | prompts/agent_engineer.md | - | agents-md-generator, agent-workflows, agent-spawner, skill-builder, agent-package-builder, agent-builder, skill-installer, fastmcp-docs, mcp-builder, mcp-client, self-improver, skill-graph-builder, pydantic-ai-docs | - | 13 | 0 | 100 |
| debugger_expert | You are the definitive Debugging Expert. You step into burning codebases, decipher cryptic stack traces, untangle deep memory leaks, and stabilize critical failures across platforms. You remain calm... | prompts/debugger_expert.md | - | developer-utilities, agent-builder | - | 2 | 0 | 60 |
| java_programmer | You are a seasoned Java and Enterprise Developer. You navigate massive object-oriented codebases with ease, wrangling the JVM, Spring Boot, and enterprise design patterns into highly scalable backend... | prompts/java_programmer.md | - | java-docs | - | 1 | 0 | 60 |
| safety_guard | --- | prompts/safety_guard.md | - | - | - | 0 | 0 | 5 |
| cloud_architect | You are a visionary Cloud Architect. You conceptualize, map, and deploy the invisible highways of the internet. You specialize in AWS, Azure, GCP, and general cloud-native topologies. You design... | prompts/cloud_architect.md | - | azure-docs, gcp-docs, developer-utilities, c4-architecture, aws-docs | - | 5 | 0 | 70 |
| mobile_programmer | You are a top-tier Mobile Application Programmer. You breathe React Native, iOS, and Android build pipelines. Your mission is to write intuitive, fast, and 60FPS mobile interfaces utilizing modern... | prompts/mobile_programmer.md | - | react-docs, react-native-skills | - | 2 | 0 | 60 |
| critique | --- | prompts/critique.md | - | spec-verifier, tdd-methodology, self-improver | - | 3 | 0 | 25 |
| python_programmer | You are a Python programming wizard! You breathe Pythonic code and dream in async generators. Your mission is to craft production-ready Python solutions that follow PEP 8 and project standards. | prompts/python_programmer.md | - | fastapi-docs, tdd-methodology, agent-package-builder, django-docs, api-wrapper-builder, agent-builder, python-docs, pydantic-docs, jupyter-notebook, mcp-builder, developer-utilities, fastmcp-docs, pydantic-ai-docs | - | 13 | 0 | 100 |
| c_programmer | You are a ruthless C Systems Programmer. You operate at the lowest levels of the software stack, where memory is managed manually, pointers dictate structure, and performance is measured in... | prompts/c_programmer.md | - | developer-utilities, c-docs | - | 2 | 0 | 60 |
| coordinator | --- | prompts/coordinator.md | - | internal-comms, agent-workflows, task-planner, session-handoff | - | 4 | 0 | 25 |
| planner | You are a Project Planner and task orchestration expert. Your goal is to decompose user requests into high-fidelity, phased TaskLists that guide implementation from concept to completion, ensuring... | prompts/planner.md | - | internal-comms, task-planner, brainstorming, constitution-generator, spec-generator | - | 5 | 0 | 70 |
| researcher | You are a master discovery agent and multi-vector search expert. Your goal is to gather high-fidelity information from various sources to support complex agentic workflows and provide thorough... | prompts/researcher.md | - | web-design-guidelines, browser-tools, web-artifacts, web-crawler, agent-browser, web-search, web-fetch | - | 7 | 0 | 90 |
| golang_programmer | You are an expert Golang programmer and reviewer. Your mission is to write simple, efficient, and highly concurrent applications using Go, following idiomatic Gopher patterns. | prompts/golang_programmer.md | - | go-docs | - | 1 | 0 | 60 |
| ui_ux_designer | You are a legendary UI/UX Designer and Frontend Artist. You refuse to build generic MVPs; every pixel you construct is deliberate, vibrant, dynamic, and cinematic. You think in layout structures,... | prompts/ui_ux_designer.md | - | chakra-ui-docs, web-design-guidelines, material-ui-docs, canvas-design, shadcn-docs, web-artifacts, brand-guidelines, website-cloner, website-builder, radix-ui-docs, framer-docs, algorithmic-art, theme-factory | - | 13 | 0 | 100 |
| document_specialist | You are a premier Document and Presentation Specialist. You specialize in the extraction, conversion, formatting, and generation of dense documents. Whether processing complex PDFs, migrating legacy... | prompts/document_specialist.md | - | marp-presentations, document-tools, document-converter, creative-media | - | 4 | 0 | 70 |
| systems_manager | You are a relentless Systems Manager. You maintain the foundational environment—hardware, OS, and software stacks—ensuring these systems are healthy, optimized, and secure. You manage raw system... | prompts/systems_manager.md | - | uptime-kuma-docs, system-tools, home-assistant-docs, linux-docs, postiz-docs, owncast-docs | - | 6 | 0 | 90 |
| architect | --- | prompts/architect.md | - | mermaid-diagrams, brainstorming, product-strategy, user-research, spec-generator, c4-architecture | - | 6 | 0 | 45 |
| memory_instruction | You are a system that manages how agent memory files are loaded and processed. Your purpose is to establish that user-provided instructions take absolute precedence over default behavior through the... | prompts/memory_instruction.md | - | - | - | 0 | 0 | 50 |
| javascript_programmer | You are the JavaScript Programmer. Stay playful but be brutally honest about runtime risks, async chaos, and bundle bloat. | prompts/javascript_programmer.md | - | react-docs, canvas-design, nodejs-docs, web-artifacts, developer-utilities | - | 5 | 0 | 60 |
| qa_expert | You are the QA expert. Risk-based mindset, defect-prevention first, automation evangelist. Be playful, but push teams to ship with confidence. | prompts/qa_expert.md | - | spec-verifier, tdd-methodology, developer-utilities, self-improver, testing-library-docs | - | 5 | 0 | 60 |
| agent_summary | You are a system that generates periodic background progress updates for sub-agents running in coordinator mode. Your purpose is to provide the parent agent with real-time awareness of what each... | prompts/agent_summary.md | - | - | - | 0 | 0 | 50 |
| safety_policy | > | prompts/safety_policy.md | - | - | - | 0 | 0 | 5 |
| cpp_programmer | You are an expert C++ Software Engineer. You thrive in the nexus of absolute performance and zero-cost abstraction paradigms. You command modern C++ (C++17, C++20), relying heavily on templates, RAII... | prompts/cpp_programmer.md | - | developer-utilities | - | 1 | 0 | 60 |
| security_auditor | You are a vigilant Security Auditor and Threat Modeler. You hunt for vulnerabilities, analyze deep architectural flaws, manage access controls, and enforce the highest levels of cryptographic and... | prompts/security_auditor.md | - | security-tools, linux-docs | - | 2 | 0 | 60 |
| devops_engineer | You are a DevOps and operational stability expert responsible for ensuring applications are deployed smoothly, run efficiently, and remain stable. Your mission is to design and maintain robust CI/CD... | prompts/devops_engineer.md | - | azure-docs, docker-docs, aws-docs, temporal-docs, minio-docs, gcp-docs, terraform-docs, cloudflare-deploy, c4-architecture | - | 9 | 0 | 90 |
| Jellyfin Itemrefresh Specialist | Expert specialist for itemrefresh domain tasks. | You are a Jellyfin Itemrefresh specialist. Help users manage and interact with Itemrefresh functionality using the available tools. | itemrefresh | - | stdio | 0 | 1 | 50 |
| Jellyfin Collection Specialist | Expert specialist for collection domain tasks. | You are a Jellyfin Collection specialist. Help users manage and interact with Collection functionality using the available tools. | collection | - | stdio | 0 | 1 | 50 |
| Jellyfin Tvshows Specialist | Expert specialist for tvshows domain tasks. | You are a Jellyfin Tvshows specialist. Help users manage and interact with Tvshows functionality using the available tools. | tvshows | - | stdio | 0 | 1 | 50 |
| Jellyfin Scheduledtasks Specialist | Expert specialist for scheduledtasks domain tasks. | You are a Jellyfin Scheduledtasks specialist. Help users manage and interact with Scheduledtasks functionality using the available tools. | scheduledtasks | - | stdio | 0 | 1 | 50 |
| Jellyfin Tmdb Specialist | Expert specialist for tmdb domain tasks. | You are a Jellyfin Tmdb specialist. Help users manage and interact with Tmdb functionality using the available tools. | tmdb | - | stdio | 0 | 1 | 40 |
| Jellyfin Dashboard Specialist | Expert specialist for dashboard domain tasks. | You are a Jellyfin Dashboard specialist. Help users manage and interact with Dashboard functionality using the available tools. | dashboard | - | stdio | 0 | 1 | 50 |
| Jellyfin Clientlog Specialist | Expert specialist for clientlog domain tasks. | You are a Jellyfin Clientlog specialist. Help users manage and interact with Clientlog functionality using the available tools. | clientlog | - | stdio | 0 | 1 | 50 |
| Jellyfin Search Specialist | Expert specialist for search domain tasks. | You are a Jellyfin Search specialist. Help users manage and interact with Search functionality using the available tools. | search | - | stdio | 0 | 1 | 50 |
| Jellyfin Backup Specialist | Expert specialist for backup domain tasks. | You are a Jellyfin Backup specialist. Help users manage and interact with Backup functionality using the available tools. | backup | - | stdio | 0 | 1 | 50 |
| Jellyfin Mediasegments Specialist | Expert specialist for mediasegments domain tasks. | You are a Jellyfin Mediasegments specialist. Help users manage and interact with Mediasegments functionality using the available tools. | mediasegments | - | stdio | 0 | 1 | 50 |
| Jellyfin Hlssegment Specialist | Expert specialist for hlssegment domain tasks. | You are a Jellyfin Hlssegment specialist. Help users manage and interact with Hlssegment functionality using the available tools. | hlssegment | - | stdio | 0 | 1 | 50 |
| Jellyfin Displaypreferences Specialist | Expert specialist for displaypreferences domain tasks. | You are a Jellyfin Displaypreferences specialist. Help users manage and interact with Displaypreferences functionality using the available tools. | displaypreferences | - | stdio | 0 | 1 | 50 |
| Jellyfin Misc Specialist | Expert specialist for misc domain tasks. | You are a Jellyfin Misc specialist. Help users manage and interact with Misc functionality using the available tools. | misc | - | stdio | 0 | 1 | 40 |
| Jellyfin Livetv Specialist | Expert specialist for livetv domain tasks. | You are a Jellyfin Livetv specialist. Help users manage and interact with Livetv functionality using the available tools. | livetv | - | stdio | 0 | 1 | 50 |
| Jellyfin Videoattachments Specialist | Expert specialist for videoattachments domain tasks. | You are a Jellyfin Videoattachments specialist. Help users manage and interact with Videoattachments functionality using the available tools. | videoattachments | - | stdio | 0 | 1 | 50 |
| Jellyfin Channels Specialist | Expert specialist for channels domain tasks. | You are a Jellyfin Channels specialist. Help users manage and interact with Channels functionality using the available tools. | channels | - | stdio | 0 | 1 | 50 |
| Jellyfin Dynamichls Specialist | Expert specialist for dynamichls domain tasks. | You are a Jellyfin Dynamichls specialist. Help users manage and interact with Dynamichls functionality using the available tools. | dynamichls | - | stdio | 0 | 1 | 50 |
| Jellyfin Library Specialist | Expert specialist for library domain tasks. | You are a Jellyfin Library specialist. Help users manage and interact with Library functionality using the available tools. | library | - | stdio | 0 | 1 | 50 |
| Jellyfin Audio Specialist | Expert specialist for audio domain tasks. | You are a Jellyfin Audio specialist. Help users manage and interact with Audio functionality using the available tools. | audio | - | stdio | 0 | 1 | 40 |
| Jellyfin Plugins Specialist | Expert specialist for plugins domain tasks. | You are a Jellyfin Plugins specialist. Help users manage and interact with Plugins functionality using the available tools. | plugins | - | stdio | 0 | 1 | 50 |
| Jellyfin Session Specialist | Expert specialist for session domain tasks. | You are a Jellyfin Session specialist. Help users manage and interact with Session functionality using the available tools. | session | - | stdio | 0 | 1 | 50 |
| Jellyfin Image Specialist | Expert specialist for image domain tasks. | You are a Jellyfin Image specialist. Help users manage and interact with Image functionality using the available tools. | image | - | stdio | 0 | 1 | 40 |
| Jellyfin Studios Specialist | Expert specialist for studios domain tasks. | You are a Jellyfin Studios specialist. Help users manage and interact with Studios functionality using the available tools. | studios | - | stdio | 0 | 1 | 50 |
| Jellyfin Environment Specialist | Expert specialist for environment domain tasks. | You are a Jellyfin Environment specialist. Help users manage and interact with Environment functionality using the available tools. | environment | - | stdio | 0 | 1 | 50 |
| Jellyfin Persons Specialist | Expert specialist for persons domain tasks. | You are a Jellyfin Persons specialist. Help users manage and interact with Persons functionality using the available tools. | persons | - | stdio | 0 | 1 | 50 |
| Jellyfin Trickplay Specialist | Expert specialist for trickplay domain tasks. | You are a Jellyfin Trickplay specialist. Help users manage and interact with Trickplay functionality using the available tools. | trickplay | - | stdio | 0 | 1 | 50 |
| Jellyfin Instantmix Specialist | Expert specialist for instantmix domain tasks. | You are a Jellyfin Instantmix specialist. Help users manage and interact with Instantmix functionality using the available tools. | instantmix | - | stdio | 0 | 1 | 50 |
| Jellyfin Movies Specialist | Expert specialist for movies domain tasks. | You are a Jellyfin Movies specialist. Help users manage and interact with Movies functionality using the available tools. | movies | - | stdio | 0 | 1 | 50 |
| Jellyfin Syncplay Specialist | Expert specialist for syncplay domain tasks. | You are a Jellyfin Syncplay specialist. Help users manage and interact with Syncplay functionality using the available tools. | syncplay | - | stdio | 0 | 1 | 50 |
| Jellyfin Startup Specialist | Expert specialist for startup domain tasks. | You are a Jellyfin Startup specialist. Help users manage and interact with Startup functionality using the available tools. | startup | - | stdio | 0 | 1 | 50 |
| Jellyfin Universalaudio Specialist | Expert specialist for universalaudio domain tasks. | You are a Jellyfin Universalaudio specialist. Help users manage and interact with Universalaudio functionality using the available tools. | universalaudio | - | stdio | 0 | 1 | 50 |
| Jellyfin User Specialist | Expert specialist for user domain tasks. | You are a Jellyfin User specialist. Help users manage and interact with User functionality using the available tools. | user | - | stdio | 0 | 1 | 40 |
| Jellyfin Musicgenres Specialist | Expert specialist for musicgenres domain tasks. | You are a Jellyfin Musicgenres specialist. Help users manage and interact with Musicgenres functionality using the available tools. | musicgenres | - | stdio | 0 | 1 | 50 |
| Jellyfin Suggestions Specialist | Expert specialist for suggestions domain tasks. | You are a Jellyfin Suggestions specialist. Help users manage and interact with Suggestions functionality using the available tools. | suggestions | - | stdio | 0 | 1 | 50 |
| Jellyfin Timesync Specialist | Expert specialist for timesync domain tasks. | You are a Jellyfin Timesync specialist. Help users manage and interact with Timesync functionality using the available tools. | timesync | - | stdio | 0 | 1 | 50 |
| Jellyfin Artists Specialist | Expert specialist for artists domain tasks. | You are a Jellyfin Artists specialist. Help users manage and interact with Artists functionality using the available tools. | artists | - | stdio | 0 | 1 | 50 |
| Jellyfin System Specialist | Expert specialist for system domain tasks. | You are a Jellyfin System specialist. Help users manage and interact with System functionality using the available tools. | system | - | stdio | 0 | 1 | 50 |
| Jellyfin Localization Specialist | Expert specialist for localization domain tasks. | You are a Jellyfin Localization specialist. Help users manage and interact with Localization functionality using the available tools. | localization | - | stdio | 0 | 1 | 50 |
| Jellyfin Itemupdate Specialist | Expert specialist for itemupdate domain tasks. | You are a Jellyfin Itemupdate specialist. Help users manage and interact with Itemupdate functionality using the available tools. | itemupdate | - | stdio | 0 | 1 | 50 |
| Jellyfin Librarystructure Specialist | Expert specialist for librarystructure domain tasks. | You are a Jellyfin Librarystructure specialist. Help users manage and interact with Librarystructure functionality using the available tools. | librarystructure | - | stdio | 0 | 1 | 50 |
| Jellyfin Mediainfo Specialist | Expert specialist for mediainfo domain tasks. | You are a Jellyfin Mediainfo specialist. Help users manage and interact with Mediainfo functionality using the available tools. | mediainfo | - | stdio | 0 | 1 | 50 |
| Jellyfin Quickconnect Specialist | Expert specialist for quickconnect domain tasks. | You are a Jellyfin Quickconnect specialist. Help users manage and interact with Quickconnect functionality using the available tools. | quickconnect | - | stdio | 0 | 1 | 50 |
| Jellyfin Videos Specialist | Expert specialist for videos domain tasks. | You are a Jellyfin Videos specialist. Help users manage and interact with Videos functionality using the available tools. | videos | - | stdio | 0 | 1 | 50 |
| Jellyfin Remoteimage Specialist | Expert specialist for remoteimage domain tasks. | You are a Jellyfin Remoteimage specialist. Help users manage and interact with Remoteimage functionality using the available tools. | remoteimage | - | stdio | 0 | 1 | 50 |
| Jellyfin Playstate Specialist | Expert specialist for playstate domain tasks. | You are a Jellyfin Playstate specialist. Help users manage and interact with Playstate functionality using the available tools. | playstate | - | stdio | 0 | 1 | 50 |
| Jellyfin Apikey Specialist | Expert specialist for apikey domain tasks. | You are a Jellyfin Apikey specialist. Help users manage and interact with Apikey functionality using the available tools. | apikey | - | stdio | 0 | 1 | 50 |
| Jellyfin Devices Specialist | Expert specialist for devices domain tasks. | You are a Jellyfin Devices specialist. Help users manage and interact with Devices functionality using the available tools. | devices | - | stdio | 0 | 1 | 50 |
| Jellyfin Filter Specialist | Expert specialist for filter domain tasks. | You are a Jellyfin Filter specialist. Help users manage and interact with Filter functionality using the available tools. | filter | - | stdio | 0 | 1 | 50 |
| Jellyfin Branding Specialist | Expert specialist for branding domain tasks. | You are a Jellyfin Branding specialist. Help users manage and interact with Branding functionality using the available tools. | branding | - | stdio | 0 | 1 | 50 |
| Jellyfin Genres Specialist | Expert specialist for genres domain tasks. | You are a Jellyfin Genres specialist. Help users manage and interact with Genres functionality using the available tools. | genres | - | stdio | 0 | 1 | 50 |
| Jellyfin Userviews Specialist | Expert specialist for userviews domain tasks. | You are a Jellyfin Userviews specialist. Help users manage and interact with Userviews functionality using the available tools. | userviews | - | stdio | 0 | 1 | 50 |
| Jellyfin Years Specialist | Expert specialist for years domain tasks. | You are a Jellyfin Years specialist. Help users manage and interact with Years functionality using the available tools. | years | - | stdio | 0 | 1 | 40 |
| Jellyfin Lyrics Specialist | Expert specialist for lyrics domain tasks. | You are a Jellyfin Lyrics specialist. Help users manage and interact with Lyrics functionality using the available tools. | lyrics | - | stdio | 0 | 1 | 50 |
| Jellyfin Trailers Specialist | Expert specialist for trailers domain tasks. | You are a Jellyfin Trailers specialist. Help users manage and interact with Trailers functionality using the available tools. | trailers | - | stdio | 0 | 1 | 50 |
| Jellyfin Activitylog Specialist | Expert specialist for activitylog domain tasks. | You are a Jellyfin Activitylog specialist. Help users manage and interact with Activitylog functionality using the available tools. | activitylog | - | stdio | 0 | 1 | 50 |
| Jellyfin Package Specialist | Expert specialist for package domain tasks. | You are a Jellyfin Package specialist. Help users manage and interact with Package functionality using the available tools. | package | - | stdio | 0 | 1 | 50 |
| Jellyfin Subtitle Specialist | Expert specialist for subtitle domain tasks. | You are a Jellyfin Subtitle specialist. Help users manage and interact with Subtitle functionality using the available tools. | subtitle | - | stdio | 0 | 1 | 50 |
| Jellyfin Playlists Specialist | Expert specialist for playlists domain tasks. | You are a Jellyfin Playlists specialist. Help users manage and interact with Playlists functionality using the available tools. | playlists | - | stdio | 0 | 1 | 50 |
| Jellyfin Userlibrary Specialist | Expert specialist for userlibrary domain tasks. | You are a Jellyfin Userlibrary specialist. Help users manage and interact with Userlibrary functionality using the available tools. | userlibrary | - | stdio | 0 | 1 | 50 |
| Jellyfin Configuration Specialist | Expert specialist for configuration domain tasks. | You are a Jellyfin Configuration specialist. Help users manage and interact with Configuration functionality using the available tools. | configuration | - | stdio | 0 | 1 | 50 |
| Jellyfin Items Specialist | Expert specialist for items domain tasks. | You are a Jellyfin Items specialist. Help users manage and interact with Items functionality using the available tools. | items | - | stdio | 0 | 1 | 40 |
| Jellyfin Itemlookup Specialist | Expert specialist for itemlookup domain tasks. | You are a Jellyfin Itemlookup specialist. Help users manage and interact with Itemlookup functionality using the available tools. | itemlookup | - | stdio | 0 | 1 | 50 |

## Tool Inventory Table

| Tool Name | Description | Tag | Source | Score | Approval |
|-----------|-------------|-----|--------|-------|----------|
| jellyfin-mcp_itemrefresh_toolset | Static hint toolset for itemrefresh based on config env. | itemrefresh | jellyfin-mcp | 50 | No |
| jellyfin-mcp_collection_toolset | Static hint toolset for collection based on config env. | collection | jellyfin-mcp | 50 | No |
| jellyfin-mcp_tvshows_toolset | Static hint toolset for tvshows based on config env. | tvshows | jellyfin-mcp | 50 | No |
| jellyfin-mcp_scheduledtasks_toolset | Static hint toolset for scheduledtasks based on config env. | scheduledtasks | jellyfin-mcp | 50 | No |
| jellyfin-mcp_tmdb_toolset | Static hint toolset for tmdb based on config env. | tmdb | jellyfin-mcp | 40 | No |
| jellyfin-mcp_dashboard_toolset | Static hint toolset for dashboard based on config env. | dashboard | jellyfin-mcp | 50 | No |
| jellyfin-mcp_clientlog_toolset | Static hint toolset for clientlog based on config env. | clientlog | jellyfin-mcp | 50 | No |
| jellyfin-mcp_search_toolset | Static hint toolset for search based on config env. | search | jellyfin-mcp | 50 | No |
| jellyfin-mcp_backup_toolset | Static hint toolset for backup based on config env. | backup | jellyfin-mcp | 50 | No |
| jellyfin-mcp_mediasegments_toolset | Static hint toolset for mediasegments based on config env. | mediasegments | jellyfin-mcp | 50 | No |
| jellyfin-mcp_hlssegment_toolset | Static hint toolset for hlssegment based on config env. | hlssegment | jellyfin-mcp | 50 | No |
| jellyfin-mcp_displaypreferences_toolset | Static hint toolset for displaypreferences based on config env. | displaypreferences | jellyfin-mcp | 50 | No |
| jellyfin-mcp_misc_toolset | Static hint toolset for misc based on config env. | misc | jellyfin-mcp | 40 | No |
| jellyfin-mcp_livetv_toolset | Static hint toolset for livetv based on config env. | livetv | jellyfin-mcp | 50 | No |
| jellyfin-mcp_videoattachments_toolset | Static hint toolset for videoattachments based on config env. | videoattachments | jellyfin-mcp | 50 | No |
| jellyfin-mcp_channels_toolset | Static hint toolset for channels based on config env. | channels | jellyfin-mcp | 50 | No |
| jellyfin-mcp_dynamichls_toolset | Static hint toolset for dynamichls based on config env. | dynamichls | jellyfin-mcp | 50 | No |
| jellyfin-mcp_library_toolset | Static hint toolset for library based on config env. | library | jellyfin-mcp | 50 | No |
| jellyfin-mcp_audio_toolset | Static hint toolset for audio based on config env. | audio | jellyfin-mcp | 40 | No |
| jellyfin-mcp_plugins_toolset | Static hint toolset for plugins based on config env. | plugins | jellyfin-mcp | 50 | No |
| jellyfin-mcp_session_toolset | Static hint toolset for session based on config env. | session | jellyfin-mcp | 50 | No |
| jellyfin-mcp_image_toolset | Static hint toolset for image based on config env. | image | jellyfin-mcp | 40 | No |
| jellyfin-mcp_studios_toolset | Static hint toolset for studios based on config env. | studios | jellyfin-mcp | 50 | No |
| jellyfin-mcp_environment_toolset | Static hint toolset for environment based on config env. | environment | jellyfin-mcp | 50 | No |
| jellyfin-mcp_persons_toolset | Static hint toolset for persons based on config env. | persons | jellyfin-mcp | 50 | No |
| jellyfin-mcp_trickplay_toolset | Static hint toolset for trickplay based on config env. | trickplay | jellyfin-mcp | 50 | No |
| jellyfin-mcp_instantmix_toolset | Static hint toolset for instantmix based on config env. | instantmix | jellyfin-mcp | 50 | No |
| jellyfin-mcp_movies_toolset | Static hint toolset for movies based on config env. | movies | jellyfin-mcp | 50 | No |
| jellyfin-mcp_syncplay_toolset | Static hint toolset for syncplay based on config env. | syncplay | jellyfin-mcp | 50 | No |
| jellyfin-mcp_startup_toolset | Static hint toolset for startup based on config env. | startup | jellyfin-mcp | 50 | No |
| jellyfin-mcp_universalaudio_toolset | Static hint toolset for universalaudio based on config env. | universalaudio | jellyfin-mcp | 50 | No |
| jellyfin-mcp_user_toolset | Static hint toolset for user based on config env. | user | jellyfin-mcp | 40 | No |
| jellyfin-mcp_musicgenres_toolset | Static hint toolset for musicgenres based on config env. | musicgenres | jellyfin-mcp | 50 | No |
| jellyfin-mcp_suggestions_toolset | Static hint toolset for suggestions based on config env. | suggestions | jellyfin-mcp | 50 | No |
| jellyfin-mcp_timesync_toolset | Static hint toolset for timesync based on config env. | timesync | jellyfin-mcp | 50 | No |
| jellyfin-mcp_artists_toolset | Static hint toolset for artists based on config env. | artists | jellyfin-mcp | 50 | No |
| jellyfin-mcp_system_toolset | Static hint toolset for system based on config env. | system | jellyfin-mcp | 50 | No |
| jellyfin-mcp_localization_toolset | Static hint toolset for localization based on config env. | localization | jellyfin-mcp | 50 | No |
| jellyfin-mcp_itemupdate_toolset | Static hint toolset for itemupdate based on config env. | itemupdate | jellyfin-mcp | 50 | No |
| jellyfin-mcp_librarystructure_toolset | Static hint toolset for librarystructure based on config env. | librarystructure | jellyfin-mcp | 50 | No |
| jellyfin-mcp_mediainfo_toolset | Static hint toolset for mediainfo based on config env. | mediainfo | jellyfin-mcp | 50 | No |
| jellyfin-mcp_quickconnect_toolset | Static hint toolset for quickconnect based on config env. | quickconnect | jellyfin-mcp | 50 | No |
| jellyfin-mcp_videos_toolset | Static hint toolset for videos based on config env. | videos | jellyfin-mcp | 50 | No |
| jellyfin-mcp_remoteimage_toolset | Static hint toolset for remoteimage based on config env. | remoteimage | jellyfin-mcp | 50 | No |
| jellyfin-mcp_playstate_toolset | Static hint toolset for playstate based on config env. | playstate | jellyfin-mcp | 50 | No |
| jellyfin-mcp_apikey_toolset | Static hint toolset for apikey based on config env. | apikey | jellyfin-mcp | 50 | No |
| jellyfin-mcp_devices_toolset | Static hint toolset for devices based on config env. | devices | jellyfin-mcp | 50 | No |
| jellyfin-mcp_filter_toolset | Static hint toolset for filter based on config env. | filter | jellyfin-mcp | 50 | No |
| jellyfin-mcp_branding_toolset | Static hint toolset for branding based on config env. | branding | jellyfin-mcp | 50 | No |
| jellyfin-mcp_genres_toolset | Static hint toolset for genres based on config env. | genres | jellyfin-mcp | 50 | No |
| jellyfin-mcp_userviews_toolset | Static hint toolset for userviews based on config env. | userviews | jellyfin-mcp | 50 | No |
| jellyfin-mcp_years_toolset | Static hint toolset for years based on config env. | years | jellyfin-mcp | 40 | No |
| jellyfin-mcp_lyrics_toolset | Static hint toolset for lyrics based on config env. | lyrics | jellyfin-mcp | 50 | No |
| jellyfin-mcp_trailers_toolset | Static hint toolset for trailers based on config env. | trailers | jellyfin-mcp | 50 | No |
| jellyfin-mcp_activitylog_toolset | Static hint toolset for activitylog based on config env. | activitylog | jellyfin-mcp | 50 | No |
| jellyfin-mcp_package_toolset | Static hint toolset for package based on config env. | package | jellyfin-mcp | 50 | No |
| jellyfin-mcp_subtitle_toolset | Static hint toolset for subtitle based on config env. | subtitle | jellyfin-mcp | 50 | No |
| jellyfin-mcp_playlists_toolset | Static hint toolset for playlists based on config env. | playlists | jellyfin-mcp | 50 | No |
| jellyfin-mcp_userlibrary_toolset | Static hint toolset for userlibrary based on config env. | userlibrary | jellyfin-mcp | 50 | No |
| jellyfin-mcp_configuration_toolset | Static hint toolset for configuration based on config env. | configuration | jellyfin-mcp | 50 | No |
| jellyfin-mcp_items_toolset | Static hint toolset for items based on config env. | items | jellyfin-mcp | 40 | No |
| jellyfin-mcp_itemlookup_toolset | Static hint toolset for itemlookup based on config env. | itemlookup | jellyfin-mcp | 50 | No |

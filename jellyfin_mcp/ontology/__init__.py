"""Media & Downloads ontology contribution (CONCEPT:JF-KG.ontology.kg).

Data-only subpackage: it carries ``media.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/media`` module — media asset management and download
tracking bridging qBittorrent, Jellyfin and the media downloader: download jobs,
media assets and their consumption patterns) which the scion-sdk hub
federates in via the ``scion_sdk.ontology_providers`` entry-point. It holds
no business logic and no heavy imports so the hub can resolve it cheaply.
"""

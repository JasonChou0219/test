Introduction
=============

Laboratory management and information systems (LMS, LIMS) have developed in recent years to support and integrate more
and more functions that are encountered in the laboratory on regular basis. Commercial software facilitates experiment
planning, analysis and other lab related activities such as audit trail, storage and user management. However, they
always exclude device management and device control. A user is always required to to run the experiments step by step,
transfer data, and translate input.

The main reason for the lack of this functionality is more obvious than one might think. It all boils down to a lack of
standardization. Devices in a laboratory environment cannot be integrated easily into a control software making it near
impossible to conduct experiments that require many devices at once. Experiments that rely on inter-device communication
in real-time , experiments that need to be flexible, adjustable to new findings, require a framework for easy integration,
management, data access and workflow design.

Based on SiLA. A mission to establish international standards in laboratory automation and to create open connectivity.
Goals are interoperability, flexibility, resource optimization for laboratory instrument integration and software
services based on standardized communication protocls an d content specifications. Open standard. Cost efficient.
Based on well established communication protocols (Http2, gRPC). For more information visit the SiLA website or check
out  their repository on GitLab.

SiLA is based on an inherent server-client architecture. Connection is established over a TCP/IP network.
SiLA servers and client

SiLA uses auto-discovery to broadcast services on the network. Accessing, managing and integrating these services
into workflows in the lab environment is not part of the SiLA standard. A software framework is needed to connect and
manage available lab devices.
